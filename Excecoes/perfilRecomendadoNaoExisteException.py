"""
Exceção lançada quando um perfil de consumidor inválido é fornecido.

Esta exceção é usada pela classe PerfilConsumidor durante inicialização quando
o perfil fornecido não está na lista de perfis válidos. Inclui o perfil
inválido na mensagem para facilitar correção. Previne criação de clientes ou
cafés com perfis inválidos, mantendo consistência dos dados.
"""

class PerfilRecomendadoNaoExisteException(Exception):
    def __init__(self, perfil: str):
        super().__init__(f"Perfil recomendado '{perfil}' não existe.")
