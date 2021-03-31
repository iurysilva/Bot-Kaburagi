import sqlite3
import os
from discord.embeds import Embed
import string
from funcionalidades.funcionalidade_lembretes import retorna_dia_da_semana


class Lembrete:
    def __init__(self):
        self.nome_dos_bancos = []
        self.caminho = 'funcionalidades/funcionalidade_lembretes/bancos'
        self.dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
        self.comandos = [["/lembretes", "Lista todos os lembretes do servidor."],
                    ["/adicionar_lembrete (nome) (dia) (informação adicional)",
                     "Adiciona um lembrete"],
                    ["/remover_lembrete (nome)", "Remove um lembrete do servidor."],
                         ["/hoje", "Exibe os lembretes correspondentes ao dia atual."],
                         ["/editar_informacao_adicional (nome)",
                          "Edita as informações adicionais de um lembrete."],
                         ["/editar_dia (nome)", "Edita o dia de um lembrete."],
                         ["/mensagens_diarias",
                          "Informa os requisitos para implementar mensagens diarias no servidor."]]
        
    def ajuda(self):
        embed = Embed(title="Lista de Comandos:")
        comandos = self.comandos
        for comando in comandos:
            embed.add_field(name=comando[0], value=comando[1], inline=False)
        return embed

    def atualizar_lista_de_bancos(self):
        for arquivo in os.listdir(self.caminho):
            if arquivo != '__pycache__':
                self.nome_dos_bancos.append(arquivo)
        print('Servidores com lembretes: ', self.nome_dos_bancos, '\n')

    def verifica_banco(self, nome_do_servidor):
        servidor = nome_do_servidor
        print('Verificação de banco feita em: ', servidor)
        if servidor in self.nome_dos_bancos:
            print('banco %s existe\n' % servidor)
            return True, Embed(title="Este servidor possui lembretes")
        else:
            print('Banco %s não existe\n' % servidor)
            return False, Embed(title="Este servidor não possui lembretes")

    def interpreta_mensagem(self, mensagem):
        mensagem = list(mensagem)
        for palavra in range(len(mensagem)):
            mensagem[palavra] = string.capwords(mensagem[palavra])
        print("Interpretando mensagem: ", mensagem)
        achou_index = False
        index = None
        for dia in self.dias:
            for palavra in range(len(mensagem)):
                if dia == mensagem[palavra] and palavra != 0:
                    achou_index = True
                    index = palavra
                    break
        if achou_index:
            print('Dia encontrado na posição: ', index, '\n')
            return True, index
        else:
            print('Dia não encontrado na posição correta\n')
            return False, index

    def adicionar_lembrete(self, contexto, nome, dia, adicional="Nada"):
        print('Função adicionar lembrete')
        banco_existe, resultado = self.verifica_banco(contexto.guild.name)
        banco = sqlite3.connect(self.caminho + '/%s' % contexto.guild)
        cursor = banco.cursor()
        if not banco_existe:
            print('Banco %s não existe, criando banco e inserindo...\n' % contexto.guild)
            cursor.execute("CREATE TABLE Lembretes (Nome text, Dia text, Adicional text)")
            cursor.execute("INSERT INTO Lembretes VALUES(?, ?, ?)", (nome, dia, adicional))
            self.nome_dos_bancos.append(contexto.guild.name)
        else:
            print('Banco %s existe, inserindo...\n' % contexto.guild)
            if self.verifica_se_nome_existe(contexto, nome):
                return Embed(title="Lembrete com esse nome já existe na lista")
            cursor.execute("INSERT INTO Lembretes VALUES(?, ?, ?)", (nome, dia, adicional))
        banco.commit()
        embed = Embed(title="Lembrete Inserido")
        embed.add_field(name=nome, value="Dia: %s\nInformação Adicional: %s" % (dia, adicional))
        return embed

    def remover_lembrete(self, contexto, nome):
        print('Função remover lembrete')
        banco_existe, resultado = self.verifica_banco(contexto.guild.name)
        if banco_existe:
            banco = sqlite3.connect(self.caminho + '/%s' % contexto.guild)
            cursor = banco.cursor()
            if not self.verifica_se_nome_existe(contexto, nome):
                return False, "Lembrete com esse nome não existe na lista"
            cursor.execute('DELETE from Lembretes WHERE Nome = ?', (nome,))
            banco.commit()
            print('Dados removidos com sucesso\n')
            return True, "Lembrete para %s removido :)" % nome
        else:
            print('Banco %s não existe\n')
            return False, resultado

    def mostra_lembretes(self, contexto):
        print('Função mostra lembretes')
        banco_existe, resultado = self.verifica_banco(contexto.guild.name)
        if banco_existe:
            embed = Embed(title="Lembretes")
            banco = sqlite3.connect(self.caminho + '/%s' % contexto.guild)
            cursor = banco.cursor()
            for dia in self.dias:
                cursor.execute("SELECT * FROM Lembretes WHERE Dia=?", (dia,))
                for lembrete in cursor.fetchall():
                    print('exibindo lembrete: ', lembrete)
                    embed.add_field(name=lembrete[0], value="Dia: %s\nInformação Adicional: %s" % (lembrete[1],
                    lembrete[2]), inline=False)
            print('')
            return True, embed
        else:
            return False, resultado

    def hoje(self, nome_do_servidor):
        print('Função hoje')
        banco_existe, resultado = self.verifica_banco(nome_do_servidor)
        if banco_existe:
            dia_da_semana = retorna_dia_da_semana()
            embed = Embed(title="Lembretes de %s:" % dia_da_semana)
            banco = sqlite3.connect(self.caminho + '/%s' % nome_do_servidor)
            cursor = banco.cursor()
            cursor.execute("SELECT * FROM Lembretes WHERE Dia=?", (dia_da_semana,))
            vazio = True
            for lembrete in cursor.fetchall():
                vazio = False
                print('exibindo lembrete: ', lembrete)
                embed.add_field(name=lembrete[0], value="Informação Adicional: %s" % (lembrete[2]), inline=False)
            if not vazio:
                return True, embed
            else:
                embed.title = "Não há lembretes para %s" % dia_da_semana
                return False, embed
        else:
            return False, resultado

    def editar_informacao_adicional(self, contexto, nome, mensagem):
        print("Editando informação adicional de %s" % nome)
        print("Mensagem = %s\n" % mensagem)
        banco = sqlite3.connect(self.caminho + '/%s' % contexto.guild)
        cursor = banco.cursor()
        cursor.execute("UPDATE Lembretes SET Adicional = (?) WHERE Nome = (?)", (mensagem, nome))
        banco.commit()
        embed = Embed(title="Lembrete Atualizado")
        embed.add_field(name=nome, value="Informação Adicional: %s" % mensagem)
        return embed

    def editar_dia(self, contexto, nome, dia):
        print("Editando dia de %s" % nome)
        print("Dia = %s\n" % dia)
        if dia not in self.dias:
            return Embed(title="Dia inválido")
        banco = sqlite3.connect(self.caminho + '/%s' % contexto.guild)
        cursor = banco.cursor()
        cursor.execute("UPDATE Lembretes SET Dia = (?) WHERE Nome = (?)", (dia, nome))
        banco.commit()
        embed = Embed(title="Lembrete Atualizado")
        embed.add_field(name=nome, value="Dia: %s" % dia)
        return embed

    def verifica_se_nome_existe(self, contexto, nome):
        banco = sqlite3.connect(self.caminho + '/%s' % contexto.guild)
        cursor = banco.cursor()
        cursor.execute("SELECT * FROM Lembretes WHERE Nome=?", (nome,))
        if not cursor.fetchall():
            return False
        else:
            return True
