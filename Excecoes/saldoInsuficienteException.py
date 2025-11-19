"""
Exceção lançada quando cliente não possui saldo suficiente para finalizar venda.

Esta exceção é usada durante finalização de vendas quando o valor total da
compra excede o saldo disponível do cliente. Previne transações que resultariam
em saldo negativo, mantendo integridade financeira do sistema.
"""

class SaldoInsuficienteException(Exception):
    def __init__(self):
        super().__init__("Saldo insuficiente para realizar a compra.")
