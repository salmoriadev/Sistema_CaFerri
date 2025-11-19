"""
Exceção lançada quando se tenta criar uma entidade com ID já existente.

Esta exceção previne duplicação de identificadores únicos no sistema. É usada
durante criação de vendas e outras entidades que requerem IDs únicos. O tipo
de objeto é passado como parâmetro para mensagem de erro mais descritiva.
"""

class IDJaExistenteException(Exception):
    def __init__(self, tipo_objeto: str):
        super().__init__(f"ERRO: Já existe um(a) {tipo_objeto} com este ID.")
