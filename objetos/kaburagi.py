from funcoes import informar_dia_da_semana
from funcoes import condicoes_adicionar_anime
from funcoes import condicoes_remover_anime
from funcoes import condicoes_incrementar_episodio


class Kaburagi:
    def __init__(self, cliente, servidor, banco_animes):
        self.cliente = cliente
        self.servidor = servidor
        self.banco_animes = banco_animes

    def ajuda(self):
        mensagem1 = "Lista de Comandos:\n"
        mensagem2 = "?animes - Lista todos os animes sendo assistidos no momento, com episódio atual e dia.\n"
        mensagem3 = "?adicionar (anime) (dia) - Adiciona um anime para o Animezada, dia no formato: terça, quarta etc.\n"
        mensagem4 = "?remover (anime) - Remove uma anime do Animezada\n"
        mensagem5 = "?assistido (anime) (número de episódios vistos) - Modifica o episódio atual do anime\n"
        mensagem = mensagem1 + mensagem2 + mensagem3 + mensagem4 + mensagem5
        print(mensagem)
        return mensagem1 + mensagem2 + mensagem3 + mensagem4 + mensagem5

    def informar_anime_do_dia(self):
        animes_do_dia = []
        episodios = []
        dia_de_hoje = informar_dia_da_semana()
        for coluna in self.banco_animes:
            atributo_dia = self.banco_animes[coluna][1]
            if atributo_dia.lower() == dia_de_hoje.lower():
                animes_do_dia.append(self.banco_animes[coluna][0])
                episodios.append(self.banco_animes[coluna][2])
        if not animes_do_dia:
            return "Hoje não tem animezada :("
        else:
            mensagem = ''
            for anime in range(0, len(animes_do_dia)):
                mensagem += '-%s episódio %s\n' % (animes_do_dia[anime], episodios[anime])
            for cargo in self.servidor.dados.roles:
                if cargo.name == self.servidor.cargo_para_marcar:
                    return '%s hoje tem:\n%s' % (cargo.mention, mensagem)

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
            for coluna in self.banco_animes:
                if anime.lower() == self.banco_animes[coluna][0].lower():
                    self.banco_animes = self.banco_animes.drop(columns=[coluna])
                    self.banco_animes.to_csv('banco_animes/bd_animes.csv', index=False, header=False)
                    print(self.banco_animes)
                    return True, anime
            return False, "Anime não encontrado e não removido"

    def modificar_episodio(self, mensagem):
        validacao_de_mensagem = condicoes_incrementar_episodio(mensagem)
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
            for coluna in self.banco_animes:
                if anime.lower() == self.banco_animes[coluna][0].lower():
                    num_episodios = self.banco_animes[coluna][2]
                    novo_num_episodios = mensagem_separada[-1]
                    self.banco_animes.loc[2, coluna] = novo_num_episodios
                    self.banco_animes.to_csv('banco_animes/bd_animes.csv', index=False, header=False)
                    print(self.banco_animes)
                    return True, anime
            return False, "Anime não encontrado e não incrementado"

    def mostrar_animes(self):
        mensagem = 'Animes sendo vistos atualmente:\n'
        for coluna in self.banco_animes:
            mensagem += '-Anime: %s\n' % self.banco_animes[coluna][0]
            mensagem += '-Dia: %s\n' % self.banco_animes[coluna][1]
            mensagem += '-Último episódio visto: %d\n\n' % int(self.banco_animes[coluna][2])
        return mensagem
