from discord.ext import commands
from funcionalidades import Lembrete
from discord.embeds import Embed
import string

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
        dia = args[index_do_dia]
        nome = ''.join(args[0:index_do_dia])
        adicional = ''.join(args[index_do_dia+1:])
        resultado = lembrete.adicionar_lembrete(contexto, nome, dia, adicional)
        await contexto.send(embed=resultado)
    else:
        await contexto.send(embed=Embed(title='Dia não encontrado na mensagem'))


@cliente.command()
async def al(contexto, *args):
    flag, index_do_dia = lembrete.interpreta_mensagem(args)
    if flag:
        dia = string.capwords(args[index_do_dia])
        nome = string.capwords(' '.join(args[0:index_do_dia]))
        adicional = ' '.join(args[index_do_dia+1:])
        resultado = lembrete.adicionar_lembrete(contexto, nome, dia, adicional)
        await contexto.send(embed=resultado)
    else:
        await contexto.send(embed=Embed(title='Dia não encontrado na mensagem'))


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
    banco_existe, resultado = lembrete.hoje(contexto)
    await contexto.send('%s' % contexto.author.mention)
    await contexto.send(embed=resultado)


@cliente.command()
async def editar_informacao_adicional(contexto, *args):
    def check(mensagem):
        return contexto.author == mensagem.author and mensagem.channel == mensagem.channel

    banco_existe, resultado = lembrete.verifica_banco(contexto)
    if not banco_existe:
        await contexto.send(embed=resultado)
    else:
        nome = string.capwords(' '.join(args))
        if not args or not lembrete.verifica_se_nome_existe(contexto, nome):
            await contexto.send(embed=Embed(title="Informe um lembrete válido"))
            return 0
        await contexto.send(embed=Embed(title="O que devo colocar nas informações adicionais de %s?" % nome))
        mensagem = await cliente.wait_for('message', check=check)
        mensagem = string.capwords(mensagem.content)
        await contexto.send(embed=lembrete.editar_informacao_adicional(contexto, nome, mensagem))


@cliente.command()
async def eia(contexto, *args):
    def check(mensagem):
        return contexto.author == mensagem.author and mensagem.channel == mensagem.channel

    banco_existe, resultado = lembrete.verifica_banco(contexto)
    if not banco_existe:
        await contexto.send(embed=resultado)
    else:
        nome = string.capwords(' '.join(args))
        if not args or not lembrete.verifica_se_nome_existe(contexto, nome):
            await contexto.send(embed=Embed(title="Informe um lembrete válido"))
            return 0
        await contexto.send(embed=Embed(title="O que devo colocar nas informações adicionais de %s?" % nome))
        mensagem = await cliente.wait_for('message', check=check)
        mensagem = string.capwords(mensagem.content)
        await contexto.send(embed=lembrete.editar_informacao_adicional(contexto, nome, mensagem))


@cliente.command()
async def ed(contexto, *args):
    def check(mensagem):
        return contexto.author == mensagem.author and mensagem.channel == mensagem.channel

    banco_existe, resultado = lembrete.verifica_banco(contexto)
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

    banco_existe, resultado = lembrete.verifica_banco(contexto)
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
'''
@cliente.event
async def avisa_animezada():
    global kaburagi, servidor, bot_ativo
    avisar = True
    while True:
        if (retorna_hora() == '20:00' or retorna_hora() == '22:30') and avisar:
            avisar = False
            await servidor.canal.send(servidor.cargo.mention)
            await servidor.canal.send(embed=kaburagi.informar_anime_do_dia())
        if retorna_hora() == '20:01' or retorna_hora() == "22:31":
            avisar = True
        await asyncio.sleep(1)
'''

cliente.run('ODA4NzEzNTMzMzk4ODQzMzky.YCKjKw.52-rt_tB5bEAiZ5aRenQgguYPmY')
