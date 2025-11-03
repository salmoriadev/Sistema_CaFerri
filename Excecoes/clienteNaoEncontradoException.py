class ClienteNaoEncontradoException(Exception):
    def __init__(self):
        super().__init__("Cliente não existe.")
