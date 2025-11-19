"""
Exceção lançada quando um produto não está cadastrado no estoque.

Esta exceção é usada durante finalização de vendas e baixas de estoque quando
o produto solicitado não existe no inventário. Inclui nome do produto na
mensagem para facilitar diagnóstico e correção do problema.
"""

class ProdutoNaoEmEstoqueException(Exception):
    def __init__(self, nome_produto: str):
        super().__init__(f"O produto '{nome_produto}' não consta no estoque.")
