import datetime
from entidade.cliente import Cliente
from entidade.produto import Produto
from entidade.estoque import Estoque

class Venda:
    def __init__(self, id_venda: int, cliente: Cliente) -> None:
        self.__id_venda = id_venda
        self.__cliente = cliente
        self.__data_venda = None
        self.__valor_total = 0.0
        self.__carrinho = {}
        self.__status_venda = "Em andamento"

    def adicionar_produto(self, produto: Produto, quantidade: int) -> None:
        if quantidade <= 0:
            return

        self.__carrinho[produto] = self.__carrinho.get(produto, 0) + quantidade
        self.__valor_total += produto.preco_venda * quantidade

    def remover_produto(self, produto: Produto) -> None:
        if produto in self.__carrinho:
            quantidade_removida = self.__carrinho.pop(produto)
            self.__valor_total -= produto.preco_venda * quantidade_removida

    def listar_produtos_formatado(self) -> list[dict]:
        if not self.__carrinho:
            return []
        
        lista_formatada = []
        for produto, quantidade in self.__carrinho.items():
            lista_formatada.append({
                "nome": produto.nome,
                "quantidade": quantidade,
                "preco_unitario": f"R$ {produto.preco_venda:.2f}",
                "subtotal": f"R$ {produto.preco_venda * quantidade:.2f}"
            })
        return lista_formatada
    
    def finalizar_venda(self, estoque: Estoque) -> str:
        if self.__status_venda != "Em andamento":
            return "ERRO: Esta venda não está mais em andamento."
        if self.__cliente.saldo < self.__valor_total:
            return f"ERRO: Saldo insuficiente. Saldo: R$ {self.__cliente.saldo:.2f}, Valor da Compra: R$ {self.__valor_total:.2f}"
        for produto, quantidade_necessaria in self.__carrinho.items():
            produtos_em_estoque = estoque.listar_produtos()
            if produto not in produtos_em_estoque:
                return f"ERRO: O produto '{produto.nome}' não consta no estoque."
            if produtos_em_estoque[produto] < quantidade_necessaria:
                return f"ERRO: Estoque insuficiente para '{produto.nome}'. Necessário: {quantidade_necessaria}, Disponível: {produtos_em_estoque[produto]}."
        for produto, quantidade_necessaria in self.__carrinho.items():
            estoque.retirar_quantidade(produto, quantidade_necessaria)
        self.__cliente.saldo -= self.__valor_total
        self.__data_venda = datetime.datetime.now()
        self.__status_venda = "Finalizada"
        return "Venda finalizada com sucesso!"
    
    @property
    def id_venda(self) -> int:
        return self.__id_venda
    
    @property
    def cliente(self) -> Cliente:
        return self.__cliente
    
    @property
    def data_venda(self) -> datetime.datetime:
        return self.__data_venda
    
    @property
    def valor_total(self) -> float:
        return self.__valor_total
        
    @property
    def status_venda(self) -> str:
        return self.__status_venda