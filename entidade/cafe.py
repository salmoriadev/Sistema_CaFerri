from entidade.produto import Produto
from entidade.perfil_consumidor import PerfilConsumidor

class Cafe(Produto):
    def __init__(self, nome: str, preco_compra: float, preco_venda: float,
                 id: int, data_fabricacao: str, origem: str, variedade: str, 
                 altitude: int, moagem: str, notas_sensoriais: str, perfil_recomendado: str) -> None:
        super().__init__(nome, preco_compra, preco_venda, id, data_fabricacao)
        self.__origem = origem
        self.__variedade = variedade
        self.__altitude = altitude
        self.__moagem = moagem
        self.__notas_sensoriais = notas_sensoriais
        self.__perfil_recomendado = PerfilConsumidor(perfil_recomendado)

    @property
    def origem(self) -> str:
        return self.__origem

    @property
    def variedade(self) -> str:
        return self.__variedade

    @property
    def altitude(self) -> int:
        return self.__altitude

    @property
    def moagem(self) -> str:
        return self.__moagem

    @property
    def notas_sensoriais(self) -> str:
        return self.__notas_sensoriais

    @property
    def perfil_recomendado(self) -> PerfilConsumidor:
        return self.__perfil_recomendado
    
    @perfil_recomendado.setter
    def perfil_recomendado(self, perfil: str) -> None:
        self.__perfil_recomendado = PerfilConsumidor(perfil)
    
    @moagem.setter
    def moagem(self, tipo_moagem: str) -> None:
        self.__moagem = tipo_moagem

    @notas_sensoriais.setter
    def notas_sensoriais(self, notas: str) -> None:
        self.__notas_sensoriais = notas

    @altitude.setter
    def altitude(self, nova_altitude: int) -> None:
        self.__altitude = nova_altitude
    
    @variedade.setter
    def variedade(self, nova_variedade: str) -> None:
        self.__variedade = nova_variedade

    @origem.setter
    def origem(self, nova_origem: str) -> None:
        self.__origem = nova_origem
