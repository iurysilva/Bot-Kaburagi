import sqlite3
import os
from discord.embeds import Embed
import string
from funcionalidades.funcionalidade_lembretes import retorna_dia_da_semana
from servicos.repositorio import Lembretes


class Lembrete:

    def __init__(self, banco):

        self.nome_dos_bancos = []
        self.repositorio = Lembretes(banco)
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
        self.repositorio.seta_banco(contexto.guild.id)
        if self.repositorio.adiciona(nome, dia, adicional):
            embed = Embed(title="Lembrete Inserido")
            embed.add_field(name=nome, value="Dia: %s\nInformação Adicional: %s" % (dia, adicional))
            return embed
        else:
            return Embed(title="Lembrete com esse nome já existe na lista")


    def remover_lembrete(self, contexto, nome):
        print('Função remover lembrete')
        self.repositorio.seta_banco(contexto.guild.id)
        if self.repositorio.remove_por_nome(nome):
            print('Dados removidos com sucesso\n')
            return True, "Lembrete para %s removido :)" % nome
        else:
            return False, "Lembrete com esse nome não existe na lista"


    def mostra_lembretes(self, contexto):
        print('Função mostra lembretes')
        self.repositorio.seta_banco(contexto.guild.id)
        embed = Embed(title="Lembretes")
        for dia in self.dias:
            for lembrete in self.repositorio.busca_por_dia(dia):
                print('exibindo lembrete: ', lembrete)
                embed.add_field(name=lembrete['nome'], value="Dia: %s\nInformação Adicional: %s" % (lembrete['dia'],
                                                                                               lembrete['adicional']),
                                inline=False)
        print()
        return True, embed



    def hoje(self, id):
        print('Função hoje')
        self.repositorio.seta_banco(id)
        dia_da_semana = retorna_dia_da_semana()
        embed = Embed(title="Lembretes de %s:" % dia_da_semana)
        lembretes = self.repositorio.busca_por_dia(dia_da_semana)
        vazio = True
        for lembrete in lembretes:
            vazio = False
            print('exibindo lembrete: ', lembrete)
            embed.add_field(name=lembrete['nome'], value="Informação Adicional: %s" % (lembrete['adicional']), inline=False)
        if not vazio:
            return True, embed
        else:
            embed.title = "Não há lembretes para %s" % dia_da_semana
            return False, embed

    def editar_informacao_adicional(self, contexto, nome, mensagem):
        print("Editando informação adicional de %s" % nome)
        print("Mensagem = %s\n" % mensagem)
        self.repositorio.seta_banco(contexto.guild.id)
        self.repositorio.edita_informacao_adicional(mensagem, nome)
        embed = Embed(title="Lembrete Atualizado")
        embed.add_field(name=nome, value="Informação Adicional: %s" % mensagem)
        return embed

    def editar_dia(self, contexto, nome, dia):
        print("Editando dia de %s" % nome)
        print("Dia = %s\n" % dia)
        if dia not in self.dias:
            return Embed(title="Dia inválido")
        self.repositorio.seta_banco(contexto.guild.id)
        self.repositorio.edita_dia(dia, nome)
        embed = Embed(title="Lembrete Atualizado")
        embed.add_field(name=nome, value="Dia: %s" % dia)
        return embed

    def verifica_se_nome_existe(self, contexto, nome):

        self.repositorio.seta_banco(contexto.guild.id)
        if not self.repositorio.busca_por_nome(nome):
            return False
        else:
            return True
