from funcionalidades.funcionalidade_lembretes.manipulacao_de_embed import adiciona_info
from discord.embeds import Embed
from servicos import Bancos_De_Dados


class Lembrete(Bancos_De_Dados):
    def __init__(self):
        caminho = 'funcionalidades/funcionalidade_lembretes/bancos'
        super().__init__(caminho)
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

    def listar_dados_por_atributo(self, atributo, cursor, embed, atributo_especifico):
        cursor.execute("SELECT * FROM Lembretes WHERE Dia=?", (atributo,))
        lembretes_dia = cursor.fetchall()
        numero_lembretes = len(lembretes_dia)

        if lembretes_dia:
            if atributo_especifico:
                embed.description = 'Há {} lembrete(s)'.format(numero_lembretes)
            else:
                embed = embed.add_field(name=atributo, value='Há {} lembrete(s)'.format(numero_lembretes), inline=False)

        for lembrete in lembretes_dia:
            descricao = "*Informação: %s*" % (lembrete[2])
            embed.add_field(name=lembrete[0], value=descricao, inline=True)
        return embed

    def mostra_dados(self, nome_do_banco, dia=None, autor=None):
        print('Função mostra lembretes')
        banco_existe = super().verifica_banco(nome_do_banco)
        dia_especifico = False
        if banco_existe:
            banco = super().acessar_banco(nome_do_banco)
            cursor = banco.cursor()
            if dia:
                dia_especifico = True
                embed = Embed(title="Lembretes de **{}**".format(dia))
                embed = self.listar_dados_por_atributo(dia, cursor, embed, dia_especifico)
                if not embed.fields:
                    embed = Embed(title="Não há lembretes para **%s**" % dia)
                    embed = adiciona_info(embed, autor)
                    return embed
            else:
                embed = Embed(title="**Lembretes**")
                for dia in self.dias:
                    embed = self.listar_dados_por_atributo(dia, cursor, embed, dia_especifico)
                print(embed)
                if not embed.fields:
                    embed = Embed(title="Não há lembretes neste servidor")
                    embed = adiciona_info(embed, autor)
                    return embed
            print("Mostra lembretes finalizada\n")
            embed = adiciona_info(embed, autor)
            return embed
        else:
            print("Mostrar_lembretes finalizada\n")
            embed = Embed(title="Este servidor não possui lembretes")
            embed = adiciona_info(embed, autor)
            return embed

    def insere_dados(self, nome_do_banco, *args):
        nome = args[0]
        dia = args[1]
        adicional = args[2]
        autor = args[3]
        print('Função adicionar lembrete')
        banco_existe = super().verifica_banco(nome_do_banco)
        banco = super().acessar_banco(nome_do_banco)
        cursor = banco.cursor()
        if not banco_existe:
            print('Banco %s não existe, criando banco e inserindo...\n' % nome_do_banco)
            cursor.execute("CREATE TABLE Lembretes (Nome text, Dia text, Adicional text)")
            cursor.execute("INSERT INTO Lembretes VALUES(?, ?, ?)", (nome, dia, adicional))
        else:
            print('Banco %s existe, inserindo...\n' % nome_do_banco)
            if super().verifica_se_atributo_ja_existe(nome_do_banco, nome):
                embed = Embed(title="Lembrete com esse nome já existe na lista :(")
                embed = adiciona_info(embed)
                return embed
            cursor.execute("INSERT INTO Lembretes VALUES(?, ?, ?)", (nome, dia, adicional))
        banco.commit()
        embed = Embed(title="Lembrete Inserido")
        embed = adiciona_info(embed, autor)
        embed.add_field(name=nome, value="Dia: %s\nInformação Adicional: %s" % (dia, adicional))
        return embed

    def remove_dados(self, nome_do_banco, *args):
        nome = args[0]
        autor = args[1]
        print('Função remover lembrete')
        banco_existe = super().verifica_banco(nome_do_banco)
        if banco_existe:
            banco = super().acessar_banco(nome_do_banco)
            cursor = banco.cursor()
            if not self.verifica_se_atributo_ja_existe(nome_do_banco, nome):
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

    def editar_atributo(self, nome_do_servidor, atributo, *args):
        nome = args[0]
        mensagem = args[1]
        autor = args[2]
        print("Editando %s de %s" % (atributo, nome))
        print("Mensagem = %s\n" % mensagem)
        banco_existe = super().verifica_banco(nome_do_servidor)
        if banco_existe:
            if not self.verifica_se_atributo_ja_existe(nome_do_servidor, nome):
                embed = Embed(title="Lembrete com esse nome não existe na lista")
                embed = adiciona_info(embed, autor)
                return embed
            banco = super().acessar_banco(nome_do_servidor)
            cursor = banco.cursor()
            cursor.execute("UPDATE Lembretes SET %s = ? WHERE Nome = ?" % (atributo), (mensagem, nome))
            banco.commit()
            embed = Embed(title="Lembrete Atualizado")
            embed = adiciona_info(embed, autor)
            embed.add_field(name=nome, value="%s: %s" % (atributo, mensagem))
            return embed
        else:
            embed = Embed(title="Este servidor não possui lembretes")
            embed = adiciona_info(embed, autor)
            return embed

    def verifica_se_atributo_ja_existe(self, nome_do_servidor, atributo):
        banco = self.acessar_banco(nome_do_servidor)
        cursor = banco.cursor()
        cursor.execute("SELECT * FROM Lembretes WHERE Nome=?", (atributo,))
        if not cursor.fetchall():
            print("Lembrete com nome %s não existe no banco" % atributo)
            return False
        else:
            print("Lembrete com nome %s existe no banco" % atributo)
            return True
