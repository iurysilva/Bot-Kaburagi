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
        await servidor.canal.send("Kaburagi iniciado!\n\n")

    if mensagem.channel.id == servidor.canal.id:
        comando = interpreta_mensagem(mensagem.content)
        if not comando:
            pass
        elif comando == "ajuda":
            await mensagem.channel.send(embed=kaburagi.ajuda())
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
        elif comando == "assistido":
            confirmacao, reporte = kaburagi.modificar_episodio(mensagem.content)
            if confirmacao:
                await mensagem.channel.send("%s teve seu episódio atual modificado" % reporte)
            elif not confirmacao:
                await mensagem.channel.send(reporte)
        elif comando == "hoje":
            await mensagem.channel.send(mensagem.author.mention)
            await mensagem.channel.send(embed=kaburagi.informar_anime_do_dia())
        elif comando == "animes":
            await mensagem.channel.send(embed=kaburagi.mostrar_animes())


@cliente.event
async def avisa_animezada():
    global kaburagi, servidor, bot_ativo
    avisar = True
    while True:
        if (retorna_hora() == '20:00' or retorna_hora() == '22:30') and avisar:
            avisar = False
            await servidor.canal.send(servidor.cargo.mention)
            await servidor.canal.send(embed=kaburagi.informar_anime_do_dia())
        if retorna_hora() == '20:01' or retorna_hora() == "22:31":
            avisar = True
        await asyncio.sleep(1)


cliente.loop.create_task(avisa_animezada())
teste = 'ODA5MTkyNzQxNTg1NTUxNDEw.YCRhdw.i0vRre5B8mps9e96OheLxGT5yjI'
bot = open('token.txt','r').read()
cliente.run('ODA5MTkyNzQxNTg1NTUxNDEw.YCRhdw.i0vRre5B8mps9e96OheLxGT5yjI')
