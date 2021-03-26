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
        self.comandos = [["?lembretes", "Lista todos os lembretes do servidor."],
                    ["?adicionar_lembrete (nome) (dia) (informação adicional)",
                     "Adiciona um lembrete, abreviação do comando: ?al."],
                    ["?remover_lembrete (nome)", "Remove um lembrete do servidor, abreviação do comando: ?rl."],
                         ["?hoje", "Exibe os lembretes correspondentes ao dia atual."]]

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

    def verifica_banco(self, contexto):
        servidor = contexto.guild.name
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
            if dia in mensagem:
                index = mensagem.index(dia)
        if not achou_index:
            print('Dia encontrado na posição: ', index, '\n')
            return True, index
        else:
            print('Dia não encontrado\n')
            return False, index

    def adicionar_lembrete(self, contexto, nome, dia, adicional="Nada"):
        print('Função adicionar lembrete')
        banco_existe, resultado = self.verifica_banco(contexto)
        banco = sqlite3.connect(self.caminho + '/%s' % contexto.guild)
        cursor = banco.cursor()
        if not banco_existe:
            print('Banco %s não existe, criando banco e inserindo...\n' % contexto.guild)
            cursor.execute("CREATE TABLE Lembretes (Nome text, Dia text, Adicional text)")
            cursor.execute("INSERT INTO Lembretes VALUES(?, ?, ?)", (nome, dia, adicional))
        else:
            print('Banco %s existe, inserindo...\n' % contexto.guild)
            cursor.execute("INSERT INTO Lembretes VALUES(?, ?, ?)", (nome, dia, adicional))
        banco.commit()
        embed = Embed(title="Lembrete Inserido")
        embed.add_field(name=nome, value="Dia: %s\nInformação Adicional: %s" % (dia, adicional))
        self.nome_dos_bancos.append(contexto.guild.name)
        return embed

    def remover_lembrete(self, contexto, nome):
        print('Função remover lembrete')
        banco_existe, resultado = self.verifica_banco(contexto)
        if banco_existe:
            banco = sqlite3.connect(self.caminho + '/%s' % contexto.guild)
            cursor = banco.cursor()
            cursor.execute('DELETE from Lembretes WHERE Nome = ?', (nome,))
            banco.commit()
            print('Dados removidos com sucesso\n')
            return True, "Lembrete para %s removido :)" % nome
        else:
            print('Banco %s não existe\n')
            return False, resultado

    def mostra_lembretes(self, contexto):
        print('Função mostra lembretes')
        banco_existe, resultado = self.verifica_banco(contexto)
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
            return True, embed
        else:
            return False, resultado

    def hoje(self, contexto):
        print('Função hoje')
        banco_existe, resultado = self.verifica_banco(contexto)
        if banco_existe:
            dia_da_semana = retorna_dia_da_semana()
            embed = Embed(title="Lembretes de %s:" % dia_da_semana)
            banco = sqlite3.connect(self.caminho + '/%s' % contexto.guild)
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