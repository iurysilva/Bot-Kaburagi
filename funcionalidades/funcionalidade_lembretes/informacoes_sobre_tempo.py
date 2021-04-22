from datetime import datetime, date
from pytz import timezone


def retorna_data_hora():
    data_e_hora = datetime.now()
    fuso_horario = timezone('America/Sao_Paulo')
    data_e_hora = data_e_hora.astimezone(fuso_horario)
    return data_e_hora


def retorna_hora():
    data_e_hora = datetime.now()
    fuso_horario = timezone('America/Sao_Paulo')
    data_e_hora = data_e_hora.astimezone(fuso_horario).strftime('%d/%m/%Y %H:%M')
    hora = data_e_hora[11:]
    return hora


def retorna_dia_da_semana():
    dias_da_semana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
    fuso_horario = timezone('America/Sao_Paulo')
    data = datetime.now().astimezone(fuso_horario).date().weekday()
    return dias_da_semana[data]
