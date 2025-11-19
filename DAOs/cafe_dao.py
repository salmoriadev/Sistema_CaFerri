"""
DAO especializado para persistência de entidades Cafe.

Este módulo implementa operações de acesso a dados específicas para cafés,
herdando a funcionalidade base de DAO e adicionando validações de tipo
específicas. Utiliza o ID do café como chave primária para indexação.

Todas as operações validam que os objetos são instâncias de Cafe e que o
ID é um inteiro antes de delegar para a classe base, garantindo integridade
de tipos e prevenindo erros de runtime.
"""

from typing import Optional

from DAOs.dao import DAO
from entidade.cafe import Cafe


class CafeDAO(DAO):
    def __init__(self):
        """
        Inicializa o DAO de cafés, configurando 'cafes.pkl' como arquivo de
        persistência e carregando os dados existentes.
        """
        super().__init__('cafes.pkl')

    def add(self, cafe: Cafe) -> None:
        """
        Adiciona um novo café ao repositório. Valida que o objeto é uma
        instância de Cafe e que possui um ID inteiro antes de persistir.
        """
        if isinstance(cafe, Cafe) and isinstance(cafe.id, int):
            super().add(cafe.id, cafe)

    def update(self, cafe: Cafe) -> None:
        """
        Atualiza um café existente no repositório. Valida tipos antes de
        delegar para a classe base, garantindo que apenas cafés válidos
        sejam atualizados.
        """
        if isinstance(cafe, Cafe) and isinstance(cafe.id, int):
            super().update(cafe.id, cafe)

    def get(self, key: int) -> Optional[Cafe]:
        """
        Recupera um café pelo ID. Retorna None se não encontrado, permitindo
        verificação de existência sem exceções.
        """
        if isinstance(key, int):
            return super().get(key)
        return None

    def remove(self, key: int) -> None:
        """
        Remove um café do repositório pelo ID. Valida que a chave é um inteiro
        antes de tentar remover.
        """
        if isinstance(key, int):
            super().remove(key)
