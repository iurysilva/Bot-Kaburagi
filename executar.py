from discord.ext import commands, tasks
from funcionalidades import Lembrete
from discord.embeds import Embed
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option, create_choice
import string
from funcionalidades.funcionalidade_lembretes.informacoes_sobre_tempo import retorna_hora
from funcionalidades.funcionalidade_lembretes.informacoes_sobre_tempo import retorna_dia_da_semana
from funcionalidades.funcionalidade_lembretes.manipulacao_de_embed import adiciona_info
from funcionalidades.funcionalidade_lembretes.manipulacao_de_banco import verifica_banco

cliente = commands.Bot(command_prefix='?')
slash = SlashCommand(cliente, sync_commands=True)
lembrete = Lembrete()


@cliente.event
async def on_ready():
    print('Kaburagi Iniciado!')


@slash.slash(name="klembretes", 
             guild_ids=[460678660559470592], 
             description="Lista os lembretes do servidor.",
             options=[
               create_option(
                 name="dia",
                 description="Lembretes de um dia específico.",
                 option_type=3,
                 required=False,
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
             ]
             )
async def _lembretes(contexto, dia=None):
    nome_do_servidor = contexto.guild.name
    resultado = lembrete.mostra_lembretes(nome_do_servidor, dia, contexto.author)
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
                 name="informacao_adicional",
                 description="Alguma informação adicional para o lembrete.",
                 option_type=3,
                 required=False
               ),
             ])
async def _adicionar_lembrete(contexto, nome, dia, informacao_adicional=None):
    nome = string.capwords(nome)
    nome_do_servidor = contexto.guild.name
    resultado = lembrete.adicionar_lembrete(nome_do_servidor, nome, dia, informacao_adicional, contexto.author)
    await contexto.send(embed=resultado)


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
    nome = string.capwords(nome)
    nome_do_servidor = contexto.guild.name
    resultado = lembrete.remover_lembrete(nome_do_servidor, nome, contexto.author)
    await contexto.send(embed=resultado)


@slash.slash(name="kajuda", 
             guild_ids=[460678660559470592],
             description="Exibe todos os comandos e suas descrições."
             )
async def _ajuda(contexto):
    embed = lembrete.ajuda()
    embed = adiciona_info(embed, contexto.author)
    await contexto.send(embed=embed)


@slash.slash(name="khoje", 
             guild_ids=[460678660559470592],
             description="Exibe os lembretes correspondentes ao dia atual."
             )
async def _hoje(contexto):
    dia = retorna_dia_da_semana()
    embed = lembrete.mostra_lembretes(contexto.guild.name, dia, contexto.author)
    await contexto.send(embed=embed)


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
                 name="informacao_adicional",
                 description="Nova informação adicional para o lembrete.",
                 option_type=3,
                 required=True
               ),
             ])
async def _editar_informacao_adicional(contexto, nome, informacao_adicional):
    nome = string.capwords(nome)
    nome_do_servidor = contexto.guild.name
    resultado = lembrete.editar_informacao_adicional(nome_do_servidor, nome, informacao_adicional, contexto.author)
    await contexto.send(embed=resultado)


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
    nome = string.capwords(nome)
    nome_do_servidor = contexto.guild.name
    resultado = lembrete.editar_dia(nome_do_servidor, nome, dia, contexto.author)
    await contexto.send(embed=resultado)


@slash.slash(name="kmensagens_diarias", 
             guild_ids=[460678660559470592],
             description="Instruções para receber as mensagens diárias do Kaburagi."
             )
async def _mensagens_diarias(contexto):
    mensagem = Embed(title="Para receber mensagens diárias dos lembretes no servidor, faça:")
    mensagem = adiciona_info(mensagem)
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
            dia_da_semana = retorna_dia_da_semana()
            resultado = lembrete.mostra_lembretes(servidor.name, dia=dia_da_semana)
            if verifica_banco(servidor.name) and cargo and message_channel:
                if resultado.title != 'Não há lembretes para **%s**' % dia_da_semana:
                    print(f"Enviando para: {message_channel}")
                    print(cargo)
                    await message_channel.send(cargo.mention, embed=resultado)
                else:
                    print("Não há lembretes para %s" % dia_da_semana)
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