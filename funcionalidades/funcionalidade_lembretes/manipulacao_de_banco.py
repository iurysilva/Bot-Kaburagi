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


def listar_lembretes_por_dia(dia, cursor, embed):
    cursor.execute("SELECT * FROM Lembretes WHERE Dia=?", (dia,))
    for lembrete in cursor.fetchall():
        print('acessando lembrete: ', lembrete)
        descricao = "Dia: %s\nInformação Adicional: %s" % (lembrete[1], lembrete[2])
        embed.add_field(name=lembrete[0], value=descricao, inline=False)
    return embed