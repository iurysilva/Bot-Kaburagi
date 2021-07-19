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
    resultado = lembrete.mostra_lembretes(nome_do_servidor, dia, contexto.author)
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
                     name="informacao_adicional",
                     description="Alguma informação adicional para o lembrete.",
                     option_type=3,
                     required=False
                 ),
             ])
async def _adicionar_lembrete(contexto, nome, dia, informacao_adicional=None):
    nome = string.capwords(nome)
    nome_do_servidor = contexto.guild.name
    resultado = lembrete.adiciona_lembretes(nome_do_servidor, nome, dia, informacao_adicional)
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
    embed = lembrete.mostra_lembretes(contexto.guild.name, dia, contexto.author)
    print("Enviando...")
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
             description="Instruções para receber as mensagens diárias do Kaburagi."
             )
async def _mensagens_diarias(contexto):
    mensagem = Embed(title="Para receber mensagens diárias dos lembretes no servidor, faça:")
    mensagem = adiciona_info(mensagem)
    mensagem.add_field(name="Crie um canal para o Kaburagi", value="O nome do canal deve ser: kaburagi", inline=False)
    mensagem.add_field(name="Crie um cargo para o Kaburagi marcar", value="O nome do cargo deve ser: Esquecido",
                       inline=False)
    await contexto.send(embed=mensagem)

