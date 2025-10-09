from controle.buscaProdutoMixin import BuscaProdutoMixin
from limite.telaEstoque import TelaEstoque
from entidade.estoque import Estoque
from Excecoes.produtoNaoEncontradoException import ProdutoNaoEncontradoException

class ControladorEstoque(BuscaProdutoMixin):
    def __init__(self, controlador_sistema) -> None:
        self._controlador_sistema = controlador_sistema
        self.__estoque = Estoque()
        self.__tela_estoque = TelaEstoque()
    
    def tem_produtos_em_estoque(self) -> bool:
        return len(self.__estoque.cafes) > 0 or len(self.__estoque.maquinas) > 0

    @property
    def estoque(self) -> Estoque:
        return self.__estoque

    def listar_estoque(self) -> None:
        self.__tela_estoque.mostra_mensagem("\n---------- INVENTÁRIO ATUAL ----------")
        if not self.__estoque.listar_produtos():
            self.__tela_estoque.mostra_mensagem("O estoque está vazio.")
        else:
            for produto, quantidade in self.__estoque.listar_produtos().items():
                self.__tela_estoque.mostra_mensagem(f"-> PRODUTO: {produto.nome} (ID: {produto.id}) | QUANTIDADE: {quantidade}")
        self.__tela_estoque.mostra_mensagem("------------------------------------")

    def adicionar_novo_produto(self) -> None:
        dados = self.__tela_estoque.pega_dados_produto_estoque()
        if not dados:
            return
        try:
            produto = self.pega_produto_por_id(dados["id_produto"])
            if self.__estoque.produto_ja_existe(produto):
                self.__tela_estoque.mostra_mensagem(f"ERRO: '{produto.nome}' já está cadastrado no estoque.")
                self.__tela_estoque.mostra_mensagem("Use a opção 'Repor Estoque' para adicionar mais unidades.")
            else:
                self.__estoque.cadastrar_novo_produto(produto, dados["quantidade"])
                self.__tela_estoque.mostra_mensagem(f"'{produto.nome}' adicionado ao estoque com sucesso!")
        except ProdutoNaoEncontradoException as e:
            self.__tela_estoque.mostra_mensagem(f"ERRO: {e}")

    def repor_estoque(self) -> None:
        self.listar_estoque()
        dados = self.__tela_estoque.pega_dados_produto_estoque()
        if not dados:
            return
        try:
            produto = self.pega_produto_por_id(dados["id_produto"])

            if self.__estoque.produto_ja_existe(produto):
                self.__estoque.adicionar_quantidade(produto, dados["quantidade"])
                self.__tela_estoque.mostra_mensagem(f"Estoque de '{produto.nome}' atualizado.")
            else:
                self.__tela_estoque.mostra_mensagem(f"ERRO: '{produto.nome}' não está no estoque.")
                self.__tela_estoque.mostra_mensagem("Use a opção 'Adicionar Novo Produto' para cadastrá-lo primeiro.")
        except ProdutoNaoEncontradoException as e:
            self.__tela_estoque.mostra_mensagem(f"ERRO: {e}")

    def baixar_estoque(self) -> None:
        self.listar_estoque()
        dados = self.__tela_estoque.pega_dados_produto_estoque()
        if not dados:
            return
        try:
            produto = self.pega_produto_por_id(dados["id_produto"])
            resultado = self.__estoque.retirar_quantidade(produto, dados["quantidade"])
            
            if resultado:
                self.__tela_estoque.mostra_mensagem(resultado)
            else:
                self.__tela_estoque.mostra_mensagem("Baixa de estoque realizada com sucesso.")
        except ProdutoNaoEncontradoException as e:
            self.__tela_estoque.mostra_mensagem(f"ERRO: {e}")

    def retornar(self) -> None:
        self._controlador_sistema.abre_tela()
        
    def abre_tela(self) -> None:
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
                if opcao == 0:
                    mapa_opcoes[0]()
                    break
                
                if opcao in mapa_opcoes:
                    mapa_opcoes[opcao]()
                else:
                    self.__tela_estoque.mostra_mensagem("Opção inválida.")
            except ProdutoNaoEncontradoException as e:
                self.__tela_estoque.mostra_mensagem(f"ERRO: {e}")