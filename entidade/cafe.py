from entidade.produto import Produto
from entidade.perfil_consumidor import PerfilConsumidor
class Cafe(Produto):
    def __init__(self, nome: str, preco_compra: float, preco_venda: float,
                  estoque: int, id: int, data_fabricacao: str, origem: str, variedade: str, altitude: int, moagem: str, notas_sensoriais: str, perfil_recomendado: str):
        super().__init__(nome, preco_compra, preco_venda, estoque, id, data_fabricacao)
        self.__origem = origem
        self.__variedade = variedade
        self.__altitude = altitude
        self.__moagem = moagem
        self.__notas_sensoriais = notas_sensoriais
        self.__perfil_recomendado = PerfilConsumidor(perfil_recomendado)

    @property
    def origem(self):
        return self.__origem

    @property
    def variedade(self):
        return self.__variedade
    @property
    def altitude(self):   
        return self.__altitude

    @property
    def moagem(self):
        return self.__moagem

    @property
    def notas_sensoriais(self):
        return self.__notas_sensoriais

    @property
    def perfil_recomendado(self):
        return self.__perfil_recomendado
    
    @perfil_recomendado.setter
    def perfil_recomendado(self, perfil: PerfilConsumidor):
        self.__perfil_recomendado = perfil
    
    @moagem.setter
    def moagem(self, tipo_moagem: str):
        self.__moagem = tipo_moagem

    @notas_sensoriais.setter
    def notas_sensoriais(self, notas: str):
        self.__notas_sensoriais = notas
