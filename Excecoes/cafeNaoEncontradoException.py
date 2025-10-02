class CafeNaoEncontradoException(Exception):
    def __init__(self):
        self.mensagem = "Café não encontrado."
        super().__init__(self.mensagem)