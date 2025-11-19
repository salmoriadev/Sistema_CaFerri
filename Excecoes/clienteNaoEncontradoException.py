"""
Exceção lançada quando um cliente não é encontrado no repositório.

Esta exceção é usada pelo ControladorCliente quando uma busca por ID não encontra
o cliente solicitado. Permite que controladores tratem a ausência de clientes
de forma específica, especialmente em operações de vendas e relatórios.
"""

class ClienteNaoEncontradoException(Exception):
    def __init__(self):
        super().__init__("Cliente não existe.")
