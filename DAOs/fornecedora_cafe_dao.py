from typing import Optional

from DAOs.dao import DAO
from entidade.fornecedora_cafe import FornecedoraCafe


class FornecedoraCafeDAO(DAO):
    def __init__(self):
        super().__init__('fornecedores_cafe.pkl')

    def add(self, fornecedor: FornecedoraCafe) -> None:
        if isinstance(fornecedor, FornecedoraCafe) and isinstance(fornecedor.cnpj, str):
            super().add(fornecedor.cnpj, fornecedor)

    def update(self, fornecedor: FornecedoraCafe) -> None:
        if isinstance(fornecedor, FornecedoraCafe) and isinstance(fornecedor.cnpj, str):
            super().update(fornecedor.cnpj, fornecedor)

    def get(self, key: str) -> Optional[FornecedoraCafe]:
        if isinstance(key, str):
            return super().get(key)
        return None

    def remove(self, key: str) -> None:
        if isinstance(key, str):
            super().remove(key)
