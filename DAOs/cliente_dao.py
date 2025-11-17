from typing import Optional

from DAOs.dao import DAO
from entidade.cliente import Cliente


class ClienteDAO(DAO):
    def __init__(self):
        super().__init__('clientes.pkl')

    def add(self, cliente: Cliente) -> None:
        if isinstance(cliente, Cliente) and isinstance(cliente.id, int):
            super().add(cliente.id, cliente)

    def update(self, cliente: Cliente) -> None:
        if isinstance(cliente, Cliente) and isinstance(cliente.id, int):
            super().update(cliente.id, cliente)

    def get(self, key: int) -> Optional[Cliente]:
        if isinstance(key, int):
            return super().get(key)
        return None

    def remove(self, key: int) -> None:
        if isinstance(key, int):
            super().remove(key)

