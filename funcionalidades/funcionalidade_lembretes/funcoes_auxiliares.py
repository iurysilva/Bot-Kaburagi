from datetime import datetime, date
from pytz import timezone


def retorna_hora():
    data_e_hora = datetime.now()
    fuso_horario = timezone('America/Sao_Paulo')
    data_e_hora = data_e_hora.astimezone(fuso_horario).strftime('%d/%m/%Y %H:%M')
    hora = data_e_hora[11:]
    return hora


def retorna_dia_da_semana():
    dias_da_semana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
    data = date.today().today()
    if 0 < int(retorna_hora()[:2]) < 3:
        dia_da_semana_atual = dias_da_semana[data.weekday() - 1]
    else:
        dia_da_semana_atual = dias_da_semana[data.weekday()]
    return dia_da_semana_atual