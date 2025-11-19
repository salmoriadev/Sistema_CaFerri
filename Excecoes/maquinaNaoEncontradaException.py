"""
Exceção lançada quando uma máquina de café não é encontrada no repositório.

Esta exceção é usada pelo ControladorMaquinaDeCafe quando uma busca por ID não
encontra a máquina solicitada. Permite que controladores tratem a ausência de
máquinas de forma específica, diferenciando de outros tipos de produtos.
"""

class MaquinaNaoEncontradaException(Exception):
    def __init__(self):
        super().__init__("Máquina não encontrada.")
