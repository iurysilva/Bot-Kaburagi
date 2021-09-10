from servicos import Bancos_De_Dados
from tmdbv3api import Movie
from tmdbv3api import TMDb
from discord.embeds import Embed
from servicos import traduzir_do_ingles
import os


class Filmes():
    def __init__(self):
        self.chave_api = open('funcionalidades/funcionalidade_filmes/api_key.txt').read()
        self.tmdb = TMDb()
        self.tmdb.api_key = self.chave_api
        self.caminho = 'funcionalidades/funcionalidade_filmes/bancos'
        self.tabela = "Pool"
        self.banco_de_dados = Bancos_De_Dados(self.caminho)
        self.comandos = [["/kfilme_procura (nome)", "Mostra as informações do filme especificado"],
                         ["/kfilme_pool_adicionar (nome)", "Adiciona um filme na pool"],
                         ["/kfilme_pool_remover (nome)", "remove um filme da pool"],
                         ["/kfilme_pool_limpar", "Remove todos os filme da pool"],
                         ["/kfilme_pool", "Visualiza todos os filmes na pool"]]
        self.emojis = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮', '🇯', '🇰', '🇱', '🇲', '🇳', '🇴', '🇵',
                       '🇶', '🇷', '🇸', '🇹', '🇺', '🇻', '🇼', '🇽', '🇾', '🇿']

    def ajuda(self):
        print("\nFunção Ajuda\n")
        embed = Embed(title="Lista de Comandos:")
        comandos = self.comandos
        for comando in comandos:
            embed.add_field(name=comando[0], value=comando[1], inline=False)

        return embed

    def retorna_filme(self, nome):
        print("Função retorna anime para: ", nome)
        movie = Movie()
        pesquisa = movie.search(nome)
        if pesquisa:
            for filme in pesquisa:
                if filme['original_title'] == nome or filme['title'] == nome:
                    return filme
            filme = pesquisa[0]
            return filme
        else:
            return False

    def procura(self, nome):
        print("\nFunção procura para o filme: ", nome)
        filme = self.retorna_filme(nome)
        if filme is not False:
            mensagem = Embed(title=filme['title'])
            if filme['poster_path'] is not None:
                mensagem.set_image(url='https://image.tmdb.org/t/p/original/' + filme['poster_path'])
            mensagem.add_field(name="Nota", value=str(filme['vote_average']))
            mensagem.add_field(name="Número de Votos", value=str(filme['vote_count']))
            mensagem.add_field(name="Lançamento", value=str(filme['release_date']))
            mensagem.add_field(name="Sinopse", value=traduzir_do_ingles(str(filme['overview']))[0:1020] + "...")
            return mensagem
        else:
            return Embed(title="Filme não encontrado")

    def adicionar_filme_na_pool(self, reaction, user, nome, nome_do_servidor):
        print("\nFunção adicionar filme na pool, reação: ", reaction)
        if self.banco_de_dados.retornar_numero_de_linhas(nome_do_servidor, self.tabela) >= 26:
            return Embed(title="Número máximo de filmes na pool alcançado: 26")
        if reaction.emoji == "✅":
            resultado = self.banco_de_dados.insere_dados(nome_do_servidor, self.tabela,
                                                         {"Nome": nome, "Usuário": user.name}, "Nome")
            if resultado:
                print("Filme inserido\n")
                return Embed(title="O filme %s foi inserido na pool" % nome)
        print("Filme não inserido\n")
        return Embed(title="Filme não adicionado na pool (Ação negada ou filme repetido)")

    def remover_filme_da_pool(self, nome_do_servidor, nome):
        print('\nFunção remover filme da pool')
        if not self.banco_de_dados.remove_dados(nome_do_servidor, self.tabela, nome, "Nome"):
            embed = Embed(title="Falha ao remover filme (nome não existe na lista?)")
            print("Falha ao remover filme\n")
            return embed
        embed = Embed(title="Filme %s removido da pool" % nome)
        print('Filme removido com sucesso\n')
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
            resultado = Embed(title="Pool de Filmes")
            for anime in range(numero_de_linhas):
                linha = self.banco_de_dados.retornar_linha(nome_do_servidor, self.tabela, anime)
                resultado.add_field(name="%s " % self.emojis[anime] + linha[0], value="Inserido por %s" % linha[1],
                                    inline=False)
            print("Visualiza pool finalizada")
            return resultado
        print("Visualiza pool finalizada")
        return Embed(title="Pool está atualmente vazia")
