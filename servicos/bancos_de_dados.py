import pandas as pd
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
        if nome_do_servidor in nome_dos_bancos:
            print('Banco %s existe' % nome_do_servidor)
            return True
        else:
            print('Banco %s não existe' % nome_do_servidor)
            return False

    def listar_dados_por_atributo(self, atributo, cursor, embed, dia_especifico):
        pass

    def verifica_se_chave_ja_existe(self, nome_do_banco, tabela, chave, coluna_chave):
        print("Verificação de chave repetida")
        if self.verifica_banco(nome_do_banco):
            banco = self.acessar_banco(nome_do_banco)
            dataframe = pd.read_sql_query("select * from %s" % tabela, banco)
            if chave in dataframe[coluna_chave].values:
                print("Chave %s existe na tabela %s" % (chave, tabela))
                return True
        else:
            print("Verificação de chave repetida falhou, banco não existe")
        return False

    def mostra_dados(self, atributo, autor):
        pass

    def insere_dados(self, nome_do_banco, tabela, dados, coluna_chave):
        if self.verifica_banco(nome_do_banco):
            banco = self.acessar_banco(nome_do_banco)
            dataframe = pd.read_sql_query("select * from %s" % tabela, banco)
            if self.verifica_se_chave_ja_existe(nome_do_banco, tabela, dados[coluna_chave], coluna_chave):
                return False
            dataframe = dataframe.append(dados, ignore_index=True)
        else:
            banco = self.acessar_banco(nome_do_banco)
            dataframe = pd.DataFrame.from_records([dados])
        dataframe.to_sql(tabela, banco, if_exists="replace", index=False)
        return True

    def remove_dados(self, nome_do_banco, tabela, chave, coluna_chave):
        if self.verifica_banco(nome_do_banco):
            if self.verifica_se_chave_ja_existe(nome_do_banco, tabela, chave, coluna_chave):
                banco = self.acessar_banco(nome_do_banco)
                dataframe = pd.read_sql_query("select * from %s" % tabela, banco)
                index_linha = dataframe[coluna_chave][dataframe[coluna_chave] == chave].index[0]
                dataframe = dataframe.drop(index_linha)
                dataframe.to_sql(tabela, banco, if_exists="replace", index=False)
                return True
        return False

    def edita_dados(self, nome_do_banco, tabela, coluna, dado, chave, coluna_chave):
        print(coluna, dado, chave, coluna_chave)
        if self.verifica_banco(nome_do_banco):
            if self.verifica_se_chave_ja_existe(nome_do_banco, tabela, chave, coluna_chave):
                banco = self.acessar_banco(nome_do_banco)
                dataframe = pd.read_sql_query("select * from %s" % tabela, banco)
                index_linha = dataframe[coluna_chave][dataframe[coluna_chave] == chave].index[0]
                dataframe[coluna][index_linha] = dado
                dataframe.to_sql(tabela, banco, if_exists="replace", index=False)
                return True
        return False

    def retornar_numero_de_linhas(self, nome_do_banco, tabela):
        if self.verifica_banco(nome_do_banco):
            banco = self.acessar_banco(nome_do_banco)
            dataframe = pd.read_sql_query("select * from %s" % tabela, banco)
            return len(dataframe)
        return 0

    def retornar_linha(self, nome_do_banco, tabela, linha):
        if self.verifica_banco(nome_do_banco):
            banco = self.acessar_banco(nome_do_banco)
            dataframe = pd.read_sql_query("select * from %s" % tabela, banco)
            return dataframe.loc[linha]
        return False
