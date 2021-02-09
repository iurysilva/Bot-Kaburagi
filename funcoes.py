from datetime import date


def informar_dia_da_semana():
    dias_da_semana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sabado', 'Domingo']
    data = date.today().today()
    dia_da_semana_atual = dias_da_semana[data.weekday()]
    return dia_da_semana_atual


def informar_anime_do_dia(banco_animes, cargo):
    dia = informar_dia_da_semana()
    animes_do_dia = banco_animes.loc[dia, :]
    if type(animes_do_dia[1]) != str:
        return "Hoje não tem animezada :("
    else:
        animes = ''
        for anime in animes_do_dia:
            animes += '-%s\n' % anime
        return '@%s hoje tem:\n%s' % (cargo, animes)
