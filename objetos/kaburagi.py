from funcoes import informar_dia_da_semana
from funcoes import condicoes_adicionar_anime
from funcoes import condicoes_remover_anime


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

    def adiciona_anime(self, mensagem):
        validacao_de_mensagem = condicoes_adicionar_anime(mensagem)
        if validacao_de_mensagem != "válida":
            return False, validacao_de_mensagem
        else:
            mensagem_separada = mensagem.split(' ')
            anime = ''
            for palavra in range(1, len(mensagem_separada)-1):
                if palavra == 1:
                    anime += '%s' % mensagem_separada[palavra]
                else:
                    anime += ' %s' % mensagem_separada[palavra]
            dia = mensagem.split(' ')[-1]
            tamanho_banco = self.banco_animes.shape[1]
            self.banco_animes.insert(tamanho_banco, tamanho_banco, [anime, "%s" % dia, 0])
            self.banco_animes.to_csv('banco_animes/bd_animes.csv', index=False, header=False)
            print(self.banco_animes)
            return True, anime

    def remover_anime(self, mensagem):
        validacao_de_mensagem = condicoes_remover_anime(mensagem)
        if validacao_de_mensagem != "válida":
            return False, validacao_de_mensagem
        else:
            mensagem_separada = mensagem.split(' ')
            anime = ''
            for palavra in range(1, len(mensagem_separada)):
                if palavra == 1:
                    anime += '%s' % mensagem_separada[palavra]
                else:
                    anime += ' %s' % mensagem_separada[palavra]
            print(anime)
            for coluna in self.banco_animes:
                if anime.lower() == self.banco_animes[coluna][0].lower():
                    self.banco_animes = self.banco_animes.drop(columns=[coluna])
                    self.banco_animes.to_csv('banco_animes/bd_animes.csv', index=False, header=False)
                    print(self.banco_animes)
                    return True, anime
            return False, "Anime não encontrado e não removido"

    def mostrar_animes(self):
        mensagem = ''
        for coluna in self.banco_animes:
            mensagem += '-Anime: %s\n' % self.banco_animes[coluna][0]
            mensagem += '-Dia: %s\n' % self.banco_animes[coluna][1]
            mensagem += '-Último episódio visto: %d\n\n' % int(self.banco_animes[coluna][2])
        return mensagem
