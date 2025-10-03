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
        try:
            return self.__controlador_sistema.controlador_cafe.pega_cafe_por_id(id_produto)
        except: 
            try:
                return self.__controlador_sistema.controlador_maquina_de_cafe.pega_maquina_por_id(id_produto)
            except: 
                raise ProdutoNaoEncontradoException

    def listar_estoque(self):
        self.__tela_estoque.mostra_estoque(self.__estoque.listar_produtos())

    def adicionar_novo_produto(self):
        pass

    def repor_estoque(self):
        pass
    
    def baixar_estoque(self):
        pass
    
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