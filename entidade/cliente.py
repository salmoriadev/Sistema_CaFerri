import hashlib
from entidade.perfil_consumidor import PerfilConsumidor
class Cliente:
    def __init__(self, id, nome, email, senha, saldo, perfil: str):
        self.__id = id
        self.__nome = nome
        self.__email = email
        self.__senha = hashlib.sha256(senha.encode('utf-8')).hexdigest()
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
    
    @saldo.setter
    def saldo(self, valor):
        self.__saldo = valor

    @perfil_do_consumidor.setter
    def perfil_do_consumidor(self, perfil: str):
        self.__perfil_do_consumidor = PerfilConsumidor(perfil)
        self.__lista_cafes_recomendados = perfil.recomendar_cafes()

    
    def mostrar_recomendacoes(self):
        return self.__lista_cafes_recomendados

    def exibir_informacoes(self):
        return f"Nome: {self.__nome}, Email: {self.__email}, Saldo: {self.__saldo}, Perfil do Consumidor: {self.__perfil_do_consumidor.perfil}, Cafés Recomendados: {self.__lista_cafes_recomendados}"