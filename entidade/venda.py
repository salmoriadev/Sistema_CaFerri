"""
    Representa e gerencia uma transação de venda completa no sistema.

    Esta classe funciona como uma máquina de estados para uma única compra,
    controlando seu ciclo de vida desde a criação até a finalização. Ela
    encapsula todos os dados pertinentes a uma venda, incluindo o `cliente`
    associado, um `carrinho` de produtos, o `valor_total` e o `status_venda`.

    Suas principais responsabilidades são:
    - Gerenciar o carrinho de compras, permitindo adicionar, remover ou
      ajustar a quantidade de produtos.
    - Calcular dinamicamente o valor total da compra à medida que o carrinho
      é modificado.
    - Orquestrar o processo de finalização da venda (`finalizar_venda`), que
      envolve uma série de validações críticas: verificar o saldo do cliente,
      confirmar a disponibilidade de cada item no `Estoque` e garantir que a
      venda ainda esteja em andamento.
    - Executar as operações transacionais após a validação: debitar o valor
      do saldo do cliente, abater os produtos do estoque e registrar a data
      da transação, efetivamente concluindo a venda.
    """

import datetime
from typing import Optional
from entidade.cliente import Cliente
from entidade.produto import Produto
from entidade.estoque import Estoque
from Excecoes.vendaNaoEmAndamentoException import VendaNaoEmAndamentoException
from Excecoes.saldoInsuficienteException import SaldoInsuficienteException
from Excecoes.produtoNaoEmEstoqueException import ProdutoNaoEmEstoqueException
from Excecoes.estoqueInsuficienteException import EstoqueInsuficienteException


class Venda:
    def __init__(self, id_venda: int, cliente: Cliente) -> None:
        """
        Inicializa uma nova venda associada a um cliente. Cria carrinho vazio,
        define valor total como zero e status como "Em andamento". Data de
        venda permanece None até finalização, quando é registrada automaticamente.
        """
        if id_venda < 0:
            raise ValueError("O ID da venda não pode ser negativo.")
        self.__id_venda = id_venda
        self.__cliente = cliente
        self.__data_venda = None
        self.__valor_total = 0.0
        self.__carrinho = {}
        self.__status_venda = "Em andamento"

    def adicionar_produto(self, produto: Produto, quantidade: int) -> None:
        """
        Adiciona produto ao carrinho da venda. Se produto já existe, incrementa
        quantidade. Recalcula valor total automaticamente multiplicando preço
        de venda pela quantidade adicionada. Ignora quantidades negativas ou zero.
        """
        if quantidade <= 0:
            return

        self.__carrinho[produto] = self.__carrinho.get(produto, 0) + quantidade
        self.__valor_total += produto.preco_venda * quantidade

    def remover_produto(self, produto: Produto) -> None:
        """
        Remove completamente um produto do carrinho, independente da quantidade.
        Recalcula valor total subtraindo o valor do produto removido. Não faz
        nada se produto não estiver no carrinho.
        """
        if produto in self.__carrinho:
            quantidade_removida = self.__carrinho.pop(produto)
            self.__valor_total = max(0.0, self.__valor_total - produto.preco_venda * quantidade_removida)

    def listar_produtos_formatado(self) -> list[dict]:
        """
        Retorna lista formatada de produtos no carrinho com informações
        prontas para exibição (nome, quantidade, preço unitário formatado,
        subtotal formatado). Usado pela tela para exibir detalhes da venda.
        Retorna lista vazia se carrinho estiver vazio.
        """
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

    def finalizar_venda(self, estoque: Estoque) -> None:
        """
        Finaliza uma venda executando todas as validações e operações
        transacionais necessárias. Verifica que venda está em andamento,
        valida saldo do cliente, verifica disponibilidade de cada produto
        no estoque, debita valores do cliente, atualiza estoque e registra
        data de conclusão. Lança exceções específicas se alguma validação falhar.
        """
        if self.__status_venda != "Em andamento":
            raise VendaNaoEmAndamentoException()
        if not self.__carrinho:
            raise ValueError("Não é possível finalizar uma venda com carrinho vazio.")
        if self.__cliente.saldo < self.__valor_total:
            raise SaldoInsuficienteException()
        for produto, quantidade_necessaria in self.__carrinho.items():
            produtos_em_estoque = estoque.listar_produtos()
            if produto not in produtos_em_estoque:
                raise ProdutoNaoEmEstoqueException(produto.nome)
            if produtos_em_estoque[produto] < quantidade_necessaria:
                raise EstoqueInsuficienteException(
                    produto.nome, quantidade_necessaria, produtos_em_estoque[produto])
        for produto, quantidade_necessaria in self.__carrinho.items():
            estoque.retirar_quantidade(produto, quantidade_necessaria)
        self.__cliente.saldo -= self.__valor_total
        self.__data_venda = datetime.datetime.now()
        self.__status_venda = "Finalizada"

    def diminuir_quantidade_produto(self, produto: Produto, quantidade: int) -> str:
        """
        Reduz quantidade de um produto no carrinho. Se quantidade a remover
        for maior ou igual à quantidade atual, remove produto completamente.
        Recalcula valor total e retorna mensagem descritiva da operação
        realizada. Retorna mensagem de erro se produto não estiver no carrinho.
        """
        if quantidade <= 0:
            return "A quantidade a ser removida deve ser positiva."

        if produto in self.__carrinho:
            quantidade_atual = self.__carrinho[produto]

            if quantidade >= quantidade_atual:
                self.remover_produto(produto)
                return f"Todas as unidades de '{produto.nome}' foram removidas do carrinho."
            else:
                self.__carrinho[produto] -= quantidade
                self.__valor_total = max(0.0, self.__valor_total - produto.preco_venda * quantidade)
                return f"{quantidade} unidade(s) de '{produto.nome}' foram removidas."
        else:
            return f"ERRO: O produto '{produto.nome}' não está no carrinho."

    @property
    def id_venda(self) -> int:
        return self.__id_venda

    @property
    def cliente(self) -> Cliente:
        return self.__cliente

    @property
    def data_venda(self) -> Optional[datetime.datetime]:
        return self.__data_venda

    @property
    def valor_total(self) -> float:
        return self.__valor_total

    @property
    def status_venda(self) -> str:
        return self.__status_venda

    @property
    def carrinho(self) -> dict:
        return self.__carrinho
