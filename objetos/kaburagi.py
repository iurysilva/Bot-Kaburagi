from discord.embeds import Embed
from funcoes import informar_dia_da_semana
from funcoes import condicoes_adicionar_anime
from funcoes import condicoes_remover_anime
from funcoes import condicoes_incrementar_episodio
from funcoes import retorna_comandos
import discord
import string

import pandas as pd
import numpy as np


class Kaburagi:
    def __init__(self, cliente, servidor, banco_animes):
        self.cliente = cliente
        self.servidor = servidor
        self.banco_animes = banco_animes


    def ajuda(self):
        embed = discord.Embed(title="Lista de Comandos:")
        comandos = retorna_comandos()
        for comando in comandos:
            embed.add_field(name=comando[0], value=comando[1], inline=False)   
        return embed 
        
        
    def informar_anime_do_dia(self):
        animes_do_dia = []
        episodios = []
        dia_de_hoje = informar_dia_da_semana()
        for _,anime in self.banco_animes.iterrows():
            atributo_dia = anime[1]
            if atributo_dia.lower() == dia_de_hoje.lower():
                animes_do_dia.append(anime[0])
                episodios.append(anime[2])
        if not animes_do_dia:
            return discord.Embed(title="Hoje não tem animezada :(")
        else:
            saida = discord.Embed(title="Hoje tem:")
            for anime in range(0, len(animes_do_dia)):
                saida.add_field(name=animes_do_dia[anime], value="Episódio %s" %episodios[anime], inline=False) 
            return saida

    def adiciona_anime(self, mensagem):
        mensagem = string.capwords(mensagem)
        validacao_de_mensagem = condicoes_adicionar_anime(mensagem)
        if validacao_de_mensagem != "válida":
            return False, validacao_de_mensagem
        else:
            mensagem_separada = mensagem.split(' ')
            anime = ''
            for palavra in range(1, len(mensagem_separada)-1):
                if palavra == 1:
                    anime += '%s' % mensagem_separada[palavra]
                else:
                    anime += ' %s' % mensagem_separada[palavra]
            dia = mensagem.split(' ')[-1]
            anime_e_dia = pd.DataFrame(np.array([[anime, dia, 0]]),
                                                columns=['anime','dia','episodio'])
            self.banco_animes = pd.concat([self.banco_animes, anime_e_dia], ignore_index=True, axis=0)
            self.banco_animes.to_csv('banco_animes/bd_animes.csv', index=False, header=False)
            print(self.banco_animes)
            return True, anime

    def remover_anime(self, mensagem):
        validacao_de_mensagem = condicoes_remover_anime(mensagem)
        if validacao_de_mensagem != "válida":
            return False, validacao_de_mensagem
        else:
            mensagem_separada = mensagem.split(' ')
            anime_escolhido = ''
            for palavra in range(1, len(mensagem_separada)):
                if palavra == 1:
                    anime_escolhido += '%s' % mensagem_separada[palavra]
                else:
                    anime_escolhido += ' %s' % mensagem_separada[palavra]
            for index,anime in self.banco_animes.iterrows():
                if anime_escolhido.lower() == anime[0].lower():
                    self.banco_animes = self.banco_animes.drop([index])
                    self.banco_animes.to_csv('banco_animes/bd_animes.csv', index=False, header=False)
                    print(self.banco_animes)
                    return True, anime_escolhido
            return False, "Anime não encontrado e não removido"

    def modificar_episodio(self, mensagem):
        validacao_de_mensagem = condicoes_incrementar_episodio(mensagem)
        if validacao_de_mensagem != "válida":
            return False, validacao_de_mensagem
        else:
            mensagem_separada = mensagem.split(' ')
            anime_escolhido = ''
            for palavra in range(1, len(mensagem_separada)-1):
                if palavra == 1:
                    anime_escolhido += '%s' % mensagem_separada[palavra]
                else:
                    anime_escolhido += ' %s' % mensagem_separada[palavra]
            for index,anime in self.banco_animes.iterrows():
                if anime_escolhido.lower() == anime[0].lower():
                    novo_num_episodios = mensagem_separada[-1]
                    self.banco_animes.loc[index, "episodio"] = novo_num_episodios
                    self.banco_animes.to_csv('banco_animes/bd_animes.csv', index=True, header=False)
                    print(self.banco_animes)
                    return True, anime_escolhido
            return False, "Anime não encontrado e não incrementado"

    def mostrar_animes(self):
        embed = discord.Embed(title="Animes sendo vistos atualmente:")
        for _,anime in self.banco_animes.iterrows():
            embed.add_field(name=anime[0], value='Dia: %s\nEpisódio: %s' % (anime[1],anime[2]), inline=False)
        return embed
