class VendaNaoEmAndamentoException(Exception):
    def __init__(self):
        super().__init__("Esta venda não está mais em andamento.")

