"""
Exceção lançada quando uma venda não é encontrada no repositório.

Esta exceção é usada pelo ControladorVenda quando uma busca por ID não encontra
a venda solicitada. Permite que controladores tratem a ausência de vendas de
forma específica, especialmente em operações de gerenciamento e exclusão.
"""

class VendaNaoEncontradaException(Exception):
    def __init__(self):
        super().__init__("Venda não encontrada.")
