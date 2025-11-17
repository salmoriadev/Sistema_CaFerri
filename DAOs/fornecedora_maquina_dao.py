from typing import Optional

from DAOs.dao import DAO
from entidade.fornecedora_maquina import FornecedoraMaquina


class FornecedoraMaquinaDAO(DAO):
    def __init__(self):
        super().__init__('fornecedores_maquina.pkl')

    def add(self, fornecedor: FornecedoraMaquina) -> None:
        if isinstance(fornecedor, FornecedoraMaquina) and isinstance(fornecedor.cnpj, str):
            super().add(fornecedor.cnpj, fornecedor)

    def update(self, fornecedor: FornecedoraMaquina) -> None:
        if isinstance(fornecedor, FornecedoraMaquina) and isinstance(fornecedor.cnpj, str):
            super().update(fornecedor.cnpj, fornecedor)

    def get(self, key: str) -> Optional[FornecedoraMaquina]:
        if isinstance(key, str):
            return super().get(key)
        return None

    def remove(self, key: str) -> None:
        if isinstance(key, str):
            super().remove(key)

