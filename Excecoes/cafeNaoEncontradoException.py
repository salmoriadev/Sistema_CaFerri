class CafeNaoEncontradoException(Exception):
    def __init__(self, id_cafe: int):
        self.mensagem = "Café com ID {} não encontrado.".format(id_cafe)
        super().__init__(self.mensagem)