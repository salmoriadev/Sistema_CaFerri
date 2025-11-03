class ProdutoNaoEmEstoqueException(Exception):
    def __init__(self, nome_produto: str):
        super().__init__(f"O produto '{nome_produto}' não consta no estoque.")

