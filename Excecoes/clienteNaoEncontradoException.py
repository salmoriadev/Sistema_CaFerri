class ClienteNaoEncontradoException(Exception):
    def __init__(self, id):
        self.id = id
        self.mensagem = f"Cliente com ID {id} não existe."
        super().__init__(self.mensagem)
