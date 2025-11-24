"""
    Orquestra a lógica de negócio para o gerenciamento de Estoque.

    Esta classe atua como a camada de Controle (Controller), sendo a ponte
    entre a interface do usuário (`TelaEstoque`) e o modelo de dados (`Estoque`).
    Sua principal função é processar as solicitações do usuário e aplicar as
    regras de negócio para manipular o inventário de produtos do sistema.

    Utilizando a herança de `BuscaProdutoMixin`, este controlador tem a
    capacidade de localizar qualquer produto (seja um `Cafe` ou uma
    `MaquinaDeCafe`) em todo o sistema pelo seu ID, permitindo uma
    integração coesa entre os diferentes módulos de produtos.
    """

from controle.buscaProdutoMixin import BuscaProdutoMixin
from limite.telaEstoque import TelaEstoque
from entidade.estoque import Estoque
from Excecoes.produtoNaoEncontradoException import ProdutoNaoEncontradoException
from Excecoes.produtoNaoEmEstoqueException import ProdutoNaoEmEstoqueException
from Excecoes.estoqueInsuficienteException import EstoqueInsuficienteException
from DAOs.estoque_dao import EstoqueDAO


class ControladorEstoque(BuscaProdutoMixin):
    def __init__(self, controlador_sistema) -> None:
        self._controlador_sistema = controlador_sistema
        self.__estoque = Estoque()
        self.__estoque_dao = EstoqueDAO()
        self.__tela_estoque = TelaEstoque()
        self.__carregar_do_dao()
        self.__estoque.definir_callback_alteracao(self.__persistir_estado)

    @property
    def estoque(self) -> Estoque:
        return self.__estoque

    @property
    def produtos_em_estoque(self) -> dict:
        return self.__estoque.produtos_em_estoque

    def tem_produtos_em_estoque(self) -> bool:
        return sum(self.__estoque.produtos_em_estoque.values()) > 0

    def listar_estoque(self) -> None:
        """
        Exibe inventário completo do estoque. Extrai informações de cada
        produto (nome, ID, quantidade) e formata para exibição na tela.
        Informa se estoque está vazio antes de tentar listar.
        """
        produtos = self.__estoque.listar_produtos()
        if not produtos:
            self.__tela_estoque.mostra_mensagem("O estoque está vazio.")
            return

        itens = []
        for produto, quantidade in produtos.items():
            itens.append({
                "nome": produto.nome,
                "id": produto.id,
                "quantidade": quantidade
            })

        self.__tela_estoque.mostra_inventario(itens)

    def adicionar_novo_produto(self) -> None:
        """
        Cadastra um novo produto no estoque com quantidade inicial. Valida
        que produto não está já cadastrado (usa opção de reposição se já
        existir). Busca produto pelo ID usando mixin e registra no estoque,
        que notifica callback para persistência automática.
        """
        dados_produto = self.__tela_estoque.pega_dados_produto_estoque()
        if not dados_produto:
            return
        produto = self.pega_produto_por_id(dados_produto["id_produto"])
        if self.__estoque.produto_ja_existe(produto):
            self.__tela_estoque.mostra_mensagem(
                f"ERRO: '{produto.nome}' já está cadastrado no estoque.")
            self.__tela_estoque.mostra_mensagem(
                "Use a opção 'Repor Estoque' para adicionar mais unidades.")
        else:
            self.__estoque.cadastrar_novo_produto(
                produto, dados_produto["quantidade"])
            self.__tela_estoque.mostra_mensagem(
                f"'{produto.nome}' adicionado ao estoque com sucesso!")

    def repor_estoque(self) -> None:
        """
        Adiciona quantidade a um produto já existente no estoque. Lista
        estoque primeiro para facilitar seleção, valida que produto está
        cadastrado e incrementa quantidade. Persistência ocorre via callback
        automático após alteração.
        """
        self.listar_estoque()
        dados_produto = self.__tela_estoque.pega_dados_produto_estoque()
        if not dados_produto:
            return
        produto = self.pega_produto_por_id(dados_produto["id_produto"])

        if self.__estoque.produto_ja_existe(produto):
            self.__estoque.adicionar_quantidade(
                produto, dados_produto["quantidade"])
            self.__tela_estoque.mostra_mensagem(
                f"Estoque de '{produto.nome}' atualizado.")
        else:
            self.__tela_estoque.mostra_mensagem(
                f"ERRO: '{produto.nome}' não está no estoque.")
            self.__tela_estoque.mostra_mensagem(
                "Use a opção 'Adicionar Novo Produto' para cadastrá-lo primeiro.")

    def baixar_estoque(self) -> None:
        """
        Remove quantidade de um produto do estoque (baixa manual). Lista
        estoque primeiro, valida existência e quantidade suficiente, e
        decrementa. Lança exceção se produto não existir ou quantidade
        insuficiente. Persistência via callback automático.
        """
        self.listar_estoque()
        dados_produto = self.__tela_estoque.pega_dados_produto_estoque()
        if not dados_produto:
            return
        produto = self.pega_produto_por_id(dados_produto["id_produto"])
        self.__estoque.retirar_quantidade(produto, dados_produto["quantidade"])
        self.__tela_estoque.mostra_mensagem(
            "Baixa de estoque realizada com sucesso.")

    def retornar(self) -> None:
        """
        Retorna ao menu principal do sistema, delegando navegação para o
        controlador sistema.
        """
        self._controlador_sistema.abre_tela()

    def abre_tela(self) -> None:
        """
        Controla o loop principal do menu de estoque. Exibe opções, captura
        escolha do usuário e delega execução para método correspondente.
        Trata exceções de negócio (produto não encontrado, estoque insuficiente)
        e exibe mensagens de erro apropriadas. Continua em loop até usuário
        escolher retornar (opção 0).
        """
        mapa_opcoes = {
            1: self.listar_estoque,
            2: self.adicionar_novo_produto,
            3: self.repor_estoque,
            4: self.baixar_estoque,
            0: self.retornar
        }
        while True:
            try:
                opcao = self.__tela_estoque.tela_opcoes()
                if opcao is None:
                    break
                if opcao == 0:
                    mapa_opcoes[0]()
                    break

                if opcao in mapa_opcoes:
                    mapa_opcoes[opcao]()
                else:
                    self.__tela_estoque.mostra_mensagem(
                        "Opção inválida! Por favor, digite um número do menu.")
            except (ProdutoNaoEncontradoException, ProdutoNaoEmEstoqueException,
                    EstoqueInsuficienteException) as e:
                self.__tela_estoque.mostra_mensagem(f"ERRO: {e}")

    def __carregar_do_dao(self) -> None:
        """
        Carrega estado do estoque do arquivo de persistência durante
        inicialização. Itera sobre dados salvos, busca produtos pelo ID
        usando mixin e registra no estoque. Ignora produtos que não
        existem mais (foram excluídos), mantendo consistência. Persiste
        estado após carregamento para sincronizar arquivo.
        """
        dados_estoque = self.__estoque_dao.carregar()
        for id_produto, quantidade in dados_estoque.items():
            try:
                produto = self.pega_produto_por_id(id_produto)
                self.__estoque.cadastrar_novo_produto(produto, quantidade)
            except ProdutoNaoEncontradoException:
                continue
        self.__persistir_estado(self.__estoque.produtos_em_estoque)

    def __persistir_estado(self, produtos: dict) -> None:
        mapa_produtos_por_id = {
            produto.id: quantidade for produto, quantidade in produtos.items()}
        self.__estoque_dao.salvar(mapa_produtos_por_id)
