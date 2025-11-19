"""
Exceção lançada quando quantidade solicitada excede disponibilidade no estoque.

Esta exceção é usada durante finalização de vendas e baixas manuais de estoque
quando a quantidade necessária é maior que a quantidade disponível. Inclui
informações detalhadas (nome do produto, quantidade necessária e disponível)
para facilitar diagnóstico e correção do problema.
"""

class EstoqueInsuficienteException(Exception):
    def __init__(self, nome_produto: str, quantidade_necessaria: int, quantidade_disponivel: int):
        super().__init__(
            f"Estoque insuficiente para '{nome_produto}'. Necessário: {quantidade_necessaria}, Disponível: {quantidade_disponivel}.")
