from executaveis.initiate_bot import *

lembrete = Lembrete()


@slash.slash(name="kajuda_lembretes",
             description="Exibe todos os comandos da funcionalidade lembretes",
             options=[
                 create_option(
                     name="ignore",
                     description="ignore",
                     option_type=3,
                     required=False
                 )
             ]
             )
async def _ajuda_lembretes(contexto, ignore=None):
    embed = lembrete.ajuda()
    embed = adiciona_info(embed, contexto.author)
    await contexto.send(embed=embed)


@slash.slash(name="klembretes",
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
    resultado = lembrete.mostra_lembretes(nome_do_servidor, dia)
    resultado = adiciona_info(resultado, contexto.author)
    await contexto.send(embed=resultado)


@slash.slash(name="kadicionar_lembrete",
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
                     name="hora",
                     description="Hora na qual você quer ser lembrado.",
                     option_type=3,
                     required=True,
                     choices=[
                         create_choice(
                             name="09:00",
                             value="09:00"
                         ),
                         create_choice(
                             name="10:00",
                             value="10:00"
                         ),
                         create_choice(
                             name="11:00",
                             value="11:00"
                         ),
                         create_choice(
                             name="12:00",
                             value="12:00"
                         ),
                         create_choice(
                             name="13:00",
                             value="13:00"
                         ),
                         create_choice(
                             name="14:00",
                             value="14:00"
                         ),
                         create_choice(
                             name="15:00",
                             value="15:00"
                         ),
                         create_choice(
                             name="16:00",
                             value="16:00"
                         ),
                         create_choice(
                             name="17:00",
                             value="17:00"
                         ),
                         create_choice(
                             name="18:00",
                             value="18:00"
                         ),
                         create_choice(
                             name="19:00",
                             value="19:00"
                         ),
                         create_choice(
                             name="20:00",
                             value="20:00"
                         ),
                         create_choice(
                             name="21:00",
                             value="21:00"
                         ),
                         create_choice(
                             name="22:00",
                             value="22:00"
                         ),
                         create_choice(
                             name="23:00",
                             value="23:00"
                         ),
                     ]
                 ),
                 create_option(
                     name="informacao_adicional",
                     description="Alguma informação adicional para o lembrete.",
                     option_type=3,
                     required=False
                 ),
                 create_option(
                     name="cargo_ou_pessoa",
                     description="Marca o cargo ou pessoa descrita.",
                     option_type=3,
                     required=False
                 ),
             ])
async def _adicionar_lembrete(contexto, nome, dia, hora, informacao_adicional=None, cargo_ou_pessoa=None):
    nome = string.capwords(nome)
    resultado = lembrete.adiciona_lembretes(contexto.guild, nome, dia, hora, informacao_adicional, cargo_ou_pessoa)
    resultado = adiciona_info(resultado, contexto.author)
    await contexto.send(embed=resultado)


@cliente.command()
async def adicionar_lembrete(contexto, nome, dia, hora, informacao_adicional=None, cargo_ou_pessoa=None):
    nome = string.capwords(nome)
    resultado = lembrete.adiciona_lembretes(contexto.guild, nome, dia, hora, informacao_adicional, cargo_ou_pessoa)
    resultado = adiciona_info(resultado, contexto.author)
    await contexto.send(embed=resultado)


@slash.slash(name="kremover_lembrete",
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
    resultado = lembrete.remove_lembretes(nome_do_servidor, nome)
    resultado = adiciona_info(resultado, contexto.author)
    await contexto.send(embed=resultado)


@slash.slash(name="khoje",
             description="Exibe os lembretes correspondentes ao dia atual.",
             options=[
                 create_option(
                     name="ignore",
                     description="ignore",
                     option_type=3,
                     required=False
                 )
             ]
             )
async def _hoje(contexto, ignore=None):
    dia = retorna_dia_da_semana()
    embed = lembrete.mostra_lembretes(contexto.guild.name, dia)
    embed = adiciona_info(embed, contexto.author)
    await contexto.send(embed=embed)


@slash.slash(name="keditar_informacao_adicional",
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
    resultado = lembrete.editar_lembrete(nome_do_servidor, "Adicional", nome, informacao_adicional)
    resultado = adiciona_info(resultado, contexto.author)
    await contexto.send(embed=resultado)


@slash.slash(name="keditar_dia",
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
    resultado = lembrete.editar_lembrete(nome_do_servidor, "Dia", nome, dia)
    resultado = adiciona_info(resultado, contexto.author)
    await contexto.send(embed=resultado)


@slash.slash(name="kmensagens_diarias",
             description="Instruções para receber as mensagens diárias do Kaburagi.",
             options=[
                 create_option(
                     name="ignore",
                     description="ignore",
                     option_type=3,
                     required=False
                 )
             ]
             )
async def _mensagens_diarias(contexto, ignore=None):
    mensagem = Embed(title="Os lembretes diários funcionam da seguinte forma:")
    mensagem = adiciona_info(mensagem)
    mensagem.add_field(name="Crie um canal para o kaburagi enviar os lembretes",
                       value="No seu servidor, crie um canal de texto com o nome: Kaburagi.",
                       inline=False)
    mensagem.add_field(name="Crie lembretes", value="Utilize os comandos para criar lembretes.", inline=False)
    mensagem.add_field(name="Pronto!",
                       value="O Kaburagi vai automaticamente enviar os lembretes no canal criado quando chegar a hora.",
                       inline=False)
    await contexto.send(embed=mensagem)

