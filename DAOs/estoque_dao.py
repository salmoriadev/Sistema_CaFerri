"""
DAO especializado para persistência do estado do estoque.

Este módulo gerencia a persistência do inventário de produtos usando uma
estrutura de dados diferente dos outros DAOs. Ao invés de armazenar objetos
completos, armazena um dicionário que mapeia IDs de produtos para quantidades,
otimizando o armazenamento e facilitando a serialização.

Utiliza uma chave fixa ('ESTOQUE') para armazenar todo o estado do estoque
em uma única entrada no cache, simplificando o gerenciamento e garantindo
que apenas um estado de estoque exista por vez.
"""

from typing import Dict

from DAOs.dao import DAO


class EstoqueDAO(DAO):
    _CHAVE = 'ESTOQUE'

    def __init__(self):
        """
        Inicializa o DAO de estoque, configurando 'estoque.pkl' como arquivo
        de persistência e carregando o estado existente.
        """
        super().__init__('estoque.pkl')

    def salvar(self, itens: Dict[int, int]) -> None:
        """
        Persiste o estado completo do estoque. Recebe um dicionário mapeando
        IDs de produtos para quantidades e armazena usando a chave fixa.
        """
        super().add(self._CHAVE, itens)

    def carregar(self) -> Dict[int, int]:
        """
        Carrega o estado completo do estoque do arquivo. Converte todas as
        chaves e valores para inteiros, garantindo tipos consistentes mesmo
        se os dados foram salvos com tipos diferentes. Retorna dicionário
        vazio se não houver dados salvos.
        """
        dados_estoque = super().get(self._CHAVE)
        if isinstance(dados_estoque, dict):
            return {int(k): int(v) for k, v in dados_estoque.items()}
        return {}
