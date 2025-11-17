class SaldoInsuficienteException(Exception):
    def __init__(self):
        super().__init__("Saldo insuficiente para realizar a compra.")
