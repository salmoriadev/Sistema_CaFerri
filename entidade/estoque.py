"""
    Gerencia o inventário de todos os produtos do sistema.

    Esta classe atua como um repositório centralizado para o controle de
    quantidades de produtos. Ela utiliza um dicionário (`__produtos_em_estoque`)
    para mapear objetos `Produto` (sejam `Cafe` ou `MaquinaDeCafe`) às suas
    respectivas quantidades disponíveis.
    """

from typing import Callable, Dict, Optional

from entidade.produto import Produto
from Excecoes.estoqueInsuficienteException import EstoqueInsuficienteException
from Excecoes.produtoNaoEmEstoqueException import ProdutoNaoEmEstoqueException


class Estoque:
    def __init__(self) -> None:
        self.__produtos_em_estoque = {}
        self.__callback_alteracao: Optional[Callable[[
            Dict[Produto, int]], None]] = None

    @property
    def produtos_em_estoque(self) -> dict:
        return self.__produtos_em_estoque

    def definir_callback_alteracao(self, callback: Callable[[Dict[Produto, int]], None]) -> None:
        """Permite que o controlador registre uma função a ser chamada após qualquer mudança."""
        self.__callback_alteracao = callback

    def __notificar_alteracao(self) -> None:
        if self.__callback_alteracao:
            self.__callback_alteracao(self.__produtos_em_estoque)

    def produto_ja_existe(self, produto: Produto) -> bool:
        return produto in self.__produtos_em_estoque

    def cadastrar_novo_produto(self, produto: Produto, quantidade: int) -> None:
        if not self.produto_ja_existe(produto):
            self.__produtos_em_estoque[produto] = quantidade
            self.__notificar_alteracao()

    def adicionar_quantidade(self, produto: Produto, quantidade_a_adicionar: int) -> None:
        if self.produto_ja_existe(produto):
            self.__produtos_em_estoque[produto] += quantidade_a_adicionar
            self.__notificar_alteracao()

    def retirar_quantidade(self, produto: Produto, quantidade_a_retirar: int) -> None:
        if not self.produto_ja_existe(produto):
            raise ProdutoNaoEmEstoqueException(produto.nome)

        if self.__produtos_em_estoque[produto] >= quantidade_a_retirar:
            self.__produtos_em_estoque[produto] -= quantidade_a_retirar
            self.__notificar_alteracao()
        else:
            raise EstoqueInsuficienteException(
                produto.nome, quantidade_a_retirar, self.__produtos_em_estoque[produto])

    def remover_produto_do_estoque(self, produto: Produto) -> None:
        if self.produto_ja_existe(produto):
            del self.__produtos_em_estoque[produto]
            self.__notificar_alteracao()

    def listar_produtos(self) -> dict:
        return self.__produtos_em_estoque

    def remover_produto(self, produto: Produto) -> bool:
        if self.produto_ja_existe(produto):
            del self.__produtos_em_estoque[produto]
            self.__notificar_alteracao()
            return True
        return False
