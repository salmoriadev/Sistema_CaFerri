from typing import Dict

from DAOs.dao import DAO


class EstoqueDAO(DAO):
    _CHAVE = 'ESTOQUE'

    def __init__(self):
        super().__init__('estoque.pkl')

    def salvar(self, itens: Dict[int, int]) -> None:
        super().add(self._CHAVE, itens)

    def carregar(self) -> Dict[int, int]:
        dados = super().get(self._CHAVE)
        if isinstance(dados, dict):
            return {int(k): int(v) for k, v in dados.items()}
        return {}
