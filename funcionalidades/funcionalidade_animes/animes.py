from mal import *
from discord import Embed
from servicos.manipulacao_de_embed import adiciona_info


class Animes():
    def __init__(self):
        self.comandos = [["/kprocura (nome)", "Mostra as informações do anime especificado"],
                         ["/kprocura_detalhada (nome)", "Exibe informações mais detalhadas, porém demora mais"]]

    def ajuda(self):
        embed = Embed(title="Lista de Comandos:")
        comandos = self.comandos
        for comando in comandos:
            embed.add_field(name=comando[0], value=comando[1], inline=False)

        return embed

    def retorna_anime(self, nome):
        pesquisa = AnimeSearch(nome)
        anime = pesquisa.results[0]
        return anime

    def retorna_anime_detalhado(self, nome):
        pesquisa = AnimeSearch(nome)
        id_do_anime = pesquisa.results[0].mal_id
        anime = Anime(id_do_anime)
        return anime

    def procura(self, nome, autor):
        anime = self.retorna_anime(nome)
        mensagem = Embed(title=anime.title)
        mensagem.set_image(url=anime.image_url)
        mensagem.add_field(name="Nota", value=str(anime.score))
        mensagem.add_field(name="Episódios", value=str(anime.episodes))
        mensagem.add_field(name="Tipo", value=str(anime.type))
        mensagem.add_field(name="Sinopse", value=str(anime.synopsis))
        mensagem = adiciona_info(mensagem, autor=autor)
        return mensagem

    def procura_detalhada(self, nome, autor):
        anime = self.retorna_anime_detalhado(nome)
        mensagem = Embed(title=anime.title)
        mensagem.set_image(url=anime.image_url)
        mensagem.add_field(name="Nota", value=str(anime.score))
        mensagem.add_field(name="Episódios", value=str(anime.episodes))
        mensagem.add_field(name="Estúdio", value=str(anime.studios[0]))
        mensagem.add_field(name="Status", value=str(anime.status))
        mensagem.add_field(name="Lançamento", value=str(anime.aired))
        mensagem.add_field(name="Gêneros", value=str(', '.join(anime.genres)))
        mensagem.add_field(name="Sinopse", value=str(anime.synopsis)[0:1020])
        mensagem = adiciona_info(mensagem, autor=autor)
        return mensagem
