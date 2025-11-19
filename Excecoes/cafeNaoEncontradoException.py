"""
Exceção lançada quando um café não é encontrado no repositório.

Esta exceção é usada pelo ControladorCafe quando uma busca por ID não encontra
o café solicitado. Permite que controladores tratem a ausência de cafés de
forma específica, diferenciando de outros tipos de produtos.
"""

class CafeNaoEncontradoException(Exception):
    def __init__(self):
        super().__init__("Café não encontrado.")
