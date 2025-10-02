class MaquinaNaoEncontradaException(Exception):
    def __init__(self):
        self.mensagem = "Máquina não encontrada."
        super().__init__(self.mensagem)