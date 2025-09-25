from limite.telaSistema import TelaSistema
from controle.controladorCafe import ControladorCafe
from controle.controladorCliente import ControladorCliente
from controle.controladorMaquinaDeCafe import ControladorMaquinaDeCafe

class ControladorSistema:

    def __init__(self):
        self.__controlador_cafe = ControladorCafe(self)
        self.__controlador_cliente = ControladorCliente(self)
        self.__controlador_maquina_de_cafe = ControladorMaquinaDeCafe(self)
        self.__tela_sistema = TelaSistema()

    @property
    def controlador_cliente(self):
        return self.__controlador_cliente

    @property
    def controlador_maquina_de_cafe(self):
        return self.__controlador_maquina_de_cafe

    @property
    def controlador_cafe(self):
        return self.__controlador_cafe

    def inicializa_sistema(self):
        self.abre_tela()

    def cadastra_cafe(self):
        self.__controlador_cafe.abre_tela()

    def cadastra_cliente(self):
        self.__controlador_cliente.abre_tela()

    def cadastra_maquina_de_cafe(self):
        self.__controlador_maquina_de_cafe.abre_tela()
    
    #Tem que implementar essas funções
    def cadastra_estoque(self):
        pass
    def cadastra_venda(self):
        pass
    def cadastra_fornecedor_cafe(self):
        pass
    def cadastra_fornecedor_maquina_cafe(self):
        pass

    def encerra_sistema(self):
        exit(0)

    def abre_tela(self):
        lista_opcoes = {1: self.cadastra_cafe, 2: self.cadastra_maquina_de_cafe, 3: self.cadastra_cliente, 4: self.cadastra_estoque, 5: self.cadastra_venda, 6: self.cadastra_fornecedor_cafe, 7: self.cadastra_fornecedor_maquina_cafe,
                        0: self.encerra_sistema}

        while True:
            opcao_escolhida = self.__tela_sistema.tela_opcoes()
            funcao_escolhida = lista_opcoes[opcao_escolhida]
            funcao_escolhida()