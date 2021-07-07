from mal import *
from discord import Embed
from servicos.manipulacao_de_embed import adiciona_info


class Anime():
    def __init__(self, titulo, tipo, nota, episodios, sinopse, imagem):
        self.titulo = titulo
        self.tipo = tipo
        self.nota = nota
        self.sinopse = sinopse
        self.episodios = episodios
        self.imagem = imagem


class Animes():
    def __init__(self):
        self.comandos = [["/kprocura (Nome)", "Mostra as informações do anime especificado"]]

    def ajuda(self):
        embed = Embed(title="Lista de Comandos:")
        comandos = self.comandos
        for comando in comandos:
            embed.add_field(name=comando[0], value=comando[1], inline=False)

        return embed

    def retorna_anime(self, nome):
        pesquisa = AnimeSearch(nome)
        resultado = pesquisa.results[0]
        return Anime(resultado.title, resultado.type, resultado.score, resultado.episodes, resultado.synopsis,
                     resultado.image_url)

    def procura(self, nome, autor):
        anime = self.retorna_anime(nome)
        mensagem = Embed(title=anime.titulo)
        mensagem.set_image(url=anime.imagem)
        mensagem.add_field(name="Nota", value=str(anime.nota))
        mensagem.add_field(name="Episódios", value=str(anime.episodios))
        mensagem.add_field(name="Tipo", value=str(anime.tipo))
        mensagem.add_field(name="Sinopse", value=str(anime.sinopse))
        mensagem = adiciona_info(mensagem, autor=autor)
        return mensagem
