import discord
import pandas as pd
from objetos import Kaburagi
from objetos.servidores import *
from funcoes import retorna_hora
from funcoes import cria_banco_de_dados
import asyncio


cliente = discord.Client()

bd_animes = cria_banco_de_dados()
print(bd_animes)
servidor = None
kaburagi = None


@cliente.event
async def on_ready():
    global servidor, kaburagi
    servidor = Bar_dos_Cornos(cliente)
    kaburagi = Kaburagi(cliente, servidor, bd_animes)
    await asyncio.sleep(1)


@cliente.event
async def on_message(mensagem):
    global kaburagi, servidor
    if mensagem.channel.id == servidor.canal.id:
        if mensagem.content[0] == '?' and mensagem.content.find('animezada') != -1:
            await mensagem.channel.send(kaburagi.informar_anime_do_dia())


@cliente.event
async def avisa_animezada():
    global kaburagi, servidor
    while True:
        if retorna_hora() == '14:00':
            await servidor.canal.send(kaburagi.informar_anime_do_dia())
            return 0
        await asyncio.sleep(1)

cliente.loop.create_task(avisa_animezada())
cliente.run('ODA4NzEzNTMzMzk4ODQzMzky.YCKjKw.7C4wyiDy5E0HFQc_X6qA6rlmtew')
