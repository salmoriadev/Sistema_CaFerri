class ClienteNaoEncontradoException(Exception):
    def __init__(self):
        self.mensagem = "Cliente não existe."
        super().__init__(self.mensagem)
