"""
DAO especializado para persistência de entidades MaquinaDeCafe.

Este módulo implementa operações de acesso a dados específicas para máquinas
de café, herdando a funcionalidade base de DAO e adicionando validações de
tipo específicas. Utiliza o ID da máquina como chave primária para indexação.

Todas as operações validam que os objetos são instâncias de MaquinaDeCafe e
que o ID é um inteiro antes de delegar para a classe base, garantindo
integridade de tipos e prevenindo erros de runtime.
"""

from typing import Optional

from DAOs.dao import DAO
from entidade.maquina_de_cafe import MaquinaDeCafe


class MaquinaDeCafeDAO(DAO):
    def __init__(self):
        """
        Inicializa o DAO de máquinas de café, configurando 'maquinas.pkl' como
        arquivo de persistência e carregando os dados existentes.
        """
        super().__init__('maquinas.pkl')

    def add(self, maquina: MaquinaDeCafe) -> None:
        """
        Adiciona uma nova máquina de café ao repositório. Valida que o objeto
        é uma instância de MaquinaDeCafe e que possui um ID inteiro antes de
        persistir.
        """
        if isinstance(maquina, MaquinaDeCafe) and isinstance(maquina.id, int):
            super().add(maquina.id, maquina)

    def update(self, maquina: MaquinaDeCafe) -> None:
        """
        Atualiza uma máquina de café existente no repositório. Valida tipos
        antes de delegar para a classe base, garantindo que apenas máquinas
        válidas sejam atualizadas.
        """
        if isinstance(maquina, MaquinaDeCafe) and isinstance(maquina.id, int):
            super().update(maquina.id, maquina)

    def get(self, key: int) -> Optional[MaquinaDeCafe]:
        """
        Recupera uma máquina de café pelo ID. Retorna None se não encontrada,
        permitindo verificação de existência sem exceções.
        """
        if isinstance(key, int):
            return super().get(key)
        return None

    def remove(self, key: int) -> None:
        """
        Remove uma máquina de café do repositório pelo ID. Valida que a chave
        é um inteiro antes de tentar remover.
        """
        if isinstance(key, int):
            super().remove(key)
