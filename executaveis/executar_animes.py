from executaveis.initiate_bot import *
import asyncio
from servicos.manipulacao_de_embed import adiciona_info

animes = Animes()


@slash.slash(name="kajuda_animes",
             description="Exibe todos os comandos da funcionalidade animes",
             options=[
                 create_option(
                     name="ignore",
                     description="ignore",
                     option_type=3,
                     required=False
                 )
             ]
             )
async def _ajuda_animes(contexto, ignore=None):
    embed = animes.ajuda()
    embed = adiciona_info(embed, contexto.author)
    await contexto.send(embed=embed)


@slash.slash(name="kanime_procura",
             description="Exibe informações sobre um anime específico",
             options=[
                 create_option(
                     name="anime",
                     description="Nome do anime.",
                     option_type=3,
                     required=True
                 )
             ]
             )
async def _anime_procura(contexto, anime):
    await contexto.send("Pesquisando...", delete_after=1)
    try:
        resultado = animes.procura(anime, autor=contexto.author)
    except ValueError:
        await contexto.send("Anime não encontrado")
        return 0
    resultado = adiciona_info(resultado, autor=contexto.author)
    try:
        await contexto.channel.send(embed=resultado)
    except discord.errors.Forbidden:
        await contexto.send("Bot não tem permissão nesse canal")
        return 0


@slash.slash(name="kanime_procura_detalhada",
             description="Exibe informações detalhadas sobre um anime específico",
             options=[
                 create_option(
                     name="anime",
                     description="Nome do anime.",
                     option_type=3,
                     required=True
                 )
             ]
             )
async def _anime_procura_detalhada(contexto, anime):
    await contexto.send("Pesquisando...", delete_after=1)
    try:
        resultado = animes.procura_detalhada(anime, autor=contexto.author)
    except ValueError:
        await contexto.send("Anime não encontrado")
        return 0
    resultado = adiciona_info(resultado, autor=contexto.author)
    try:
        await contexto.channel.send(embed=resultado)
    except discord.errors.Forbidden:
        await contexto.send("Bot não tem permissão nesse canal")
        return 0


@slash.slash(name="kanime_pool_adicionar",
             description="Insere um anime na pool",
             options=[
                 create_option(
                     name="nome",
                     description="Nome do anime.",
                     option_type=3,
                     required=True
                 )
             ]
             )
async def _anime_pool_adicionar(contexto, nome):
    await contexto.send("Pesquisando...", delete_after=1)
    embed = animes.procura(nome, contexto.author)
    anime = embed.title
    embed.title = "Você deseja adicionar o anime %s para a pool?" % anime
    try:
        mensagem = await contexto.channel.send(embed=embed)
    except discord.errors.Forbidden:
        await contexto.send("Bot não tem permissão nesse canal")
        return 0
    await mensagem.add_reaction("✅")
    await mensagem.add_reaction("❌")
    while True:
        try:
            reacao, usuario = await cliente.wait_for('reaction_add', timeout=30.0)
            if usuario.name == contexto.author.name and reacao.message == mensagem:
                resultado = animes.adicionar_anime_na_pool(reacao, usuario, anime, contexto.guild.name)
                resultado = adiciona_info(resultado, autor=contexto.author)
                await contexto.channel.send(embed=resultado)
                return 1
        except asyncio.TimeoutError:
            print("Usuário não reagiu a tempo\n")
            return 0


@slash.slash(name="kanime_pool_remover",
             description="Remove um anime da pool",
             options=[
                 create_option(
                     name="nome",
                     description="Nome do anime.",
                     option_type=3,
                     required=True
                 )
             ]
             )
async def _anime_pool_remover(contexto, nome):
    await contexto.send("Pesquisando...", delete_after=1)
    embed = animes.procura(nome, contexto.author)
    anime = embed.title
    nome_do_servidor = contexto.guild.name
    resultado = animes.remover_anime_da_pool(nome_do_servidor, anime)
    resultado = adiciona_info(resultado, autor=contexto.author)
    await contexto.send(embed=resultado)


@slash.slash(name="kanime_pool",
             description="Visualiza todos os animes da pool",
             options=[
                 create_option(
                     name="ignore",
                     description="ignore",
                     option_type=3,
                     required=False
                 )
             ]
             )
async def _anime_pool(contexto, ignore=None):
    nome_do_servidor = contexto.guild.name
    resultado = animes.visualizar_pool(nome_do_servidor)
    resultado = adiciona_info(resultado, autor=contexto.author)
    try:
        mensagem = await contexto.send(embed=resultado)
        linhas = animes.banco_de_dados.retornar_numero_de_linhas(nome_do_servidor, animes.tabela)
        for reagindo in range(linhas):
            await mensagem.add_reaction(animes.emojis[reagindo])
    except discord.errors.Forbidden:
        await contexto.send("Bot não tem permissão para reagir nesse canal")
        return 0


@slash.slash(name="kanime_pool_limpar",
             description="Limpa todos os animes da pool",
             options=[
                 create_option(
                     name="ignore",
                     description="ignore",
                     option_type=3,
                     required=False
                 )
             ]
             )
async def _anime_pool_limpar(contexto, ignore=None):
    nome_do_servidor = contexto.guild.name
    resultado = animes.limpa_pool(nome_do_servidor)
    resultado = adiciona_info(resultado, autor=contexto.author)
    await contexto.send(embed=resultado)

