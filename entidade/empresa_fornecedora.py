"""
Classe base abstrata para empresas fornecedoras do sistema.

Este módulo define a interface comum que todos os fornecedores (de café e
máquinas) devem implementar. Estabelece atributos fundamentais de empresa
como nome, CNPJ (usado como chave única), endereço e telefone. Garante
consistência estrutural entre diferentes tipos de fornecedores.

A abstração permite que o sistema trate fornecedores de forma uniforme em
operações de validação e relatórios, enquanto mantém flexibilidade para
características específicas de cada tipo (tipo_cafe para fornecedores de
café, pais_de_origem para fornecedores de máquinas).
"""


from abc import ABC, abstractmethod


class EmpresaFornecedora(ABC):
    @abstractmethod
    def __init__(self, nome: str,
                 cnpj: str, endereco: str,
                 telefone: str) -> None:
        """
        Inicializa empresa fornecedora com dados básicos. Método abstrato que
        deve ser implementado por classes filhas (FornecedoraCafe, FornecedoraMaquina).
        CNPJ é usado como identificador único em todo o sistema.
        """
        self.__nome = nome
        self.__cnpj = cnpj
        self.__endereco = endereco
        self.__telefone = telefone

    @property
    def nome(self) -> str:
        return self.__nome

    @property
    def cnpj(self) -> str:
        return self.__cnpj

    @property
    def endereco(self) -> str:
        return self.__endereco

    @property
    def telefone(self) -> str:
        return self.__telefone

    @nome.setter
    def nome(self, novo_nome: str) -> None:
        self.__nome = novo_nome

    @endereco.setter
    def endereco(self, novo_endereco: str) -> None:
        self.__endereco = novo_endereco

    @telefone.setter
    def telefone(self, novo_telefone: str) -> None:
        self.__telefone = novo_telefone
