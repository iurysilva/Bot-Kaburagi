from discord.ext import commands, tasks
from funcionalidades import Lembrete
from discord.embeds import Embed
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option, create_choice
import string
from funcionalidades.funcionalidade_lembretes.funcoes_auxiliares import retorna_hora

cliente = commands.Bot(command_prefix='?')
slash = SlashCommand(cliente, sync_commands=True)
lembrete = Lembrete()
lembrete.atualizar_lista_de_bancos()


@cliente.event
async def on_ready():
    print('Kaburagi Iniciado!')


@slash.slash(name="klembretes", 
             guild_ids=[460678660559470592], 
             description="Lista todos os lembretes do servidor.")
async def _lembretes(contexto):
    banco_existe, resultado = lembrete.mostra_lembretes(contexto)
    await contexto.send(embed=resultado)


@slash.slash(name="kadicionar_lembrete",
             guild_ids=[460678660559470592],
             description="Adiciona um lembrete.",
             options=[
                 create_option(
                 name="nome",
                 description="Nome do lembrete.",
                 option_type=3,
                 required=True
               ),
                 create_option(
                 name="dia",
                 description="Dia no qual você quer ser lembrado.",
                 option_type=3,
                 required=True,
                 choices=[
                  create_choice(
                    name="Segunda-Feira",
                    value="Segunda"
                  ),
                  create_choice(
                    name="Terça-Feira",
                    value="Terça"
                  ),
                  create_choice(
                    name="Quarta-Feira",
                    value="Quarta"
                  ),
                  create_choice(
                    name="Quinta-Feira",
                    value="Quinta"
                  ),
                  create_choice(
                    name="Sexta-Feira",
                    value="Sexta"
                  ),
                  create_choice(
                    name="Sábado",
                    value="Sábado"
                  ),
                  create_choice(
                    name="Domingo",
                    value="Domingo"
                  ),
                ]
               ),
                 create_option(
                 name="informação_adicional",
                 description="Alguma informação adicional para o lembrete.",
                 option_type=3,
                 required=False
               ),
             ])
async def _adicionar_lembrete(contexto, *args):
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



@slash.slash(name="kremover_lembrete", 
             guild_ids=[460678660559470592],
             description="Remove um lembrete do servidor.",
             options=[
                 create_option(
                 name="nome",
                 description="Nome do lembrete a ser removido.",
                 option_type=3,
                 required=True
               )
             ])
async def _remover_lembrete(contexto, nome):
    removido, mensagem = lembrete.remover_lembrete(contexto, string.capwords(nome))
    await contexto.send(embed=Embed(title='%s' % mensagem))


@slash.slash(name="kajuda", 
             guild_ids=[460678660559470592],
             description="Exibe todos os comandos e suas descrições."
             )
async def _ajuda(contexto):
    await contexto.send(embed=lembrete.ajuda())


@slash.slash(name="khoje", 
             guild_ids=[460678660559470592],
             description="Exibe os lembretes correspondentes ao dia atual."
             )
async def _hoje(contexto):
    banco_existe, resultado = lembrete.hoje(contexto.guild.name)
    await contexto.send(embed=resultado)


@slash.slash(name="keditar_informacao_adicional", 
             guild_ids=[460678660559470592],
             description="Edita as informações adicionais de um lembrete.",
             options=[
                 create_option(
                 name="nome",
                 description="Nome do lembrete a ser editado.",
                 option_type=3,
                 required=True
               ),
                 create_option(
                 name="informação_adicional",
                 description="Nova informação adicional para o lembrete.",
                 option_type=3,
                 required=True
               ),
             ])
async def _editar_informacao_adicional(contexto, nome, informacao):
    def check(mensagem):
        return contexto.author == mensagem.author and mensagem.channel == mensagem.channel

    if not lembrete.verifica_se_nome_existe(contexto, string.capwords(nome)):
        await contexto.send(embed=Embed(title="Informe um lembrete válido"))
        return 0
    
    await contexto.send(embed=lembrete.editar_informacao_adicional(contexto, string.capwords(nome), informacao))


@slash.slash(name="keditar_dia", 
             guild_ids=[460678660559470592],
             description="Edita o dia de um lembrete.",
             options=[
                 create_option(
                 name="nome",
                 description="Nome do lembrete a ser editado.",
                 option_type=3,
                 required=True,
               ),
                 create_option(
                 name="dia",
                 description="Novo dia do lembrete.",
                 option_type=3,
                 required=True,
                 choices=[
                  create_choice(
                    name="Segunda-Feira",
                    value="Segunda"
                  ),
                  create_choice(
                    name="Terça-Feira",
                    value="Terça"
                  ),
                  create_choice(
                    name="Quarta-Feira",
                    value="Quarta"
                  ),
                  create_choice(
                    name="Quinta-Feira",
                    value="Quinta"
                  ),
                  create_choice(
                    name="Sexta-Feira",
                    value="Sexta"
                  ),
                  create_choice(
                    name="Sábado",
                    value="Sábado"
                  ),
                  create_choice(
                    name="Domingo",
                    value="Domingo"
                  ),
                ]
               ),
             ])
async def _editar_dia(contexto, nome, dia):

    def check(mensagem):
        return contexto.author == mensagem.author and mensagem.channel == mensagem.channel

    if not lembrete.verifica_se_nome_existe(contexto, string.capwords(nome)):
        await contexto.send(embed=Embed(title="Informe um lembrete válido"))
        return 0
      
    await contexto.send(embed=lembrete.editar_dia(contexto, string.capwords(nome), dia))


@slash.slash(name="kmensagens_diarias", 
             guild_ids=[460678660559470592],
             description="Instruções para receber as mensagens diárias do Kaburagi."
             )
async def _mensagens_diarias(contexto):
    mensagem = Embed(title="Para receber mensagens diárias dos lembretes no servidor, faça:")
    mensagem.add_field(name="Crie um canal para o Kaburagi", value="O nome do canal deve ser: kaburagi", inline=False)
    mensagem.add_field(name="Crie um cargo para o Kaburagi marcar", value="O nome do cargo deve ser: Esquecido",
                       inline=False)
    await contexto.send(embed=mensagem)


@tasks.loop(minutes=1)
async def called_once_a_day():
    horarios_para_avisar = ['09:00', '17:00', '19:30']
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