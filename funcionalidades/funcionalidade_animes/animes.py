from mal import *
from discord import Embed
import os
from servicos import traduzir_do_ingles
from servicos import Bancos_De_Dados


class Animes():
    def __init__(self):
        self.caminho = 'funcionalidades/funcionalidade_animes/bancos'
        self.tabela = "Pool"
        self.banco_de_dados = Bancos_De_Dados(self.caminho)
        self.comandos = [["/kprocura (nome)", "Mostra as informações do anime especificado"],
                         ["/kprocura_detalhada (nome)", "Exibe informações mais detalhadas, porém demora mais"],
                         ["/kanime_pool_adicionar (nome)", "Adiciona um anime na pool"],
                         ["/kanime_pool_remover (nome)", "remove um anime da pool"],
                         ["/kanime_pool_limpar", "Remove todos os animes da pool"],
                         ["/kanime_pool", "Visualiza todos os animes na pool"]]
        self.emojis = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮', '🇯', '🇰', '🇱', '🇲', '🇳', '🇴', '🇵',
                       '🇶', '🇷', '🇸', '🇹', '🇺', '🇻', '🇼', '🇽', '🇾', '🇿']

    def ajuda(self):
        print("\nFunção Ajuda\n")
        embed = Embed(title="Lista de Comandos:")
        comandos = self.comandos
        for comando in comandos:
            embed.add_field(name=comando[0], value=comando[1], inline=False)

        return embed

    def retorna_anime(self, nome):
        print("Função retorna anime para: ", nome)
        pesquisa = AnimeSearch(nome)
        anime = pesquisa.results[0]
        return anime

    def retorna_anime_detalhado(self, nome):
        print("Função retorna anime detalhada para: ", nome)
        pesquisa = AnimeSearch(nome)
        id_do_anime = pesquisa.results[0].mal_id
        anime = Anime(id_do_anime)
        return anime

    def procura(self, nome, autor):
        print("\nFunção procura para o anime: ", nome)
        anime = self.retorna_anime(nome)
        mensagem = Embed(title=anime.title)
        mensagem.set_image(url=anime.image_url)
        mensagem.add_field(name="Nota", value=str(anime.score))
        mensagem.add_field(name="Episódios", value=str(anime.episodes))
        mensagem.add_field(name="Tipo", value=str(anime.type))
        mensagem.add_field(name="Sinopse", value=str(traduzir_do_ingles(anime.synopsis)))
        return mensagem

    def procura_detalhada(self, nome, autor):
        print("\nFunção procura para o anime: ", nome)
        anime = self.retorna_anime_detalhado(nome)
        mensagem = Embed(title=anime.title)
        mensagem.set_image(url=anime.image_url)
        mensagem.add_field(name="Nota", value=str(anime.score))
        mensagem.add_field(name="Episódios", value=str(anime.episodes))
        mensagem.add_field(name="Estúdio", value=str(anime.studios[0]))
        mensagem.add_field(name="Status", value=str(traduzir_do_ingles(anime.status)))
        mensagem.add_field(name="Lançamento", value=str(traduzir_do_ingles(anime.aired)))
        mensagem.add_field(name="Gêneros", value=str(traduzir_do_ingles(', '.join(anime.genres))))
        mensagem.add_field(name="Sinopse", value=str(traduzir_do_ingles(anime.synopsis))[0:1020] + "...")
        return mensagem

    def adicionar_anime_na_pool(self, reaction, user, nome, nome_do_servidor):
        print("\nFunção adicionar anime na pool, reação: ", reaction)
        if self.banco_de_dados.retornar_numero_de_linhas(nome_do_servidor, self.tabela) >= 26:
            return Embed(title="Número máximo de animes na pool alcançado: 26")
        if reaction.emoji == "✅":
            resultado = self.banco_de_dados.insere_dados(nome_do_servidor, self.tabela,
                                                         {"Nome": nome, "Usuário": user.name}, "Nome")
            if resultado:
                print("Anime inserido\n")
                return Embed(title="O anime %s foi inserido na pool" % nome)
        print("Anime não inserido\n")
        return Embed(title="Anime não adicionado na pool (Ação negada ou anime repetido)")

    def remover_anime_da_pool(self, nome_do_servidor, nome):
        print('\nFunção remover anime da pool')
        if not self.banco_de_dados.remove_dados(nome_do_servidor, self.tabela, nome, "Nome"):
            embed = Embed(title="Falha ao remover anime (nome não existe na lista?)")
            print("Falha ao remover anime\n")
            return embed
        embed = Embed(title="Anime %s removido da pool" % nome)
        print('Anime removido com sucesso\n')
        return embed

    def limpa_pool(self, nome_do_servidor):
        print("\nFunção limpar pool")
        if '%s' % nome_do_servidor in os.listdir(self.caminho):
            print('Removendo pool %s\n' % nome_do_servidor)
            os.remove("%s/%s" % (self.caminho, nome_do_servidor))
            return Embed(title="A pool foi limpa")
        else:
            print("Pool não encontrada\n")
            return Embed(title="A pool já estava limpa")

    def visualizar_pool(self, nome_do_servidor):
        print("\nFunção visualizar pool")
        numero_de_linhas = self.banco_de_dados.retornar_numero_de_linhas(nome_do_servidor, self.tabela)
        print("Número de linhas: ", numero_de_linhas)
        if numero_de_linhas != 0:
            resultado = Embed(title="Pool de Animes")
            for anime in range(numero_de_linhas):
                linha = self.banco_de_dados.retornar_linha(nome_do_servidor, self.tabela, anime)
                resultado.add_field(name="%s " % self.emojis[anime] + linha[0], value="Inserido por %s" % linha[1],
                                    inline=False)
            print("Visualiza pool finalizada")
            return resultado
        print("Visualiza pool finalizada")
        return Embed(title="Pool está atualmente vazia")