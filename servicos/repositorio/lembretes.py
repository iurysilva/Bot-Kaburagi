from .repositorio import Repositorio
import pymongo

class Lembretes(Repositorio):

    def __init__(self, cliente : pymongo.MongoClient):

        campos = ['dia','nome','adicional']
        super().__init__(cliente, 'lembretes', campos)

    def busca_por_nome(self, nome : str):

        return  self.busca({'nome' : nome})

    def busca_por_dia(self, dia : str):

        return  self.busca({'dia' : dia})

    def adiciona(self, nome : str, dia : str, adicional : str):

        if self.busca_por_nome(nome): return False
        return self.insere({'nome':nome, 'dia':dia, 'adicional':adicional})

    def edita_informacao_adicional(self, adicional, nome):

        self.tabela.update_one({'nome':nome}, {'$set':{'adicional':adicional}})

    def edita_dia(self, dia, nome):

        self.tabela.update_one({'nome': nome}, {'$set':{'dia': dia}})

    def remove_por_nome(self, nome : str):

        if not self.busca_por_nome(nome): return False
        self.remove({'nome':nome})
        return True