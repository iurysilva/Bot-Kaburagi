from discord.ext import commands, tasks
from funcionalidades import Lembrete
from discord.embeds import Embed
import string
from funcionalidades.funcionalidade_lembretes.funcoes_auxiliares import retorna_hora

cliente = commands.Bot(command_prefix='?')
lembrete = Lembrete()
lembrete.atualizar_lista_de_bancos()


@cliente.event
async def on_ready():
    print('Kaburagi Iniciado!')


@cliente.command()
async def lembretes(contexto):
    banco_existe, resultado = lembrete.mostra_lembretes(contexto)
    await contexto.send(embed=resultado)


@cliente.command()
async def adicionar_lembrete(contexto, *args):
    flag, index_do_dia = lembrete.interpreta_mensagem(args)
    if flag:
        dia = string.capwords(args[index_do_dia])
        nome = string.capwords(' '.join(args[0:index_do_dia]))
        adicional = ' '.join(args[index_do_dia + 1:])
        resultado = lembrete.adicionar_lembrete(contexto, nome, dia, adicional)
        await contexto.send(embed=resultado)
    else:
        await contexto.send(embed=Embed(title='Dia não encontrado na  posição correta, escreva no formato:\n' +
                                              'Segunda, Terça, Quarta, Quinta, Sexta, Sábado ou Domingo.'))


@cliente.command()
async def al(contexto, *args):
    flag, index_do_dia = lembrete.interpreta_mensagem(args)
    if flag:
        dia = string.capwords(args[index_do_dia])
        nome = string.capwords(' '.join(args[0:index_do_dia]))
        adicional = ' '.join(args[index_do_dia + 1:])
        resultado = lembrete.adicionar_lembrete(contexto, nome, dia, adicional)
        await contexto.send(embed=resultado)
    else:
        await contexto.send(embed=Embed(title='Dia não encontrado na  posição correta, escreva no formato:\n' +
                                              'Segunda, Terça, Quarta, Quinta, Sexta, Sábado ou Domingo.'))


@cliente.command()
async def remover_lembrete(contexto, *args):
    nome = string.capwords(' '.join(args))
    removido, mensagem = lembrete.remover_lembrete(contexto, nome)
    await contexto.send(embed=Embed(title='%s' % mensagem))


@cliente.command()
async def rl(contexto, *args):
    nome = string.capwords(' '.join(args))
    removido, mensagem = lembrete.remover_lembrete(contexto, nome)
    await contexto.send(embed=Embed(title='%s' % mensagem))


@cliente.command()
async def ajuda(contexto):
    await contexto.send(embed=lembrete.ajuda())


@cliente.command()
async def hoje(contexto):
    banco_existe, resultado = lembrete.hoje(contexto.guild.name)
    await contexto.send('%s' % contexto.author.mention)
    await contexto.send(embed=resultado)


@cliente.command()
async def editar_informacao_adicional(contexto, *args):
    def check(mensagem):
        return contexto.author == mensagem.author and mensagem.channel == mensagem.channel

    banco_existe, resultado = lembrete.verifica_banco(contexto.guild.name)
    if not banco_existe:
        await contexto.send(embed=resultado)
    else:
        nome = string.capwords(' '.join(args))
        if not args or not lembrete.verifica_se_nome_existe(contexto, nome):
            await contexto.send(embed=Embed(title="Informe um lembrete válido"))
            return 0
        await contexto.send(embed=Embed(title="O que devo colocar nas informações adicionais de %s?" % nome))
        mensagem = await cliente.wait_for('message', check=check)
        await contexto.send(embed=lembrete.editar_informacao_adicional(contexto, nome, mensagem))


@cliente.command()
async def eia(contexto, *args):
    def check(mensagem):
        return contexto.author == mensagem.author and mensagem.channel == mensagem.channel

    banco_existe, resultado = lembrete.verifica_banco(contexto.guild.name)
    if not banco_existe:
        await contexto.send(embed=resultado)
    else:
        nome = string.capwords(' '.join(args))
        if not args or not lembrete.verifica_se_nome_existe(contexto, nome):
            await contexto.send(embed=Embed(title="Informe um lembrete válido"))
            return 0
        await contexto.send(embed=Embed(title="O que devo colocar nas informações adicionais de %s?" % nome))
        mensagem = await cliente.wait_for('message', check=check)
        await contexto.send(embed=lembrete.editar_informacao_adicional(contexto, nome, mensagem))


