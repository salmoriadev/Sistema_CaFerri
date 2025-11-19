"""
DAO especializado para persistência de entidades FornecedoraMaquina.

Este módulo implementa operações de acesso a dados específicas para
fornecedores de máquinas de café, herdando a funcionalidade base de DAO e
adicionando validações de tipo específicas. Utiliza o CNPJ como chave
primária para indexação, garantindo unicidade por identificador legal.

Todas as operações validam que os objetos são instâncias de FornecedoraMaquina
e que o CNPJ é uma string antes de delegar para a classe base, garantindo
integridade de tipos e prevenindo erros de runtime.
"""

from typing import Optional

from DAOs.dao import DAO
from entidade.fornecedora_maquina import FornecedoraMaquina


class FornecedoraMaquinaDAO(DAO):
    def __init__(self):
        """
        Inicializa o DAO de fornecedores de máquinas, configurando
        'fornecedores_maquina.pkl' como arquivo de persistência e carregando
        os dados existentes.
        """
        super().__init__('fornecedores_maquina.pkl')

    def add(self, fornecedor: FornecedoraMaquina) -> None:
        """
        Adiciona um novo fornecedor de máquinas ao repositório. Valida que o
        objeto é uma instância de FornecedoraMaquina e que possui um CNPJ
        string antes de persistir.
        """
        if isinstance(fornecedor, FornecedoraMaquina) and isinstance(fornecedor.cnpj, str):
            super().add(fornecedor.cnpj, fornecedor)

    def update(self, fornecedor: FornecedoraMaquina) -> None:
        """
        Atualiza um fornecedor de máquinas existente no repositório. Valida
        tipos antes de delegar para a classe base, garantindo que apenas
        fornecedores válidos sejam atualizados.
        """
        if isinstance(fornecedor, FornecedoraMaquina) and isinstance(fornecedor.cnpj, str):
            super().update(fornecedor.cnpj, fornecedor)

    def get(self, key: str) -> Optional[FornecedoraMaquina]:
        """
        Recupera um fornecedor de máquinas pelo CNPJ. Retorna None se não
        encontrado, permitindo verificação de existência sem exceções.
        """
        if isinstance(key, str):
            return super().get(key)
        return None

    def remove(self, key: str) -> None:
        """
        Remove um fornecedor de máquinas do repositório pelo CNPJ. Valida que
        a chave é uma string antes de tentar remover.
        """
        if isinstance(key, str):
            super().remove(key)
