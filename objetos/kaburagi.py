from funcoes import informar_dia_da_semana


class Kaburagi:
    def __init__(self, cliente, servidor, banco_animes):
        self.cliente = cliente
        self.servidor = servidor
        self.banco_animes = banco_animes

    def informar_anime_do_dia(self):
        dia = informar_dia_da_semana()
        animes_do_dia = self.banco_animes.loc[dia, :]
        if type(animes_do_dia[1]) != str:
            return "Hoje não tem animezada :("
        else:
            animes = ''
            for anime in animes_do_dia:
                animes += '-%s\n' % anime
            for cargo in self.servidor.dados.roles:
                if cargo.name == self.servidor.cargo_para_marcar:
                    return '%s hoje tem:\n%s' % (cargo.mention, animes)
