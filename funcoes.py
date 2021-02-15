import datetime
import pandas as pd


def informar_dia_da_semana():
    dias_da_semana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sabado', 'Domingo']
    data = datetime.date.today().today()
    if 0 < int(retorna_hora()[:2]) < 3:
        dia_da_semana_atual = dias_da_semana[data.weekday() - 1]
    else:
        dia_da_semana_atual = dias_da_semana[data.weekday()]
    return dia_da_semana_atual


def retorna_hora():
    data_e_hora = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
    hora = data_e_hora[11:]
    return hora


def cria_banco_de_dados():
    
    try:
        bd_animes = pd.read_csv('banco_animes/bd_animes.csv', 
                                header=None,
                                names=['anime','dia','episodio']
                                )
    except:
        bd_animes = pd.DataFrame(columns=['anime','dia','episodio'])
    print(bd_animes)
    return bd_animes


def interpreta_mensagem(mensagem):
    mensagem_separada = mensagem.split(' ')
    if mensagem_separada[0].lower() == '?animes':
        return 'animes'
    elif mensagem_separada[0].lower() == '?adicionar':
        return 'adicionar'
    elif mensagem_separada[0].lower() == '?remover':
        return 'remover'
    elif mensagem_separada[0].lower() == '?assistido':
        return 'assistido'
    elif mensagem_separada[0].lower() == '?ajuda':
        return 'ajuda'
    elif mensagem_separada[0].lower() == '?hoje':
        return 'hoje'
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


def condicoes_incrementar_episodio(mensagem):
    mensagem_separada = mensagem.split(' ')
    if not mensagem_separada[-1].isdigit():
        return "Número de episódios assistidos faltando"
    elif len(mensagem_separada) < 3:
        return "Comando com espaços faltando"
    else:
        return "válida"


def retorna_comandos():
    comandos = []
    comandos.append(["?animes", "Mostra todos os animes sendo assistidos no momento, com episódio atual e dia."])
    comandos.append(["?adicionar (anime) (dia)", "Adiciona um anime para o Animezada, dia no formato: terça, quarta etc."])
    comandos.append(["?remover (anime)", "Remove uma anime do Animezada."])
    comandos.append(["?assistido (anime) (episódio visto)", "Modifica o episódio atual do anime."])
    comandos.append(["?hoje", "Informa os animes que serão assistidos no dia atual."])
    return comandos