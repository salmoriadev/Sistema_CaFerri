from abc import ABC, abstractmethod
from datetime import date

class Produto(ABC):
    @abstractmethod
    def __init__(self, nome: str, preco_compra: float, preco_venda: float, estoque: int, id: int, data_fabricacao: str):
        self.__id = id
        self.__nome = nome
        self.__preco_compra = preco_compra
        self.__preco_venda = preco_venda
        self.__estoque = estoque
        self.__data_fabricacao = data_fabricacao

    @property
    def id(self):
        return self.__id
    
    @property
    def nome(self):
        return self.__nome

    @property
    def preco_compra(self):
        return self.__preco_compra

    @property
    def preco_venda(self):
        return self.__preco_venda

    @property
    def estoque(self):
        return self.__estoque
    
    @estoque.setter
    def estoque(self, novo_estoque: int):
        self.__estoque = novo_estoque

    @property
    def data_fabricacao(self):
        return self.__data_fabricacao

    def calcular_lucro(self):
        return self.__preco_venda - self.__preco_compra

    def atualizar_preco(self, novo_preco: float):
        self.__preco_venda = novo_preco