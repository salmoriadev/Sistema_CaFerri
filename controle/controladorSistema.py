from controle.controladorEmpresaCafe import ControladorEmpresaCafe
from controle.controladorEmpresaMaquina import ControladorEmpresaMaquina
from limite.telaSistema import TelaSistema
from controle.controladorCafe import ControladorCafe
from controle.controladorCliente import ControladorCliente
from controle.controladorMaquinaDeCafe import ControladorMaquinaDeCafe
from controle.controladorVenda import ControladorVenda
from controle.controladorEstoque import ControladorEstoque 

class ControladorSistema:

    def __init__(self) -> None:
        self.__tela_sistema = TelaSistema()
        self.__controlador_cliente = ControladorCliente(self)
        self.__controlador_cafe = ControladorCafe(self)
        self.__controlador_maquina_de_cafe = ControladorMaquinaDeCafe(self)
        self.__controlador_venda = ControladorVenda(self)
        self.__controlador_estoque = ControladorEstoque(self)
        self.__controlador_empresa_cafe = ControladorEmpresaCafe(self)
        self.__controlador_empresa_maquina = ControladorEmpresaMaquina(self)

    @property
    def controlador_cliente(self) -> ControladorCliente:
        return self.__controlador_cliente

    @property
    def controlador_maquina_de_cafe(self) -> ControladorMaquinaDeCafe:
        return self.__controlador_maquina_de_cafe

    @property
    def controlador_cafe(self) -> ControladorCafe:
        return self.__controlador_cafe
        
    @property
    def controlador_venda(self) -> ControladorVenda:
        return self.__controlador_venda
    
    @property
    def controlador_estoque(self) -> ControladorEstoque:
        return self.__controlador_estoque
    
    @property
    def controlador_empresa_cafe(self) -> ControladorEmpresaCafe:
        return self.__controlador_empresa_cafe

    @property
    def controlador_empresa_maquina(self) -> ControladorEmpresaMaquina:
        return self.__controlador_empresa_maquina

    def inicializa_sistema(self) -> None:
        self.abre_tela()

    def cadastra_clientes(self) -> None:
        self.__controlador_cliente.abre_tela()

    def cadastra_cafes(self) -> None:
        self.__controlador_cafe.abre_tela()

    def cadastra_maquinas_de_cafe(self) -> None:
        self.__controlador_maquina_de_cafe.abre_tela()

    def gerencia_vendas(self) -> None:
        self.__controlador_venda.abre_tela()

    def gerencia_estoque(self) -> None:
        self.__controlador_estoque.abre_tela()

    def gerencia_fornecedores_cafe(self) -> None:
        self.__controlador_empresa_cafe.abre_tela()

    def gerencia_fornecedores_maquina(self) -> None:
        self.__controlador_empresa_maquina.abre_tela()

    def encerra_sistema(self) -> None:
        exit(0)

    def abre_tela(self) -> None:
        lista_opcoes = {
            1: self.cadastra_cafes,
            2: self.cadastra_maquinas_de_cafe,
            3: self.cadastra_clientes,
            4: self.gerencia_estoque,
            5: self.gerencia_vendas,
            6: self.gerencia_fornecedores_cafe,
            7: self.gerencia_fornecedores_maquina,
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