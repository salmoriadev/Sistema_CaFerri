"""
Exceção lançada quando um produto (café ou máquina) não é encontrado no sistema.

Esta exceção é usada pelo BuscaProdutoMixin quando uma busca por ID não encontra
o produto em nenhum repositório (nem em cafés, nem em máquinas). Permite que
controladores tratem a ausência de produtos de forma uniforme, independente
do tipo específico.
"""

class ProdutoNaoEncontradoException(Exception):
    def __init__(self):
        super().__init__("Produto não encontrado no sistema.")
