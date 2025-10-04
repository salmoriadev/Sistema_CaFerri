from abc import ABC, abstractmethod
class EmpresaFornecedora(ABC):
    @abstractmethod
    def __init__(self, nome: str, cnpj: str, endereco: str, telefone: str) -> None:
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