from typing import Optional

from DAOs.dao import DAO
from entidade.maquina_de_cafe import MaquinaDeCafe


class MaquinaDeCafeDAO(DAO):
    def __init__(self):
        super().__init__('maquinas.pkl')

    def add(self, maquina: MaquinaDeCafe) -> None:
        if isinstance(maquina, MaquinaDeCafe) and isinstance(maquina.id, int):
            super().add(maquina.id, maquina)

    def update(self, maquina: MaquinaDeCafe) -> None:
        if isinstance(maquina, MaquinaDeCafe) and isinstance(maquina.id, int):
            super().update(maquina.id, maquina)

    def get(self, key: int) -> Optional[MaquinaDeCafe]:
        if isinstance(key, int):
            return super().get(key)
        return None

    def remove(self, key: int) -> None:
        if isinstance(key, int):
            super().remove(key)

