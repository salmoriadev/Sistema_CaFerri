"""
    Gerencia o inventário de todos os produtos do sistema.

    Esta classe atua como um repositório centralizado para o controle de
    quantidades de produtos. Ela utiliza um dicionário (`__produtos_em_estoque`)
    para mapear objetos `Produto` (sejam `Cafe` ou `MaquinaDeCafe`) às suas
    respectivas quantidades disponíveis.
    """

from entidade.produto import Produto

class Estoque:
    def __init__(self) -> None:
        self.__produtos_em_estoque = {}
    
    @property
    def produtos_em_estoque(self) -> dict:
        return self.__produtos_em_estoque

    def produto_ja_existe(self, produto: Produto) -> bool:
        return produto in self.__produtos_em_estoque

    def cadastrar_novo_produto(self, produto: Produto, quantidade: int) -> None:
        if not self.produto_ja_existe(produto):
            self.__produtos_em_estoque[produto] = quantidade

    def adicionar_quantidade(self, produto: Produto, quantidade_a_adicionar: int) -> None:
        if self.produto_ja_existe(produto):
            self.__produtos_em_estoque[produto] += quantidade_a_adicionar

    def retirar_quantidade(self, produto: Produto, quantidade_a_retirar: int) -> None:
        if not self.produto_ja_existe(produto):
            return "ERRO: Produto não encontrado no estoque."
        
        if self.__produtos_em_estoque[produto] >= quantidade_a_retirar:
            self.__produtos_em_estoque[produto] -= quantidade_a_retirar
            return None
        else:
            return "ERRO: Estoque insuficiente."

    def listar_produtos(self) -> dict:
        return self.__produtos_em_estoque