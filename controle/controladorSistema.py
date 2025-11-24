"""
    Atua como o orquestrador central e o ponto de entrada de toda a aplicação.

    Esta classe é o "maestro" do sistema, responsável por instanciar e manter
    as referências de todos os outros controladores. Ela funciona como uma
    fachada (Facade), simplificando a interação do usuário com os diversos
    módulos do sistema.

    Suas principais responsabilidades são:
    - **Inicialização:** Cria as instâncias de todos os controladores de
      submódulos, injetando uma referência de si mesma (`self`) para permitir
      a comunicação e a colaboração entre eles.
    - **Gerenciamento de Fluxo:** Controla o loop principal da aplicação,
      exibindo o menu principal (`TelaSistema`) e delegando as ações do
      usuário para o controlador apropriado.
    - **Aplicação de Regras de Negócio de Alto Nível:** Antes de invocar um
      submódulo, ela realiza validações cruciais que dependem do estado de
      outros módulos. Por exemplo, impede o cadastro de um café se nenhum
      fornecedor de café existir, ou bloqueia o início de uma venda se não
      houver clientes ou produtos em estoque.
    - **Ponto de Acesso Único:** Serve como um hub central, permitindo que os
      controladores "conversem" entre si de forma desacoplada, acessando
      uns aos outros através das propriedades expostas pelo `ControladorSistema`.
    """

from controle.controladorEmpresaCafe import ControladorEmpresaCafe
from controle.controladorEmpresaMaquina import ControladorEmpresaMaquina
from limite.telaSistema import TelaSistema
from controle.controladorCafe import ControladorCafe
from controle.controladorCliente import ControladorCliente
from controle.controladorMaquinaDeCafe import ControladorMaquinaDeCafe
from controle.controladorVenda import ControladorVenda
from controle.controladorEstoque import ControladorEstoque
from controle.controladorRelatorio import ControladorRelatorios


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
        self.__controlador_relatorios = ControladorRelatorios(self)

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
        """
        Inicia o sistema exibindo o menu principal e iniciando o loop de
        navegação. Este método é chamado pelo main.py para dar início à
        aplicação.
        """
        self.abre_tela()

    def cadastra_clientes(self) -> None:
        """
        Redireciona para o módulo de gerenciamento de clientes, permitindo
        cadastro, alteração, listagem e exclusão de clientes do sistema.
        """
        self.__controlador_cliente.abre_tela()

    def cadastra_cafes(self) -> None:
        """
        Redireciona para o módulo de gerenciamento de cafés. Valida que existe
        pelo menos um fornecedor de café cadastrado antes de permitir o acesso,
        garantindo integridade referencial dos dados.
        """
        if not self.__controlador_empresa_cafe.tem_empresas():
            self.__tela_sistema.mostra_mensagem(
                "ERRO: É necessário cadastrar uma Empresa de Café primeiro!")
            return
        self.__controlador_cafe.abre_tela()

    def cadastra_maquinas_de_cafe(self) -> None:
        """
        Redireciona para o módulo de gerenciamento de máquinas de café. Valida
        que existe pelo menos um fornecedor de máquinas cadastrado antes de
        permitir o acesso, garantindo integridade referencial dos dados.
        """
        if not self.__controlador_empresa_maquina.tem_empresas():
            self.__tela_sistema.mostra_mensagem(
                "ERRO: É necessário cadastrar uma Empresa de Máquina primeiro!")
            return
        self.__controlador_maquina_de_cafe.abre_tela()

    def gerencia_vendas(self) -> None:
        """
        Redireciona para o módulo de gerenciamento de vendas. Valida que existem
        produtos em estoque e pelo menos um cliente cadastrado antes de permitir
        o acesso, garantindo que o sistema esteja em estado válido para realizar
        transações comerciais.
        """
        if not self.__controlador_estoque.tem_produtos_em_estoque():
            self.__tela_sistema.mostra_mensagem(
                "ERRO: Não há produtos no estoque para vender!")
            return
        if not self.__controlador_cliente.tem_clientes():
            self.__tela_sistema.mostra_mensagem(
                "ERRO: É necessário cadastrar pelo menos um cliente para iniciar uma venda!")
            return
        self.__controlador_venda.abre_tela()

    def gerencia_estoque(self) -> None:
        """
        Redireciona para o módulo de gerenciamento de estoque. Valida que existe
        pelo menos um produto (café ou máquina) cadastrado antes de permitir o
        acesso, garantindo que haja produtos para serem gerenciados no estoque.
        """
        if not self.__controlador_cafe.existe_produto():
            self.__tela_sistema.mostra_mensagem(
                "ERRO: Cadastre pelo menos um tipo de Café ou Máquina antes de gerenciar o estoque!")
            return
        self.__controlador_estoque.abre_tela()

    def gerencia_fornecedores_cafe(self) -> None:
        """
        Redireciona para o módulo de gerenciamento de fornecedores de café,
        permitindo cadastro, alteração, listagem e exclusão de empresas
        fornecedoras de café.
        """
        self.__controlador_empresa_cafe.abre_tela()

    def gerencia_fornecedores_maquina(self) -> None:
        """
        Redireciona para o módulo de gerenciamento de fornecedores de máquinas,
        permitindo cadastro, alteração, listagem e exclusão de empresas
        fornecedoras de máquinas de café.
        """
        self.__controlador_empresa_maquina.abre_tela()

    def gera_relatorios(self) -> None:
        """
        Redireciona para o módulo de relatórios, que oferece análises de vendas,
        clientes, estoque e fornecedores para suporte à tomada de decisão.
        """
        self.__controlador_relatorios.abre_tela()

    def encerra_sistema(self) -> None:
        """
        Encerra a execução do sistema, finalizando o programa.
        """
        exit(0)

    def abre_tela(self) -> None:
        """
        Controla o loop principal do menu do sistema. Exibe o menu principal,
        captura a opção escolhida pelo usuário e delega a execução para o
        método correspondente. Continua em loop até que o usuário escolha
        encerrar o sistema (opção 0).
        """
        mapa_opcoes = {
            1: self.gerencia_fornecedores_cafe,
            2: self.gerencia_fornecedores_maquina,
            3: self.cadastra_clientes,
            4: self.cadastra_cafes,
            5: self.cadastra_maquinas_de_cafe,
            6: self.gerencia_estoque,
            7: self.gerencia_vendas,
            8: self.gera_relatorios,
            0: self.encerra_sistema
        }

        while True:
            opcao = self.__tela_sistema.tela_opcoes()
            if opcao is None:
                break

            funcao_escolhida = mapa_opcoes.get(opcao)
            if funcao_escolhida:
                funcao_escolhida()
                if opcao == 0:
                    break
            else:
                self.__tela_sistema.mostra_mensagem(
                    "Opção inválida, por favor escolha uma das opções listadas.")
