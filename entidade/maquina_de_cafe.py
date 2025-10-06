from entidade.produto import Produto
from entidade.fornecedora_maquina import FornecedoraMaquina
class MaquinaDeCafe(Produto):
    def __init__(self, nome: str, preco_compra: float, preco_venda: float, id: int, data_fabricacao: str, empresa_fornecedora: FornecedoraMaquina) -> None:
        super().__init__(nome, preco_compra, preco_venda, id, data_fabricacao)
        self.__empresa_fornecedora = empresa_fornecedora

    @property
    def empresa_fornecedora(self) -> FornecedoraMaquina:
        return self.__empresa_fornecedora

    @empresa_fornecedora.setter
    def empresa_fornecedora(self, nova_empresa: str) -> None:
        self.__empresa_fornecedora = FornecedoraMaquina(nova_empresa)
