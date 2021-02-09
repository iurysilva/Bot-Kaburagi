import discord
from funcoes import informar_anime_do_dia
import pandas as pd


bd_animes = pd.read_csv('banco_animes/bd_animes.csv', header=None)
cargo = 'everyone'
bd_animes = bd_animes.set_index(0)


cliente = discord.Client()


@cliente.event
async def on_message(mensagem):
    if mensagem.channel.id == 744388439113334899:
        if mensagem.content[0] == '?' and mensagem.content.find('animezada') != -1:
            await mensagem.channel.send(informar_anime_do_dia(bd_animes, cargo))


cliente.run('ODA4NzEzNTMzMzk4ODQzMzky.YCKjKw.7C4wyiDy5E0HFQc_X6qA6rlmtew')
