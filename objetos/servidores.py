class Bar_dos_Cornos:
    def __init__(self, cliente):
        self.cliente = cliente
        self.cargo_para_marcar = "Animezeiro"
        self.dados = self.cliente.get_guild(460678660559470592)
        self.canal = cliente.get_channel(793281337531301889)
        self.cargo = self.retorna_cargo()

    def retorna_cargo(self):
        for cargo in self.dados.roles:
            if cargo.name == self.cargo_para_marcar:
                return cargo


class Teste:
    def __init__(self, cliente):
        self.cliente = cliente
        self.cargo_para_marcar = "Animes"
        self.dados = self.cliente.get_guild(744388439113334895)
        self.canal = cliente.get_channel(808760229709348905)
        self.cargo = self.retorna_cargo()

    def retorna_cargo(self):
        for cargo in self.dados.roles:
            if cargo.name == self.cargo_para_marcar:
                return cargo
