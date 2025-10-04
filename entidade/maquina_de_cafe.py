from entidade.produto import Produto
class MaquinaDeCafe(Produto):
    def __init__(self, nome: str, preco_compra: float, preco_venda: float, id: int, data_fabricacao: str) -> None:
        super().__init__(nome, preco_compra, preco_venda, id, data_fabricacao)