@cliente.command()
async def ed(contexto, *args):
    def check(mensagem):
        return contexto.author == mensagem.author and mensagem.channel == mensagem.channel

    banco_existe, resultado = lembrete.verifica_banco(contexto.guild.name)
    if not banco_existe:
        await contexto.send(embed=resultado)
    else:
        nome = string.capwords(' '.join(args))
        if not args or not lembrete.verifica_se_nome_existe(contexto, nome):
            await contexto.send(embed=Embed(title="Informe um lembrete válido"))
            return 0
        await contexto.send(embed=Embed(title="Para qual dia devo mudar %s?" % nome))
        mensagem = await cliente.wait_for('message', check=check)
        mensagem = string.capwords(mensagem.content)
        await contexto.send(embed=lembrete.editar_dia(contexto, nome, mensagem))


@cliente.command()
async def editar_dia(contexto, *args):
    def check(mensagem):
        return contexto.author == mensagem.author and mensagem.channel == mensagem.channel

    banco_existe, resultado = lembrete.verifica_banco(contexto.guild.name)
    if not banco_existe:
        await contexto.send(embed=resultado)
    else:
        nome = string.capwords(' '.join(args))
        if not args or not lembrete.verifica_se_nome_existe(contexto, nome):
            await contexto.send(embed=Embed(title="Informe um lembrete válido"))
            return 0
        await contexto.send(embed=Embed(title="Para qual dia devo mudar %s?" % nome))
        mensagem = await cliente.wait_for('message', check=check)
        mensagem = string.capwords(mensagem.content)
        await contexto.send(embed=lembrete.editar_dia(contexto, nome, mensagem))


@cliente.command()
async def mensagens_diarias(contexto):
    mensagem = Embed(title="Para receber mensagens diárias dos lembretes no servidor, faça:")
    mensagem.add_field(name="Crie um canal para o Kaburagi", value="O nome do canal deve ser: kaburagi", inline=False)
    mensagem.add_field(name="Crie um cargo para o Kaburagi marcar", value="O nome do cargo deve ser: Esquecido",
                       inline=False)
    await contexto.send(embed=mensagem)


@cliente.command()
async def md(contexto):
    mensagem = Embed(title="Para receber mensagens diárias dos lembretes no servidor, faça:")
    mensagem.add_field(name="Crie um canal para o Kaburagi", value="O nome do canal deve ser: kaburagi", inline=False)
    mensagem.add_field(name="Crie um cargo para o Kaburagi marcar", value="O nome do cargo deve ser: Esquecido",
                       inline=False)
    await contexto.send(embed=mensagem)


@tasks.loop(minutes=1)
async def called_once_a_day():
    horarios_para_avisar = ['12:00', '20:00', '22:30']
    for servidor in cliente.guilds:
        if retorna_hora() in horarios_para_avisar:
            message_channel = None
            cargo = None
            for role in servidor.roles:
                if role.name == "Esquecido":
                    cargo = role
            for canal in servidor.channels:
                if canal.name == "kaburagi":
                    message_channel = canal
            banco_existe, resultado = lembrete.hoje(servidor.name)
            if banco_existe and cargo and message_channel:
                print(f"Enviando para: {message_channel}")
                print(cargo)
                await message_channel.send(cargo.mention)
                await message_channel.send(embed=resultado)
            else:
                if not cargo:
                    print('cargo não existe no servidor')
                elif not message_channel:
                    print('canal não existe no servidor')
                print("Função hoje retornou False")

        else:
            print("Hora %s não é um horario para avisar" % retorna_hora())


@called_once_a_day.before_loop
async def before():
    await cliente.wait_until_ready()
    print("Terminou de Esperar")

called_once_a_day.start()
cliente.run('ODA4NzEzNTMzMzk4ODQzMzky.YCKjKw.52-rt_tB5bEAiZ5aRenQgguYPmY')
