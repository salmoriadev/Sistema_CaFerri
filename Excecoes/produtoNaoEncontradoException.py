class ProdutoNaoEncontradoException(Exception):
    def __init__(self):
        super().__init__("Produto não encontrado no sistema.")