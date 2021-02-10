import discord
import pandas as pd
from objetos import Kaburagi
from objetos.servidores import *
from funcoes import retorna_hora
from funcoes import cria_banco_de_dados
from funcoes import interpreta_mensagem
import asyncio


servidor = Teste


cliente = discord.Client()
bot_ativo = False
bd_animes = cria_banco_de_dados()
kaburagi = None


@cliente.event
async def on_message(mensagem):
    global kaburagi, servidor, bot_ativo
    if not bot_ativo:
        servidor = servidor(cliente)
        kaburagi = Kaburagi(cliente, servidor, bd_animes)
        bot_ativo = True
        await servidor.canal.send("Bot iniciado!")

    if mensagem.channel.id == servidor.canal.id:
        comando = interpreta_mensagem(mensagem.content)
        if not comando:
            pass
        elif comando == "adicionar":
            confirmacao, reporte = kaburagi.adiciona_anime(mensagem.content)
            if confirmacao:
                await mensagem.channel.send("%s adicionado à lista" % reporte)
            elif not confirmacao:
                await mensagem.channel.send(reporte)
        elif comando == "remover":
            confirmacao, reporte = kaburagi.remover_anime(mensagem.content)
            if confirmacao:
                await mensagem.channel.send("%s removido da lista" % reporte)
            elif not confirmacao:
                await mensagem.channel.send(reporte)
        elif comando == "animes":
            await mensagem.channel.send(kaburagi.mostrar_animes())

'''
@cliente.event
async def avisa_animezada():
    global kaburagi, servidor
    while True:
        if retorna_hora() == '14:00':
            await servidor.canal.send(kaburagi.informar_anime_do_dia())
            return 0
        await asyncio.sleep(1)
'''

# cliente.loop.create_task(avisa_animezada())
cliente.run('ODA4NzEzNTMzMzk4ODQzMzky.YCKjKw.kiOqb-Mud_Ji3Bk-sfU8GIUlR4U')
