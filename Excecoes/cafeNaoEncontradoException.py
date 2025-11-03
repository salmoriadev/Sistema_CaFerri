class CafeNaoEncontradoException(Exception):
    def __init__(self):
        super().__init__("Café não encontrado.")