from abc import ABC, abstractmethod
import os
import sqlite3


class Bancos_De_Dados:
    def __init__(self, caminho):
        self.caminho = caminho

    def acessar_banco(self, nome_do_servidor):
        banco = sqlite3.connect(self.caminho + '/%s' % nome_do_servidor)
        return banco

    def verifica_banco(self, nome_do_servidor):
        print('Verificação de banco feita em: ', nome_do_servidor)
        nome_dos_bancos = []
        for arquivo in os.listdir(self.caminho):
            if arquivo != '__pycache__':
                nome_dos_bancos.append(arquivo)
        print('Servidores com lembretes: ', nome_dos_bancos)
        if nome_do_servidor in nome_dos_bancos:
            print('Banco %s existe' % nome_do_servidor)
            return True
        else:
            print('Banco %s não existe' % nome_do_servidor)
            return False

    @abstractmethod
    def listar_dados_por_atributo(self, atributo, cursor, embed, dia_especifico):
        pass

    @abstractmethod
    def verifica_se_atributo_ja_existe(self, nome_do_servidor, atributo):
        pass

    @abstractmethod
    def mostra_dados(self, atributo, autor):
        pass

    @abstractmethod
    def insere_dados(self, nome_do_banco, *args):
        pass

    @abstractmethod
    def remove_dados(self, nome_do_banco, *args):
        pass

    @abstractmethod
    def editar_atributo(self, nome_do_banco, atributo, *args):
        pass