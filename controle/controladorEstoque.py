from limite.telaEstoque import TelaEstoque
from entidade.estoque import Estoque
from Excecoes.produtoNaoEncontradoException import ProdutoNaoEncontradoException

class ControladorEstoque:
    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__estoque = Estoque()
        self.__tela_estoque = TelaEstoque()

    @property
    def estoque(self):
        return self.__estoque

    def __pega_produto_por_id(self, id_produto: int):
        self.__controlador_sistema.pega_produto_por_id()

    def listar_estoque(self):
        self.__tela_estoque.mostra_estoque(self.__estoque.listar_produtos())

    def adicionar_novo_produto(self):
        dados = self.__tela_estoque.pega_dados_produto_estoque()
        if dados:
            produto = self.__pega_produto_por_id(dados["id_produto"])
            self.__estoque.adicionar_produto(produto, dados["quantidade"])
            self.__tela_estoque.mostra_mensagem(f"'{produto.nome}' adicionado ao estoque.")

    def repor_estoque(self):
        self.listar_estoque()
        dados = self.__tela_estoque.pega_dados_produto_estoque()
        if dados:
            produto = self.__pega_produto_por_id(dados["id_produto"])
            self.__estoque.adicionar_estoque(produto, dados["quantidade"])
            self.__tela_estoque.mostra_mensagem(f"Estoque de '{produto.nome}' atualizado.")

    def baixar_estoque(self):
        self.listar_estoque()
        dados = self.__tela_estoque.pega_dados_produto_estoque()
        if dados:
            produto = self.__pega_produto_por_id(dados["id_produto"])
            resultado = self.__estoque.retirar_estoque(produto, dados["quantidade"])
            if resultado:
                self.__tela_estoque.mostra_mensagem(resultado)
            else:
                self.__tela_estoque.mostra_mensagem("Baixa de estoque realizada.")

    def retornar(self):
        self.__controlador_sistema.abre_tela()

    def abre_tela(self):
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