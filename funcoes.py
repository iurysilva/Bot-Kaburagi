import datetime


def informar_dia_da_semana():
    dias_da_semana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sabado', 'Domingo']
    data = datetime.date.today().today()
    dia_da_semana_atual = dias_da_semana[data.weekday()]
    return dia_da_semana_atual


def retorna_hora():
    data_e_hora = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
    hora = data_e_hora[11:]
    return hora
