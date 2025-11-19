"""
DAO especializado para persistência de entidades FornecedoraCafe.

Este módulo implementa operações de acesso a dados específicas para
fornecedores de café, herdando a funcionalidade base de DAO e adicionando
validações de tipo específicas. Utiliza o CNPJ como chave primária para
indexação, garantindo unicidade por identificador legal.

Todas as operações validam que os objetos são instâncias de FornecedoraCafe
e que o CNPJ é uma string antes de delegar para a classe base, garantindo
integridade de tipos e prevenindo erros de runtime.
"""

from typing import Optional

from DAOs.dao import DAO
from entidade.fornecedora_cafe import FornecedoraCafe


class FornecedoraCafeDAO(DAO):
    def __init__(self):
        """
        Inicializa o DAO de fornecedores de café, configurando
        'fornecedores_cafe.pkl' como arquivo de persistência e carregando
        os dados existentes.
        """
        super().__init__('fornecedores_cafe.pkl')

    def add(self, fornecedor: FornecedoraCafe) -> None:
        """
        Adiciona um novo fornecedor de café ao repositório. Valida que o
        objeto é uma instância de FornecedoraCafe e que possui um CNPJ
        string antes de persistir.
        """
        if isinstance(fornecedor, FornecedoraCafe) and isinstance(fornecedor.cnpj, str):
            super().add(fornecedor.cnpj, fornecedor)

    def update(self, fornecedor: FornecedoraCafe) -> None:
        """
        Atualiza um fornecedor de café existente no repositório. Valida tipos
        antes de delegar para a classe base, garantindo que apenas fornecedores
        válidos sejam atualizados.
        """
        if isinstance(fornecedor, FornecedoraCafe) and isinstance(fornecedor.cnpj, str):
            super().update(fornecedor.cnpj, fornecedor)

    def get(self, key: str) -> Optional[FornecedoraCafe]:
        """
        Recupera um fornecedor de café pelo CNPJ. Retorna None se não
        encontrado, permitindo verificação de existência sem exceções.
        """
        if isinstance(key, str):
            return super().get(key)
        return None

    def remove(self, key: str) -> None:
        """
        Remove um fornecedor de café do repositório pelo CNPJ. Valida que
        a chave é uma string antes de tentar remover.
        """
        if isinstance(key, str):
            super().remove(key)
