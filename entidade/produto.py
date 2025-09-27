from abc import ABC, abstractmethod
from datetime import date

class Produto(ABC):
    @abstractmethod
    def __init__(self, nome: str, preco_compra: float, preco_venda: float, id: int, data_fabricacao: str):
        self.__id = id
        self.__nome = nome
        self.__preco_compra = preco_compra
        self.__preco_venda = preco_venda
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
    def data_fabricacao(self):
        return self.__data_fabricacao

    def calcular_lucro(self):
        return self.__preco_venda - self.__preco_compra

    def atualizar_preco(self, novo_preco: float):
        self.__preco_venda = novo_preco

    @data_fabricacao.setter
    def data_fabricacao(self, nova_data: str):
        self.__data_fabricacao = nova_data
    
    @nome.setter
    def nome(self, novo_nome: str):
        self.__nome = novo_nome
    
    @preco_compra.setter
    def preco_compra(self, novo_preco_compra: float):
        self.__preco_compra = novo_preco_compra
    
    @preco_venda.setter
    def preco_venda(self, novo_preco_venda: float):
        self.__preco_venda = novo_preco_venda
    
    @id.setter
    def id(self, novo_id: int):
        self.__id = novo_id