"""
    Representa a entidade 'Cliente' no sistema, encapsulando todas as
    informações e comportamentos associados a um usuário.

    Esta classe armazena dados de identificação, como `id`, `nome`, `email`,
    e credenciais de segurança (`senha_cifrada`), além de informações
    transacionais, como o `saldo` disponível para compras.

    Um de seus principais aspectos é a composição com a classe `PerfilConsumidor`.
    Ao invés de simplesmente armazenar uma string de preferência, ela mantém
    um objeto `PerfilConsumidor` completo. Essa abordagem de design permite
    que a classe `Cliente` delegue a lógica de recomendação de cafés,
    acessando-a diretamente através da propriedade `lista_cafes_recomendados`.
    Isso torna o objeto `Cliente` o ponto central para funcionalidades de
    personalização e interação com o usuário no sistema.
    """


from entidade.perfil_consumidor import PerfilConsumidor

class Cliente:
    def __init__(self, id: int, nome: str, email: str, senha_cifrada: str, saldo: float, perfil: str) -> None:
        self.__id = id
        self.__nome = nome
        self.__email = email
        self.__senha_cifrada = senha_cifrada
        self.__saldo = saldo
        self.__perfil_do_consumidor = PerfilConsumidor(perfil)

    @property
    def id(self) -> int:
        return self.__id
    
    @property
    def nome(self) -> str:
        return self.__nome
    
    @property
    def email(self) -> str:
        return self.__email
    
    @property
    def senha_cifrada(self) -> str:
        return self.__senha_cifrada
        
    @property
    def saldo(self) -> float:
        return self.__saldo
    
    @property
    def perfil_do_consumidor(self) -> PerfilConsumidor:
        return self.__perfil_do_consumidor
    
    @property
    def lista_cafes_recomendados(self) -> list[str]:
        return self.__perfil_do_consumidor.recomendar_cafes()

    @id.setter
    def id(self, novo_id: int) -> None:
        self.__id = novo_id
    
    @nome.setter
    def nome(self, novo_nome: str) -> None:
        self.__nome = novo_nome
    
    @email.setter
    def email(self, novo_email: str) -> None:
        self.__email = novo_email
    
    @senha_cifrada.setter
    def senha_cifrada(self, nova_senha: str) -> None:
        self.__senha_cifrada = nova_senha

    @saldo.setter
    def saldo(self, valor: float) -> None:
        self.__saldo = valor

    @perfil_do_consumidor.setter
    def perfil_do_consumidor(self, perfil: str) -> None:
        self.__perfil_do_consumidor = PerfilConsumidor(perfil)
