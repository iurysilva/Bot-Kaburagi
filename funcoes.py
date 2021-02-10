import datetime
import pandas as pd


def informar_dia_da_semana():
    dias_da_semana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sabado', 'Domingo']
    data = datetime.date.today().today()
    dia_da_semana_atual = dias_da_semana[data.weekday()]
    return dia_da_semana_atual


def retorna_hora():
    data_e_hora = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
    hora = data_e_hora[11:]
    return hora


def cria_banco_de_dados():
    bd_animes = pd.read_csv('banco_animes/bd_animes.csv', header=None)
    print(bd_animes, '\n')
    return bd_animes


def interpreta_mensagem(mensagem):
    mensagem_separada = mensagem.split(' ')
    if mensagem_separada[0].lower() == '?animes':
        return 'animes'
    elif mensagem_separada[0].lower() == '?adicionar':
        return 'adicionar'
    elif mensagem_separada[0].lower() == '?remover':
        return 'remover'
    else:
        return False


def condicoes_adicionar_anime(mensagem):
    mensagem_separada = mensagem.split(' ')
    dias = ['segunda', 'terça', 'quarta', "quinta", "sexta", "sábado", "domingo"]
    if len(mensagem_separada) < 3:
        return "Comando com espaços faltando"
    elif mensagem_separada[-1].lower() not in dias:
        return "Dia escrito incorretamente, escreva no formato: Segunda, Terça etc."
    else:
        return "válida"


def condicoes_remover_anime(mensagem):
    mensagem_separada = mensagem.split(' ')
    if len(mensagem_separada) < 2:
        return "Comando com espaços faltando"
    else:
        return "válida"
