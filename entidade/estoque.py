"""
    Gerencia o inventário de todos os produtos do sistema.

    Esta classe atua como um repositório centralizado para o controle de
    quantidades de produtos. Ela utiliza um dicionário (`__produtos_em_estoque`)
    para mapear objetos `Produto` (sejam `Cafe` ou `MaquinaDeCafe`) às suas
    respectivas quantidades disponíveis.
    """

from typing import Callable, Dict, Optional

from entidade.produto import Produto
from Excecoes.estoqueInsuficienteException import EstoqueInsuficienteException
from Excecoes.produtoNaoEmEstoqueException import ProdutoNaoEmEstoqueException


class Estoque:
    def __init__(self) -> None:
        """
        Inicializa estoque vazio com dicionário para mapear produtos para
        quantidades. Callback de alteração inicia como None e pode ser
        registrado pelo controlador para persistência automática.
        """
        self.__produtos_em_estoque = {}
        self.__callback_alteracao: Optional[Callable[[
            Dict[Produto, int]], None]] = None

    @property
    def produtos_em_estoque(self) -> dict:
        return self.__produtos_em_estoque

    def definir_callback_alteracao(self, callback: Callable[[Dict[Produto, int]], None]) -> None:
        """
        Registra função callback a ser chamada automaticamente após qualquer
        alteração no estoque. Permite que o controlador seja notificado para
        persistir estado sem acoplamento direto. Usado para sincronização
        automática com arquivo de persistência.
        """
        self.__callback_alteracao = callback

    def __notificar_alteracao(self) -> None:
        """
        Notifica callback registrado sobre alteração no estoque, passando
        estado atual completo. Chamado internamente após cada modificação
        para garantir persistência automática.
        """
        if self.__callback_alteracao:
            self.__callback_alteracao(self.__produtos_em_estoque)

    def produto_ja_existe(self, produto: Produto) -> bool:
        """
        Verifica se produto já está cadastrado no estoque. Usado para
        validar operações de adição e reposição, garantindo que produtos
        novos sejam cadastrados e produtos existentes sejam apenas
        incrementados.
        """
        return produto in self.__produtos_em_estoque

    def cadastrar_novo_produto(self, produto: Produto, quantidade: int) -> None:
        """
        Registra um novo produto no estoque com quantidade inicial. Só
        cadastra se produto não existir previamente. Notifica callback
        após cadastro para persistência automática.
        """
        if quantidade < 0:
            raise ValueError("A quantidade não pode ser negativa.")
        if not self.produto_ja_existe(produto):
            self.__produtos_em_estoque[produto] = quantidade
            self.__notificar_alteracao()

    def adicionar_quantidade(self, produto: Produto, quantidade_a_adicionar: int) -> None:
        """
        Incrementa quantidade de um produto já existente no estoque.
        Só adiciona se produto estiver cadastrado. Notifica callback
        após incremento para persistência automática.
        """
        if quantidade_a_adicionar < 0:
            raise ValueError("A quantidade a adicionar não pode ser negativa.")
        if self.produto_ja_existe(produto):
            self.__produtos_em_estoque[produto] += quantidade_a_adicionar
            self.__notificar_alteracao()

    def retirar_quantidade(self, produto: Produto, quantidade_a_retirar: int) -> None:
        """
        Decrementa quantidade de um produto do estoque. Valida que produto
        existe e que quantidade disponível é suficiente. Lança exceções
        específicas se validações falharem. Notifica callback após retirada
        bem-sucedida para persistência automática.
        """
        if quantidade_a_retirar <= 0:
            raise ValueError("A quantidade a retirar deve ser positiva.")
        if not self.produto_ja_existe(produto):
            raise ProdutoNaoEmEstoqueException(produto.nome)

        if self.__produtos_em_estoque[produto] >= quantidade_a_retirar:
            self.__produtos_em_estoque[produto] -= quantidade_a_retirar
            self.__notificar_alteracao()
        else:
            raise EstoqueInsuficienteException(
                produto.nome, quantidade_a_retirar, self.__produtos_em_estoque[produto])

    def remover_produto_do_estoque(self, produto: Produto) -> None:
        """
        Remove completamente um produto do estoque, independente da quantidade.
        Usado quando produto é excluído do sistema para manter integridade
        referencial. Notifica callback após remoção para persistência automática.
        """
        if self.produto_ja_existe(produto):
            del self.__produtos_em_estoque[produto]
            self.__notificar_alteracao()

    def listar_produtos(self) -> dict:
        """
        Retorna dicionário completo de produtos em estoque mapeando produtos
        para suas quantidades. Usado para visualização e validações durante
        finalização de vendas.
        """
        return self.__produtos_em_estoque

    def remover_produto(self, produto: Produto) -> bool:
        """
        Remove produto do estoque e retorna True se remoção foi bem-sucedida,
        False se produto não existia. Notifica callback após remoção para
        persistência automática.
        """
        if self.produto_ja_existe(produto):
            del self.__produtos_em_estoque[produto]
            self.__notificar_alteracao()
            return True
        return False
