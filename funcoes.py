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
    bd_animes = bd_animes.rename(columns=bd_animes.iloc[0])
    return  bd_animes.drop(bd_animes.index[0])
