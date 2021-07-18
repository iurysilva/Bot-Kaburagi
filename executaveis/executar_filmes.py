from executaveis.initiate_bot import *
from funcionalidades import Filmes
import asyncio

filmes = Filmes()


@slash.slash(name="kajuda_filmes",
             description="Exibe todos os comandos da funcionalidade filmes",
             options=[
                 create_option(
                     name="ignore",
                     description="ignore",
                     option_type=3,
                     required=False
                 )
             ]
             )
async def _ajuda_filmes(contexto, ignore=None):
    embed = filmes.ajuda()
    embed = adiciona_info(embed, contexto.author)
    await contexto.send(embed=embed)


@slash.slash(name="kfilme_procura",
             description="Exibe informações sobre um filme específico",
             options=[
                 create_option(
                     name="filme",
                     description="Nome do filme.",
                     option_type=3,
                     required=True
                 )
             ]
             )
async def _filme_procura(contexto, filme):
    await contexto.send("Pesquisando...", delete_after=1)
    resultado = filmes.procura(filme)
    resultado = adiciona_info(resultado, autor=contexto.author)
    await contexto.channel.send(embed=resultado)


@slash.slash(name="kfilme_pool_adicionar",
             description="Insere um filme na pool",
             options=[
                 create_option(
                     name="nome",
                     description="Nome do filme.",
                     option_type=3,
                     required=True
                 )
             ]
             )
async def _filme_pool_adicionar(contexto, nome):
    await contexto.send("Pesquisando...", delete_after=1)
    embed = filmes.procura(nome)
    filme = embed.title
    embed.title = "Você deseja adicionar o filme %s para a pool?" % filme
    mensagem = await contexto.channel.send(embed=embed)
    await mensagem.add_reaction("✅")
    await mensagem.add_reaction("❌")
    while True:
        try:
            reacao, usuario = await cliente.wait_for('reaction_add', timeout=30.0)
            if usuario.name == contexto.author.name and reacao.message == mensagem:
                resultado = filmes.adicionar_filme_na_pool(reacao, usuario, filme, contexto.guild.name)
                resultado = adiciona_info(resultado, autor=contexto.author)
                await contexto.channel.send(embed=resultado)
                return 1
        except asyncio.TimeoutError:
            print("Usuário não reagiu a tempo\n")
            return 0


@slash.slash(name="kfilme_pool_remover",
             description="Remove um filme da pool",
             options=[
                 create_option(
                     name="nome",
                     description="Nome do filme.",
                     option_type=3,
                     required=True
                 )
             ]
             )
async def _filme_pool_remover(contexto, nome):
    await contexto.send("Pesquisando...", delete_after=1)
    embed = filmes.procura(nome)
    filme = embed.title
    nome_do_servidor = contexto.guild.name
    resultado = filmes.remover_filme_da_pool(nome_do_servidor, filme)
    resultado = adiciona_info(resultado, autor=contexto.author)
    await contexto.send(embed=resultado)


@slash.slash(name="kfilme_pool",
             description="Visualiza todos os filmes da pool",
             options=[
                 create_option(
                     name="ignore",
                     description="ignore",
                     option_type=3,
                     required=False
                 )
             ]
             )
async def _filme_pool(contexto, ignore=None):
    nome_do_servidor = contexto.guild.name
    resultado = filmes.visualizar_pool(nome_do_servidor)
    resultado = adiciona_info(resultado, autor=contexto.author)
    mensagem = await contexto.send(embed=resultado)
    linhas = filmes.banco_de_dados.retornar_numero_de_linhas(nome_do_servidor, filmes.tabela)
    for reagindo in range(linhas):
        await mensagem.add_reaction(filmes.emojis[reagindo])


@slash.slash(name="kfilme_pool_limpar",
             description="Limpa todos os filmes da pool",
             options=[
                 create_option(
                     name="ignore",
                     description="ignore",
                     option_type=3,
                     required=False
                 )
             ]
             )
async def _filme_pool_limpar(contexto, ignore=None):
    nome_do_servidor = contexto.guild.name
    resultado = filmes.limpa_pool(nome_do_servidor)
    resultado = adiciona_info(resultado, autor=contexto.author)
    await contexto.send(embed=resultado)
