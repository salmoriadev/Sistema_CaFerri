class FornecedorNaoEncontradoException(Exception):
    def __init__(self):
        self.mensagem = f"Fornecedor não encontrado."
        super().__init__(self.mensagem)