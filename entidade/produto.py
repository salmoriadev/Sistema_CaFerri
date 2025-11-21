"""
Classe base abstrata para todos os produtos comercializáveis do sistema.

Este módulo define a interface comum que todos os produtos (cafés e máquinas)
devem implementar. Estabelece atributos fundamentais de comercialização como
ID único, nome, preços de compra e venda, e data de fabricação. Fornece
métodos utilitários para cálculo de lucro e atualização de preços.

A abstração permite que o sistema trate cafés e máquinas de forma uniforme
em operações de estoque, vendas e relatórios, enquanto mantém flexibilidade
para características específicas de cada tipo de produto.
"""

from abc import ABC, abstractmethod


class Produto(ABC):
    @abstractmethod
    def __init__(self, nome: str, preco_compra: float,
                 preco_venda: float, id: int, data_fabricacao: str) -> None:
        """
        Inicializa um produto com dados básicos de comercialização. Método
        abstrato que deve ser implementado por classes filhas (Cafe, MaquinaDeCafe).
        """
        self.__id = id
        self.__nome = nome
        self.__preco_compra = preco_compra
        self.__preco_venda = preco_venda
        self.__data_fabricacao = data_fabricacao

    @property
    def id(self) -> int:
        """Retorna o identificador único do produto."""
        return self.__id

    @property
    def nome(self) -> str:
        """Retorna o nome do produto."""
        return self.__nome

    @property
    def preco_compra(self) -> float:
        """Retorna o preço de compra do produto (custo)."""
        return self.__preco_compra

    @property
    def preco_venda(self) -> float:
        """Retorna o preço de venda do produto."""
        return self.__preco_venda

    @property
    def data_fabricacao(self) -> str:
        """Retorna a data de fabricação no formato DD/MM/AAAA."""
        return self.__data_fabricacao

    def calcular_lucro(self) -> float:
        """
        Calcula o lucro unitário do produto (diferença entre preço de venda
        e preço de compra). Usado para análises de rentabilidade.
        """
        return self.__preco_venda - self.__preco_compra

    def atualizar_preco(self, novo_preco: float) -> None:
        """
        Atualiza o preço de venda do produto. Usado para ajustes de preço
        sem necessidade de recriar o objeto.
        """
        if novo_preco < 0:
            raise ValueError("O preço não pode ser negativo.")
        self.__preco_venda = novo_preco

    @data_fabricacao.setter
    def data_fabricacao(self, nova_data: str) -> None:
        self.__data_fabricacao = nova_data

    @nome.setter
    def nome(self, novo_nome: str) -> None:
        self.__nome = novo_nome

    @preco_compra.setter
    def preco_compra(self, novo_preco_compra: float) -> None:
        if novo_preco_compra < 0:
            raise ValueError("O preço de compra não pode ser negativo.")
        self.__preco_compra = novo_preco_compra

    @preco_venda.setter
    def preco_venda(self, novo_preco_venda: float) -> None:
        if novo_preco_venda < 0:
            raise ValueError("O preço de venda não pode ser negativo.")
        self.__preco_venda = novo_preco_venda

    @id.setter
    def id(self, novo_id: int) -> None:
        if novo_id < 0:
            raise ValueError("O ID não pode ser negativo.")
        self.__id = novo_id
