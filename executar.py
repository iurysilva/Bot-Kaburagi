from executaveis.executar_animes import *
from executaveis.executar_lembrete import *
from executaveis.executar_filmes import *


@cliente.event
async def on_ready():
    print('Kaburagi Iniciado!')


@slash.slash(name="kajuda",
             description="Exibe os comandos de ajuda.",
             options=[
                 create_option(
                     name="ignore",
                     description="ignore",
                     option_type=3,
                     required=False
                 )
             ]
             )
async def _ajuda(contexto, ignore=None):
    mensagem = Embed(title="O Kaburagi agora possui mais funcionalidades, para obter ajuda sobre cada uma use:")
    mensagem = adiciona_info(mensagem, autor=contexto.author)
    mensagem.add_field(name="/kajuda_lembretes", value="Crie e edite lembretes", inline=False)
    mensagem.add_field(name="/kajuda_animes", value="Pesquise e gerencie animes", inline=False)
    mensagem.add_field(name="/kajuda_filmes", value="Pesquise e gerencie filmes", inline=False)
    await contexto.send(embed=mensagem)


token = open('token.txt').read()
cliente.run(token)
