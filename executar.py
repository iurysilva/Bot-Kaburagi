from executar_lembrete import *
from executar_animes import *


@slash.slash(name="kajuda",
             description="Exibe os comandos de ajuda."
             )
async def _ajuda(contexto):
    mensagem = Embed(title="O Kaburagi agora possui mais funcionalidades, para obter ajuda sobre cada uma use:")
    mensagem = adiciona_info(mensagem, autor=contexto.author)
    mensagem.add_field(name="/kajuda_lembretes", value="Crie e edite lembretes", inline=False)
    mensagem.add_field(name="/kajuda_animes", value="Pesquise sobre animes", inline=False)
    await contexto.send(embed=mensagem)

cliente.run('ODA4NzEzNTMzMzk4ODQzMzky.YCKjKw.52-rt_tB5bEAiZ5aRenQgguYPmY')