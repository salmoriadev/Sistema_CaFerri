"""
Representa uma máquina de café como produto comercializável do sistema.

Esta classe especializa a classe abstrata Produto, adicionando a associação
com um fornecedor de máquinas (FornecedoraMaquina). Herda todas as
características comerciais básicas (ID, nome, preços, data de fabricação)
e estabelece vínculo com a empresa que fornece a máquina.

Utilizada em operações de estoque, vendas e relatórios, permitindo rastreamento
da origem de cada máquina e análise de fornecedores mais ativos no sistema.
"""


from entidade.produto import Produto
from entidade.fornecedora_maquina import FornecedoraMaquina


class MaquinaDeCafe(Produto):
    def __init__(self, nome: str, preco_compra: float,
                 preco_venda: float, id: int, data_fabricacao: str,
                 empresa_fornecedora: FornecedoraMaquina) -> None:
        """
        Inicializa uma máquina de café com dados comerciais básicos (herdados
        de Produto) e associação com fornecedor de máquinas. Estabelece vínculo
        necessário para rastreamento de origem e análises de fornecedores.
        """
        super().__init__(nome, preco_compra, preco_venda, id, data_fabricacao)
        self.__empresa_fornecedora = empresa_fornecedora

    @property
    def empresa_fornecedora(self) -> FornecedoraMaquina:
        return self.__empresa_fornecedora

    @empresa_fornecedora.setter
    def empresa_fornecedora(self, nova_empresa: FornecedoraMaquina) -> None:
        self.__empresa_fornecedora = nova_empresa
