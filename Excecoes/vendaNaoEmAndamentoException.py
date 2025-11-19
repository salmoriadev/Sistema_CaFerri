"""
Exceção lançada quando se tenta modificar uma venda que não está em andamento.

Esta exceção é usada durante finalização de vendas e operações de carrinho
quando a venda já foi finalizada ou cancelada. Previne modificações em
vendas concluídas, mantendo integridade dos dados históricos.
"""

class VendaNaoEmAndamentoException(Exception):
    def __init__(self):
        super().__init__("Esta venda não está mais em andamento.")
