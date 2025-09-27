import hashlib
from entidade.perfil_consumidor import PerfilConsumidor


class Cliente:
    def __init__(self, id, nome, email, senha_cifrada, saldo, perfil: str):
        self.__id = id
        self.__nome = nome
        self.__email = email
        self.__senha_cifrada = senha_cifrada
        self.__saldo = saldo
        self.__perfil_do_consumidor = PerfilConsumidor(perfil)
        self.__lista_cafes_recomendados = self.__perfil_do_consumidor.recomendar_cafes()

    @property
    def id(self):
        return self.__id
    @property
    def nome(self):
        return self.__nome
    @property
    def email(self):
        return self.__email
    @property
    def saldo(self):
        return self.__saldo
    @property
    def perfil_do_consumidor(self):
        return self.__perfil_do_consumidor
    @property
    def lista_cafes_recomendados(self):
        return self.__lista_cafes_recomendados
    
    @property
    def senha_cifrada(self):
        return self.__senha_cifrada
    
    @id.setter
    def id(self, novo_id: int):
        self.__id = novo_id
    
    @nome.setter
    def nome(self, novo_nome: str):
        self.__nome = novo_nome
    
    @email.setter
    def email(self, novo_email: str):
        self.__email = novo_email
    
    @senha_cifrada.setter
    def senha_cifrada(self, nova_senha: str):
        self.__senha_cifrada = nova_senha

    @saldo.setter
    def saldo(self, valor):
        self.__saldo = valor

    @perfil_do_consumidor.setter
    def perfil_do_consumidor(self, perfil: str):
        self.__perfil_do_consumidor = PerfilConsumidor(perfil)
        self.__lista_cafes_recomendados = perfil.recomendar_cafes()

    @property
    def lista_cafes_recomendados(self):
        return self.__lista_cafes_recomendados
