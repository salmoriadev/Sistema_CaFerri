from limite.telaSistema import TelaSistema
from controle.controladorCafe import ControladorCafe
from controle.controladorCliente import ControladorCliente
from controle.controladorMaquinaDeCafe import ControladorMaquinaDeCafe
'''from controle.controladorVenda import ControladorVenda
from controle.controladorEstoque import ControladorEstoque '''

class ControladorSistema:

    def __init__(self):
        self.__tela_sistema = TelaSistema()
        
        self.__controlador_cliente = ControladorCliente(self)
        self.__controlador_cafe = ControladorCafe(self)
        self.__controlador_maquina_de_cafe = ControladorMaquinaDeCafe(self)
        '''self.__controlador_venda = ControladorVenda(self)
        self.__controlador_estoque = ControladorEstoque(self) '''

    @property
    def controlador_cliente(self):
        return self.__controlador_cliente

    @property
    def controlador_maquina_de_cafe(self):
        return self.__controlador_maquina_de_cafe

    @property
    def controlador_cafe(self):
        return self.__controlador_cafe
        
    '''@property
    def controlador_venda(self):
        return self.__controlador_venda'''
    
    # @property
    # def controlador_estoque(self):
        # return self.__controlador_estoque

    def inicializa_sistema(self):
        self.abre_tela()

    def cadastra_clientes(self):
        self.__controlador_cliente.abre_tela()

    def cadastra_cafes(self):
        self.__controlador_cafe.abre_tela()
        
    def cadastra_maquinas_de_cafe(self):
        self.__controlador_maquina_de_cafe.abre_tela()

    '''def gerencia_vendas(self):
        self.__controlador_venda.abre_tela()  ''' 

    '''def gerencia_estoque(self):
        self.__controlador_estoque.abre_tela()
        self.__tela_sistema.mostra_mensagem("Opção ainda não implementada.")
        
    def gerencia_fornecedores(self):
        self.__tela_sistema.mostra_mensagem("Opção ainda não implementada.")'''

    def encerra_sistema(self):
        exit(0)

    def abre_tela(self):
        lista_opcoes = {
            1: self.cadastra_cafes,
            2: self.cadastra_maquinas_de_cafe,
            3: self.cadastra_clientes,
            #4: self.gerencia_estoque,
            #5: self.gerencia_vendas,
            #6: self.gerencia_fornecedores_cafe,
            #7: self.gerencia_fornecedores_maquina,
            0: self.encerra_sistema
        }

        while True:
            opcao_escolhida = self.__tela_sistema.tela_opcoes()
            
            if opcao_escolhida in lista_opcoes:
                funcao_escolhida = lista_opcoes[opcao_escolhida]
                funcao_escolhida() 
                if opcao_escolhida == 0:
                    break
            else:
                self.__tela_sistema.mostra_mensagem("Opção inválida, por favor escolha uma das opções listadas.")