class VendaNaoEncontradaException(Exception):
    def __init__(self):
        super().__init__("Venda não encontrada.")