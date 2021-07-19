from discord.embeds import Embed
from servicos import Bancos_De_Dados
from servicos.informacoes_sobre_tempo import retorna_hora, retorna_dia_da_semana


class Lembrete():
    def __init__(self):
        self.caminho = 'funcionalidades/funcionalidade_lembretes/bancos'
        self.tabela = "Lembretes"
        self.banco_de_dados = Bancos_De_Dados(self.caminho)
        self.dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
        self.comandos = [["/klembretes (Dia: opcional)", "Lista todos os lembretes do servidor."],
                    ["/kadicionar_lembrete (nome) (dia) (informação adicional: opcional)",
                     "Adiciona um lembrete"],
                    ["/kremover_lembrete (nome)", "Remove um lembrete do servidor."],
                         ["/khoje", "Exibe os lembretes correspondentes ao dia atual."],
                         ["/keditar_informacao_adicional (nome) (informação adicional)",
                          "Edita as informações adicionais de um lembrete."],
                         ["/keditar_dia (nome) (dia)", "Edita o dia de um lembrete."],
                         ["/kmensagens_diarias",
                          "Informa como fazer o Kaburagi enviar lembretes automáticos no servidor."]]
        
    def ajuda(self):
        embed = Embed(title="Lista de Comandos:")
        comandos = self.comandos
        for comando in comandos:
            embed.add_field(name=comando[0], value=comando[1], inline=False)
        
        return embed

    def listar_lembretes_por_atributo(self, atributo, cursor, embed, atributo_especifico):
        cursor.execute("SELECT * FROM Lembretes WHERE Dia=?", (atributo,))
        lembretes_dia = cursor.fetchall()
        numero_lembretes = len(lembretes_dia)

        if lembretes_dia:
            if atributo_especifico:
                embed.description = 'Há {} lembrete(s)'.format(numero_lembretes)
            else:
                embed = embed.add_field(name="**{}**".format(atributo), value='Há {} lembrete(s)'.format(numero_lembretes), inline=False)

        for lembrete in lembretes_dia:
            cargo = "*Marcar: %s*" % (lembrete[3])
            descricao = "*Informação: %s*" % (lembrete[2])
            embed.add_field(name="> {}".format(lembrete[0]), value="> {}\n".format(descricao) + "> {}".format(cargo), inline=True)
        return embed

    def mostra_lembretes(self, nome_do_servidor, dia=None):
        print('\nFunção mostra lembretes')
        banco_existe = self.banco_de_dados.verifica_banco(nome_do_servidor)
        dia_especifico = False
        if banco_existe:
            banco = self.banco_de_dados.acessar_banco(nome_do_servidor)
            cursor = banco.cursor()
            if dia:
                dia_especifico = True
                embed = Embed(title="Lembretes de **{}**".format(dia))
                embed = self.listar_lembretes_por_atributo(dia, cursor, embed, dia_especifico)
                if not embed.fields:
                    embed = Embed(title="Não há lembretes para **%s**" % dia)
                    return embed
            else:
                embed = Embed(title="**Lembretes**")
                for dia in self.dias:
                    embed = self.listar_lembretes_por_atributo(dia, cursor, embed, dia_especifico)
                if not embed.fields:
                    embed = Embed(title="Não há lembretes neste servidor")
                    return embed
            print("Mostra lembretes finalizada\n")
            return embed
        else:
            print("Mostrar_lembretes finalizada\n")
            embed = Embed(title="Este servidor não possui lembretes")
            return embed

    def adiciona_lembretes(self, servidor, nome, dia, adicional, cargo):
        print('\nFunção adicionar lembrete')
        cargo_ou_pessoa_existe = False
        if cargo is not None:
            for cargo_do_servidor in servidor.roles:
                if cargo == cargo_do_servidor.name:
                    cargo_ou_pessoa_existe = True
                    break
            for membro in servidor.members:
                if cargo == membro.name or cargo_ou_pessoa_existe:
                    cargo_ou_pessoa_existe = True
            if not cargo_ou_pessoa_existe:
                return Embed(title="Este cargo/pessoa não existe")
        dados = {"Nome": nome, "Dia": dia, "Adicional": adicional, 'Cargo': cargo}
        if not self.banco_de_dados.insere_dados(servidor.name, self.tabela, dados, "Nome"):
            embed = Embed(title="Falha ao inserir lembrete (nome já existe na lista?)")
            print("Falha ao adicionar lembrete")
            return embed
        embed = Embed(title="Lembrete Inserido\n")
        embed.add_field(name=nome, value="Dia: %s\nInformação Adicional: %s\nMarcar: %s" % (dia, adicional, cargo))
        print("Lembrete inserido com sucesso\n")
        return embed

    def remove_lembretes(self, nome_do_servidor, nome):
        print('\nFunção remover lembrete')
        if not self.banco_de_dados.remove_dados(nome_do_servidor, self.tabela, nome, "Nome"):
            embed = Embed(title="Falha ao remover lembrete (nome não existe na lista?)")
            print("Falha ao remover lembrete\n")
            return embed
        embed = Embed(title="Lembrete para %s removido :)" % nome)
        print('Lembrete removido com sucesso\n')
        return embed

    def editar_lembrete(self, nome_do_servidor, atributo, nome, dado):
        print("\nFunção editar lembretes")
        if not self.banco_de_dados.edita_dados(nome_do_servidor, self.tabela, atributo, dado, nome, "Nome"):
            embed = Embed(title="Falha ao editar lembrete (nome não existe na lista?)")
            print('Falha ao editar lembrete\n')
            return embed
        embed = Embed(title="Lembrete Atualizado")
        embed.add_field(name=nome, value="%s: %s" % (atributo, dado))
        print('Lembrete editado com sucesso\n')
        return embed

    async def alarme(self, cliente):
        horarios_para_avisar = ['14:57', '19:30']
        for servidor in cliente.guilds:
            if retorna_hora() in horarios_para_avisar and self.banco_de_dados.verifica_banco(servidor.name):
                dia = retorna_dia_da_semana()
                message_channel = None
                cargos_para_marcar = []
                cargos = self.banco_de_dados.retorna_items_de_coluna_sem_repeticao(servidor.name, self.tabela, "Cargo",
                                                                                   coluna_limitadora="Dia", limite=dia)
                for cargo_para_marcar in cargos:
                    for cargo_do_servidor in servidor.roles:
                        if cargo_para_marcar == cargo_do_servidor.name:
                            cargos_para_marcar.append(cargo_do_servidor)
                    for membro in servidor.members:
                        if cargo_para_marcar == membro.name:
                            cargos_para_marcar.append(membro)
                print(cargos_para_marcar)
                for canal in servidor.channels:
                    if canal.name == "kaburagi":
                        message_channel = canal
                dia_da_semana = retorna_dia_da_semana()
                resultado = self.mostra_lembretes(servidor.name, dia=dia_da_semana)
                if message_channel:
                    if resultado.title != 'Não há lembretes para **%s**' % dia_da_semana:
                        print(f"Enviando para: {message_channel}")
                        mencoes = ''
                        if cargos_para_marcar:
                            for mencao in cargos_para_marcar:
                                mencoes += '%s ' % mencao.mention
                            await message_channel.send(mencoes, embed=resultado)
                        else:
                            await message_channel.send(embed=resultado)
                    else:
                        print("Não há lembretes para %s" % dia_da_semana)
                else:
                    if not message_channel:
                        print('canal não existe no servidor')

            else:
                print("Hora %s não é um horario para avisar ou servidor %s não existe" % (retorna_hora(), servidor))
