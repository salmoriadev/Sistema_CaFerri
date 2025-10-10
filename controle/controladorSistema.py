from controle.controladorEmpresaCafe import ControladorEmpresaCafe
from controle.controladorEmpresaMaquina import ControladorEmpresaMaquina
from limite.telaSistema import TelaSistema
from controle.controladorCafe import ControladorCafe
from controle.controladorCliente import ControladorCliente
from controle.controladorMaquinaDeCafe import ControladorMaquinaDeCafe
from controle.controladorVenda import ControladorVenda
from controle.controladorEstoque import ControladorEstoque
from limite.telaRelatorio import TelaRelatorio
from Excecoes.clienteNaoEncontradoException import ClienteNaoEncontradoException

class ControladorSistema:

    def __init__(self) -> None:
        self.__tela_sistema = TelaSistema()
        self.__tela_relatorios = TelaRelatorio()
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
        if not self.__controlador_empresa_cafe.tem_empresas():
            self.__tela_sistema.mostra_mensagem("ERRO: É necessário cadastrar uma Empresa de Café primeiro!")
            return
        self.__controlador_cafe.abre_tela()

    def cadastra_maquinas_de_cafe(self) -> None:
        if not self.__controlador_empresa_maquina.tem_empresas():
            self.__tela_sistema.mostra_mensagem("ERRO: É necessário cadastrar uma Empresa de Máquina primeiro!")
            return
        self.__controlador_maquina_de_cafe.abre_tela()

    def gerencia_vendas(self) -> None:
        if not self.__controlador_estoque.tem_produtos_em_estoque():
            self.__tela_sistema.mostra_mensagem("ERRO: Não há produtos no estoque para vender!")
            return
        if not self.__controlador_cliente.tem_clientes():
            self.__tela_sistema.mostra_mensagem("ERRO: É necessário cadastrar pelo menos um cliente para iniciar uma venda!")
            return
        self.__controlador_venda.abre_tela()

    def gerencia_estoque(self) -> None:
        if not self.__controlador_cafe.existe_produto():
             self.__tela_sistema.mostra_mensagem("ERRO: Cadastre pelo menos um tipo de Café ou Máquina antes de gerenciar o estoque!")
             return
        self.__controlador_estoque.abre_tela()

    def gerencia_fornecedores_cafe(self) -> None:
        self.__controlador_empresa_cafe.abre_tela()

    def gerencia_fornecedores_maquina(self) -> None:
        self.__controlador_empresa_maquina.abre_tela()

    def relatorio_vendas_finalizadas(self):
        vendas_finalizadas = [v for v in self.__controlador_venda.vendas if v.status_venda == "Finalizada"]
        
        linhas_relatorio = []
        total_arrecadado = 0.0

        for venda in vendas_finalizadas:
            linhas_relatorio.append(
                f"ID: {venda.id_venda} | Cliente: {venda.cliente.nome} | Valor: R$ {venda.valor_total:.2f}"
            )
            total_arrecadado += venda.valor_total
        
        linhas_relatorio.append(f"\nTOTAL ARRECADADO: R$ {total_arrecadado:.2f}")
        
        self.__tela_relatorios.mostra_relatorio("Vendas Finalizadas", linhas_relatorio)

    def relatorio_clientes_por_valor(self):
        gastos_por_cliente = {}

        vendas_finalizadas = [v for v in self.__controlador_venda.vendas if v.status_venda == "Finalizada"]

        for venda in vendas_finalizadas:
            cliente_id = venda.cliente.id
            gastos_por_cliente[cliente_id] = gastos_por_cliente.get(cliente_id, 0) + venda.valor_total
        
        clientes_ordenados = sorted(gastos_por_cliente.items(), key=lambda item: item[1], reverse=True)

        linhas_relatorio = []
        for cliente_id, total_gasto in clientes_ordenados:
            try:
                cliente = self.__controlador_cliente.pega_cliente_por_id(cliente_id)
                linhas_relatorio.append(f"Cliente: {cliente.nome} (ID: {cliente_id}) | Total Gasto: R$ {total_gasto:.2f}")
            except ClienteNaoEncontradoException: 
                linhas_relatorio.append(f"Cliente ID: {cliente_id} (Excluído) | Total Gasto: R$ {total_gasto:.2f}")
        
        self.__tela_relatorios.mostra_relatorio("Clientes por Valor Gasto", linhas_relatorio)

    def relatorio_estoque_baixo(self):
        LIMITE_MINIMO = 5
        
        produtos_em_estoque = self.__controlador_estoque.produtos_em_estoque
        linhas_relatorio = []

        for produto, quantidade in produtos_em_estoque.items():
            if quantidade <= LIMITE_MINIMO:
                linhas_relatorio.append(
                    f"-> PRODUTO: {produto.nome} (ID: {produto.id}) | RESTAM APENAS: {quantidade} unidades"
                )
        
        if not linhas_relatorio:
            linhas_relatorio.append("Nenhum produto com estoque baixo.")

        self.__tela_relatorios.mostra_relatorio(f"Produtos com Estoque Abaixo de {LIMITE_MINIMO} Unidades", linhas_relatorio)


    def gera_relatorios(self) -> None:
        mapa_opcoes = {
            1: self.relatorio_vendas_finalizadas,
            2: self.relatorio_clientes_por_valor,
            3: self.relatorio_estoque_baixo
        }

        while True:
            opcao = self.__tela_relatorios.tela_opcoes()
            
            if opcao == 0:
                break
            
            funcao_escolhida = mapa_opcoes.get(opcao)
            if funcao_escolhida:
                funcao_escolhida()
            else:
                self.__tela_relatorios.mostra_mensagem("Opção inválida, por favor escolha uma das opções listadas.")
  
    def encerra_sistema(self) -> None:
        exit(0)

    def abre_tela(self) -> None:
        lista_opcoes = {
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
            opcao_escolhida = self.__tela_sistema.tela_opcoes()
            
            funcao_escolhida = lista_opcoes.get(opcao_escolhida)
            if funcao_escolhida:
                funcao_escolhida()
                if opcao_escolhida == 0:
                    break
            else:
                self.__tela_sistema.mostra_mensagem("Opção inválida, por favor escolha uma das opções listadas.")