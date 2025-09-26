from limite.telaVenda import TelaVenda
from entidade.venda import Venda

class ControladorVenda:
    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__vendas = []
        self.__tela_venda = TelaVenda()

    def pega_venda_por_id(self, id_venda: int):
        for venda in self.__vendas:
            if venda.id_venda == id_venda:
                return venda
        return None
    

    def pega_produto_por_id(self, id_produto: int):
        produto = self.__controlador_sistema.controlador_cafe.pega_cafe_por_id(id_produto)
        if produto is None:
            produto = self.__controlador_sistema.controlador_maquina_de_cafe.pega_maquina_por_id(id_produto)
        return produto

    def iniciar_venda(self):
        pass

    def gerenciar_venda(self):
        pass

    def adicionar_produto(self):
        pass

    def remover_produto(self):
        pass

    def listar_produtos_venda(self):
        pass

    def finalizar_venda(self):
        pass

    def listar_vendas(self):
        pass

    def mostrar_detalhes_venda(self):
        pass   

    def excluir_venda(self):
        pass

    def retornar(self):
        self.__controlador_sistema.abre_tela()

    def abre_tela(self):
         mapa_opcoes = {
            1: self.iniciar_venda,
            2: self.listar_vendas,
            3: self.excluir_venda,
            0: self.retornar
        }
        while True:
            opcao = self.__tela_venda.tela_opcoes()
            if opcao == 0:
                mapa_opcoes[0]()
                break
            
            if opcao in mapa_opcoes:
                mapa_opcoes[opcao]()
            else:
                self.__tela_venda.mostra_mensagem("Opção inválida.")