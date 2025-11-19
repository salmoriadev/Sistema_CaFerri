"""
DAO especializado para persistência de entidades Cliente.

Este módulo implementa operações de acesso a dados específicas para clientes,
herdando a funcionalidade base de DAO e adicionando validações de tipo
específicas. Utiliza o ID do cliente como chave primária para indexação.

Todas as operações validam que os objetos são instâncias de Cliente e que o
ID é um inteiro antes de delegar para a classe base, garantindo integridade
de tipos e prevenindo erros de runtime.
"""

from typing import Optional

from DAOs.dao import DAO
from entidade.cliente import Cliente


class ClienteDAO(DAO):
    def __init__(self):
        """
        Inicializa o DAO de clientes, configurando 'clientes.pkl' como arquivo
        de persistência e carregando os dados existentes.
        """
        super().__init__('clientes.pkl')

    def add(self, cliente: Cliente) -> None:
        """
        Adiciona um novo cliente ao repositório. Valida que o objeto é uma
        instância de Cliente e que possui um ID inteiro antes de persistir.
        """
        if isinstance(cliente, Cliente) and isinstance(cliente.id, int):
            super().add(cliente.id, cliente)

    def update(self, cliente: Cliente) -> None:
        """
        Atualiza um cliente existente no repositório. Valida tipos antes de
        delegar para a classe base, garantindo que apenas clientes válidos
        sejam atualizados.
        """
        if isinstance(cliente, Cliente) and isinstance(cliente.id, int):
            super().update(cliente.id, cliente)

    def get(self, key: int) -> Optional[Cliente]:
        """
        Recupera um cliente pelo ID. Retorna None se não encontrado, permitindo
        verificação de existência sem exceções.
        """
        if isinstance(key, int):
            return super().get(key)
        return None

    def remove(self, key: int) -> None:
        """
        Remove um cliente do repositório pelo ID. Valida que a chave é um
        inteiro antes de tentar remover.
        """
        if isinstance(key, int):
            super().remove(key)
