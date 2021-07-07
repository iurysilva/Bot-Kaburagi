from servicos.initiate_bot import *

animes = Animes()


@slash.slash(name="kajuda_animes",
             description="Exibe todos os comandos da funcionalidade animes"
             )
async def _ajuda_animes(contexto):
    embed = animes.ajuda()
    embed = adiciona_info(embed, contexto.author)
    await contexto.send(embed=embed)


@slash.slash(name="kprocura",
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
async def _procura(contexto, anime):
    await contexto.send("Pesquisando...")
    resultado = animes.procura(anime, autor=contexto.author)
    await contexto.send(embed=resultado)


@cliente.command()
async def procura(contexto, *, anime):
    resultado = animes.procura(anime, autor=contexto.author)
    await contexto.send(embed=resultado)
