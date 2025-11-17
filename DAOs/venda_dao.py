from typing import Optional

from DAOs.dao import DAO
from entidade.venda import Venda


class VendaDAO(DAO):
    def __init__(self):
        super().__init__('vendas.pkl')

    def add(self, venda: Venda) -> None:
        if isinstance(venda, Venda) and isinstance(venda.id_venda, int):
            super().add(venda.id_venda, venda)

    def update(self, venda: Venda) -> None:
        if isinstance(venda, Venda) and isinstance(venda.id_venda, int):
            super().update(venda.id_venda, venda)

    def get(self, key: int) -> Optional[Venda]:
        if isinstance(key, int):
            return super().get(key)
        return None

    def remove(self, key: int) -> None:
        if isinstance(key, int):
            super().remove(key)
