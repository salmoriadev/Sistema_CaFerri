"""
DAO especializado para persistência de entidades Venda.

Este módulo implementa operações de acesso a dados específicas para vendas,
herdando a funcionalidade base de DAO e adicionando validações de tipo
específicas. Utiliza o ID da venda (id_venda) como chave primária para
indexação, diferente dos outros DAOs que usam apenas 'id'.

Todas as operações validam que os objetos são instâncias de Venda e que o
id_venda é um inteiro antes de delegar para a classe base, garantindo
integridade de tipos e prevenindo erros de runtime.
"""

from typing import Optional

from DAOs.dao import DAO
from entidade.venda import Venda


class VendaDAO(DAO):
    def __init__(self):
        """
        Inicializa o DAO de vendas, configurando 'vendas.pkl' como arquivo
        de persistência e carregando os dados existentes.
        """
        super().__init__('vendas.pkl')

    def add(self, venda: Venda) -> None:
        """
        Adiciona uma nova venda ao repositório. Valida que o objeto é uma
        instância de Venda e que possui um id_venda inteiro antes de persistir.
        """
        if isinstance(venda, Venda) and isinstance(venda.id_venda, int):
            super().add(venda.id_venda, venda)

    def update(self, venda: Venda) -> None:
        """
        Atualiza uma venda existente no repositório. Valida tipos antes de
        delegar para a classe base, garantindo que apenas vendas válidas
        sejam atualizadas.
        """
        if isinstance(venda, Venda) and isinstance(venda.id_venda, int):
            super().update(venda.id_venda, venda)

    def get(self, key: int) -> Optional[Venda]:
        """
        Recupera uma venda pelo ID. Retorna None se não encontrada, permitindo
        verificação de existência sem exceções.
        """
        if isinstance(key, int):
            return super().get(key)
        return None

    def remove(self, key: int) -> None:
        """
        Remove uma venda do repositório pelo ID. Valida que a chave é um
        inteiro antes de tentar remover.
        """
        if isinstance(key, int):
            super().remove(key)
