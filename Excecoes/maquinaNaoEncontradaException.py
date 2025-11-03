class MaquinaNaoEncontradaException(Exception):
    def __init__(self):
        super().__init__("Máquina não encontrada.")