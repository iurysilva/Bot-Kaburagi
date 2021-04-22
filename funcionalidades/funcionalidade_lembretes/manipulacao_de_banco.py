import os
import sqlite3


def acessar_banco(nome_do_servidor):
    banco = sqlite3.connect('funcionalidades/funcionalidade_lembretes/bancos' + '/%s' % nome_do_servidor)
    return banco


def verifica_banco(nome_do_servidor):
    print('Verificação de banco feita em: ', nome_do_servidor)
    nome_dos_bancos = []
    for arquivo in os.listdir('funcionalidades/funcionalidade_lembretes/bancos'):
        if arquivo != '__pycache__':
            nome_dos_bancos.append(arquivo)
    print('Servidores com lembretes: ', nome_dos_bancos)
    if nome_do_servidor in nome_dos_bancos:
        print('Banco %s existe' % nome_do_servidor)
        return True
    else:
        print('Banco %s não existe' % nome_do_servidor)
        return False


def verifica_se_nome_ja_existe(nome_do_servidor, nome):
    banco = acessar_banco(nome_do_servidor)
    cursor = banco.cursor()
    cursor.execute("SELECT * FROM Lembretes WHERE Nome=?", (nome,))
    if not cursor.fetchall():
        print("Lembrete com nome %s não existe no banco" % nome)
        return False
    else:
        print("Lembrete com nome %s existe no banco" % nome)
        return True


def listar_lembretes_por_dia(dia, cursor, embed, dia_especifico):
    cursor.execute("SELECT * FROM Lembretes WHERE Dia=?", (dia,))
    lembretes_dia = cursor.fetchall()
    numero_lembretes = len(lembretes_dia)

    if lembretes_dia:
        if dia_especifico:
            embed.description = 'Há {} lembrete(s)'.format(numero_lembretes)
        else:
            embed = embed.add_field(name=dia,value='Há {} lembrete(s)'.format(numero_lembretes),inline=False)
    
    for lembrete in lembretes_dia:
        descricao = "*Informação: %s*" % (lembrete[2])
        #descricao = "Dia: %s\nInformação Adicional: %s" % (lembrete[1], lembrete[2])
        embed.add_field(name=lembrete[0], value=descricao, inline=True)
    return embed