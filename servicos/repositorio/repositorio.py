import pymongo

class Repositorio:

    def __init__(self, cliente : pymongo.MongoClient, tabela : str, campos : list):

        self.cliente = cliente
        self.nome_tabela = tabela
        self.tabela = cliente['kaburagi'][tabela]
        self.campos = campos

    def insere(self, dados : dict) -> str or False:

        if all(campo in dados.keys() for campo in self.campos):

            return self.tabela.insert_one(dados)

        else:

            return False

    def busca(self, pesquisa : dict = None, colunas=None):

        if colunas is None:
            colunas = {}
        if pesquisa is None:
            pesquisa = {}


        resultados = self.tabela.find(pesquisa, colunas)
        return [self.tabela.find_one(i) for i in resultados]

    def remove(self, filtro=None):

        if filtro is None:
            filtro = {}

        self.tabela.delete_one(filtro)

    def seta_banco(self, banco):

        self.tabela = self.cliente[str(banco)][self.nome_tabela]
