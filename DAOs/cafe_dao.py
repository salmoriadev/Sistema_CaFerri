from typing import Optional

from DAOs.dao import DAO
from entidade.cafe import Cafe


class CafeDAO(DAO):
    def __init__(self):
        super().__init__('cafes.pkl')

    def add(self, cafe: Cafe) -> None:
        if isinstance(cafe, Cafe) and isinstance(cafe.id, int):
            super().add(cafe.id, cafe)

    def update(self, cafe: Cafe) -> None:
        if isinstance(cafe, Cafe) and isinstance(cafe.id, int):
            super().update(cafe.id, cafe)

    def get(self, key: int) -> Optional[Cafe]:
        if isinstance(key, int):
            return super().get(key)
        return None

    def remove(self, key: int) -> None:
        if isinstance(key, int):
            super().remove(key)

