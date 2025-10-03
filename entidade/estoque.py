from entidade.produto import Produto
from entidade.cafe import Cafe
class Estoque:
    def __init__(self):
        self.__produtos = dict()
        self.cafes = []

    def adicionar_produto(self, produto: Produto, quantidade: int):
        self.__produtos[produto] = quantidade
        if isinstance(produto, Cafe):
            self.cafes.append(produto)

    def tirar_do_estoque(self, produto: Produto):
        if produto in self.__produtos:
            del self.__produtos[produto]
        if isinstance(produto, Cafe):
            self.cafes.remove(produto)

    def listar_produtos(self):
        return self.__produtos

    def adicionar_estoque(self, produto: Produto, quantidade: int):
        if produto in self.__produtos:
            self.__produtos[produto] += quantidade
        else:
            self.__produtos[produto] = quantidade

    def retirar_estoque(self, produto: Produto, quantidade: int):
        if produto in self.__produtos and self.__produtos[produto] >= quantidade:
            self.__produtos[produto] -= quantidade
        else:
            return "Estoque insuficiente ou produto não encontrado."