from funcionalidades.funcionalidade_lembretes.manipulacao_de_embed import adiciona_info
from funcionalidades.funcionalidade_lembretes import listar_lembretes_por_dia
from funcionalidades.funcionalidade_lembretes import verifica_banco
from funcionalidades.funcionalidade_lembretes import acessar_banco
from funcionalidades.funcionalidade_lembretes import verifica_se_nome_ja_existe
from discord.embeds import Embed


class Lembrete:
    def __init__(self):
        self.dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
        self.comandos = [["/klembretes", "Lista todos os lembretes do servidor."],
                    ["/kadicionar_lembrete (nome) (dia) (informação adicional)",
                     "Adiciona um lembrete"],
                    ["/kremover_lembrete (nome)", "Remove um lembrete do servidor."],
                         ["/khoje", "Exibe os lembretes correspondentes ao dia atual."],
                         ["/keditar_informacao_adicional (nome)",
                          "Edita as informações adicionais de um lembrete."],
                         ["/keditar_dia (nome)", "Edita o dia de um lembrete."],
                         ["/kmensagens_diarias",
                          "Informa os requisitos para implementar mensagens diarias no servidor."]]
        
    def ajuda(self):
        embed = Embed(title="Lista de Comandos:")
        comandos = self.comandos
        for comando in comandos:
            embed.add_field(name=comando[0], value=comando[1], inline=False)
        
        return adiciona_info(embed)

    def mostra_lembretes(self, nome_do_servidor, dia=None, autor=None):
        print('Função mostra lembretes')
        banco_existe = verifica_banco(nome_do_servidor)
        dia_especifico = False
        if banco_existe:
            banco = acessar_banco(nome_do_servidor)
            cursor = banco.cursor()
            if dia:
                dia_especifico = True
                embed = Embed(title="Lembretes de **{}**".format(dia))
                embed = listar_lembretes_por_dia(dia, cursor, embed, dia_especifico)
                if not embed.fields:
                    embed = Embed(title="Não há lembretes para **%s**" % dia)
                    embed = adiciona_info(embed,autor)
                    return embed
            else:
                embed = Embed(title="**Lembretes**")
                for dia in self.dias:
                    embed = listar_lembretes_por_dia(dia, cursor, embed, dia_especifico)
                if not embed.fields:
                    embed = Embed(title="Não há lembretes neste servidor")
                    embed = adiciona_info(embed,autor)
                    return embed
            print("Mostra lembretes finalizada\n")
            embed = adiciona_info(embed,autor)
            return embed
        else:
            print("Mostrar_lembretes finalizada\n")
            embed = Embed(title="Este servidor não possui lembretes")
            embed = adiciona_info(embed,autor)
            return embed

    def adicionar_lembrete(self, nome_do_servidor, nome, dia, adicional="Nada", autor=None):
        print('Função adicionar lembrete')
        banco_existe = verifica_banco(nome_do_servidor)
        banco = acessar_banco(nome_do_servidor)
        cursor = banco.cursor()
        if not banco_existe:
            print('Banco %s não existe, criando banco e inserindo...\n' % nome_do_servidor)
            cursor.execute("CREATE TABLE Lembretes (Nome text, Dia text, Adicional text)")
            cursor.execute("INSERT INTO Lembretes VALUES(?, ?, ?)", (nome, dia, adicional))
        else:
            print('Banco %s existe, inserindo...\n' % nome_do_servidor)
            if verifica_se_nome_ja_existe(nome_do_servidor, nome):
                embed = Embed(title="Lembrete com esse nome já existe na lista :(")
                embed = adiciona_info(embed)
                return embed
            cursor.execute("INSERT INTO Lembretes VALUES(?, ?, ?)", (nome, dia, adicional))
        banco.commit()
        embed = Embed(title="Lembrete Inserido")
        embed = adiciona_info(embed, autor)
        embed.add_field(name=nome, value="Dia: %s\nInformação Adicional: %s" % (dia, adicional))
        return embed

    def remover_lembrete(self, nome_do_servidor, nome, autor=None):
        print('Função remover lembrete')
        banco_existe = verifica_banco(nome_do_servidor)
        if banco_existe:
            banco = acessar_banco(nome_do_servidor)
            cursor = banco.cursor()
            if not verifica_se_nome_ja_existe(nome_do_servidor, nome):
                embed = Embed(title="Lembrete com esse nome não existe na lista :(")
                embed = adiciona_info(embed, autor)
                return embed
            cursor.execute('DELETE from Lembretes WHERE Nome = ?', (nome,))
            banco.commit()
            print('Dados removidos com sucesso\n')
            embed = Embed(title="Lembrete para %s removido :)" % nome)
            embed = adiciona_info(embed, autor)
            return embed
        else:
            print('Banco %s não existe\n')
            embed = Embed(title="Este servidor não possui lembretes")
            embed = adiciona_info(embed)
            return embed
        

    def editar_informacao_adicional(self, nome_do_servidor, nome, adicional='mada', autor=None):
        print("Editando informação adicional de %s" % nome)
        print("Mensagem = %s\n" % adicional)
        banco_existe = verifica_banco(nome_do_servidor)
        if banco_existe:
            if not verifica_se_nome_ja_existe(nome_do_servidor, nome):
                embed = Embed(title="Lembrete com esse nome não existe na lista")
                embed = adiciona_info(embed, autor)
                return embed
            banco = acessar_banco(nome_do_servidor)
            cursor = banco.cursor()
            cursor.execute("UPDATE Lembretes SET Adicional = (?) WHERE Nome = (?)", (adicional, nome))
            banco.commit()
            embed = Embed(title="Lembrete Atualizado")
            embed = adiciona_info(embed, autor)
            embed.add_field(name=nome, value="Informação Adicional: %s" % adicional)
            return embed
        else:
            embed = Embed(title="Este servidor não possui lembretes")
            embed = adiciona_info(embed, autor)
            return embed

    def editar_dia(self, nome_do_servidor, nome, dia, autor=None):
        print("Editando dia de %s" % nome)
        print("Dia = %s\n" % dia)
        banco_existe = verifica_banco(nome_do_servidor)
        if banco_existe:
            if not verifica_se_nome_ja_existe(nome_do_servidor, nome):
                embed = Embed(title="Lembrete com esse nome não existe na lista :(")
                embed = adiciona_info(embed, autor)
                return embed
            banco = acessar_banco(nome_do_servidor)
            cursor = banco.cursor()
            cursor.execute("UPDATE Lembretes SET Dia = (?) WHERE Nome = (?)", (dia, nome))
            banco.commit()
            embed = Embed(title="Lembrete Atualizado :)")
            embed.add_field(name=nome, value="Dia: %s" % dia)
            embed = adiciona_info(embed, autor)
            return embed
        else:
            embed = Embed(title="Este servidor não possui lembretes")
            embed = adiciona_info(embed, autor)
            return embed
