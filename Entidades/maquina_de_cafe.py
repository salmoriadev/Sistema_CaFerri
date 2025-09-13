from produto import Produto
class MaquinaDeCafe(Produto):
    def __init__(self, nome: str, preco_compra: float, preco_venda: float, estoque: int, id: int, data_fabricacao: str, modelo: str):
        super().__init__(nome, preco_compra, preco_venda, estoque, id, data_fabricacao)
        self.__modelo = modelo

    @property
    def modelo(self):
        return self.__modelo
    
    @modelo.setter
    def modelo(self, novo_modelo: str):
        self.__modelo = novo_modelo