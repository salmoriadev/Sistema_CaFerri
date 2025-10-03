import datetime
from entidade.cliente import Cliente
from entidade.produto import Produto
from entidade.estoque import Estoque
class Venda:
    def __init__ (self, id_venda: int, cliente: Cliente, produto: Produto,):
        self.__id_venda = id_venda
        self.__cliente = cliente
        self.__data_venda = None
        self.__valor_total = produto.preco_venda
        self.__produtos = [ produto ]
        self.__status_venda = "Em andamento"

    def adicionar_produto(self, produto: Produto, quantidade: int):
        for _ in range(quantidade):
            self.__produtos.append(produto)
        self.__valor_total += produto.preco_venda * quantidade

    def remover_produto(self, produto: Produto):
        if produto in self.__produtos:
            self.__produtos.remove(produto)
            self.__valor_total -= produto.preco_venda
        else:
            return "Produto não encontrado na venda."
    
    def listar_produtos(self):
        return self.__produtos
    
    def finalizar_venda(self, estoque: Estoque):
        produtos_estoque = estoque.listar_produtos()
        if self.__cliente.saldo < self.__valor_total:
            return "Saldo insuficiente para finalizar a compra."
        for produto in self.__produtos:
            if produto not in produtos_estoque or produtos_estoque[produto] < 1:
                return f"Produto {produto.nome} está fora de estoque."
        for produto in self.__produtos:
            estoque.retirar_estoque(produto, 1)
        self.__cliente.saldo -= self.__valor_total
        self.__data_venda = datetime.datetime.now()
        self.__status_venda = "Finalizada"
        return "Venda finalizada com sucesso."
    
    @property
    def id_venda(self):
        return self.__id_venda
    
    @property
    def cliente(self):
        return self.__cliente
    
    @property
    def data_venda(self):
        return self.__data_venda
    
    @property
    def valor_total(self):
        return self.__valor_total
        
    @property
    def status_venda(self):
        return self.__status_venda