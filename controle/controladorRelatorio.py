"""
    Orquestra a lógica de negócio para a geração de todos os relatórios
    de inteligência de negócio do sistema.
    Ela centraliza toda a lógica de análise de dados, mantendo os outros
    controladores focados em suas responsabilidades operacionais (CRUD) e
    delegando a exibição final dos resultados para a `TelaRelatorio`.
    """

from limite.telaRelatorio import TelaRelatorio
from Excecoes.clienteNaoEncontradoException import ClienteNaoEncontradoException

class ControladorRelatorios:
    def __init__(self, controlador_sistema) -> None:
        self.__controlador_sistema = controlador_sistema
        self.__tela_relatorios = TelaRelatorio()

    def relatorio_vendas_finalizadas(self):
        vendas_finalizadas = [v for v in self.__controlador_sistema.controlador_venda.vendas if v.status_venda == "Finalizada"]
        
        linhas_relatorio = []
        total_arrecadado = 0.0

        for venda in vendas_finalizadas:
            linhas_relatorio.append(
                f"ID: {venda.id_venda} | Cliente: {venda.cliente.nome} | Valor: R$ {venda.valor_total:.2f}"
            )
            total_arrecadado += venda.valor_total
        
        linhas_relatorio.append(f"\nTOTAL ARRECADADO: R$ {total_arrecadado:.2f}")
        
        self.__tela_relatorios.mostra_relatorio("Vendas Finalizadas", linhas_relatorio)

    def relatorio_cafes_mais_vendidos(self):
        vendas_finalizadas = [v for v in self.__controlador_sistema.controlador_venda.vendas if v.status_venda == "Finalizada"]
        contagem_cafes = {}

        for venda in vendas_finalizadas:
            for produto, quantidade in venda.carrinho.items():
                if produto in self.__controlador_sistema.controlador_cafe.cafes:
                    contagem_cafes[produto] = contagem_cafes.get(produto, 0) + quantidade
        
        cafes_ordenados = sorted(contagem_cafes.items(), key=lambda item: item[1], reverse=True)

        linhas_relatorio = []
        for cafe, total_vendido in cafes_ordenados:
            linhas_relatorio.append(f"Café: {cafe.nome} (ID: {cafe.id}) | Total Vendido: {total_vendido} unidades")
        
        if not linhas_relatorio:
            linhas_relatorio.append("Nenhum café vendido até o momento.")
        self.__tela_relatorios.mostra_relatorio("Cafés Mais Vendidos", linhas_relatorio)

    def relatorio_maquinas_mais_vendidas(self):
        vendas_finalizadas = [v for v in self.__controlador_sistema.controlador_venda.vendas if v.status_venda == "Finalizada"]
        contagem_maquinas = {}

        for venda in vendas_finalizadas:
            for produto, quantidade in venda.carrinho.items():
                if produto in self.__controlador_sistema.controlador_maquina_de_cafe.maquinas:
                    contagem_maquinas[produto] = contagem_maquinas.get(produto, 0) + quantidade
        
        maquinas_ordenadas = sorted(contagem_maquinas.items(), key=lambda item: item[1], reverse=True)

        linhas_relatorio = []
        for maquina, total_vendido in maquinas_ordenadas:
            linhas_relatorio.append(f"Máquina: {maquina.nome} (ID: {maquina.id}) | Total Vendido: {total_vendido} unidades")
        
        if not linhas_relatorio:
            linhas_relatorio.append("Nenhuma máquina vendida até o momento.")
        self.__tela_relatorios.mostra_relatorio("Máquinas Mais Vendidas", linhas_relatorio)

    def relatorio_empresas_fornecedoras_mais_ativas(self):
        vendas_finalizadas = [v for v in self.__controlador_sistema.controlador_venda.vendas if v.status_venda == "Finalizada"]
        contagem_empresas = {}

        for venda in vendas_finalizadas:
            for produto, quantidade in venda.carrinho.items():
                if hasattr(produto, 'empresa_fornecedora'):
                    fornecedor = produto.empresa_fornecedora
                    contagem_empresas[fornecedor] = contagem_empresas.get(fornecedor, 0) + quantidade

        empresas_ordenadas = sorted(contagem_empresas.items(), key=lambda item: item[1], reverse=True)

        linhas_relatorio = []
        for empresa, total_vendido in empresas_ordenadas:
            linhas_relatorio.append(f"Empresa: {empresa.nome} (ID: {empresa.id}) | Total de Produtos Vendidos: {total_vendido} unidades")

        if not linhas_relatorio:
            linhas_relatorio.append("Nenhuma venda de produtos de fornecedores registrada.")

        self.__tela_relatorios.mostra_relatorio("Empresas Fornecedoras Mais Ativas", linhas_relatorio)

    def relatorio_clientes_por_valor(self):
        gastos_por_cliente = {}
        vendas_finalizadas = [v for v in self.__controlador_sistema.controlador_venda.vendas if v.status_venda == "Finalizada"]

        for venda in vendas_finalizadas:
            cliente_id = venda.cliente.id
            gastos_por_cliente[cliente_id] = gastos_por_cliente.get(cliente_id, 0) + venda.valor_total
        
        clientes_ordenados = sorted(gastos_por_cliente.items(), key=lambda item: item[1], reverse=True)

        linhas_relatorio = []
        for cliente_id, total_gasto in clientes_ordenados:
            try:
                cliente = self.__controlador_sistema.controlador_cliente.pega_cliente_por_id(cliente_id)
                linhas_relatorio.append(f"Cliente: {cliente.nome} (ID: {cliente_id}) | Total Gasto: R$ {total_gasto:.2f}")
            except ClienteNaoEncontradoException: 
                linhas_relatorio.append(f"Cliente ID: {cliente_id} (Excluído) | Total Gasto: R$ {total_gasto:.2f}")
        
        self.__tela_relatorios.mostra_relatorio("Clientes por Valor Gasto", linhas_relatorio)

    def relatorio_estoque_baixo(self):
        LIMITE_MINIMO = 5
        
        produtos_em_estoque = self.__controlador_sistema.controlador_estoque.produtos_em_estoque
        linhas_relatorio = []

        for produto, quantidade in produtos_em_estoque.items():
            if quantidade <= LIMITE_MINIMO:
                linhas_relatorio.append(
                    f"-> PRODUTO: {produto.nome} (ID: {produto.id}) | RESTAM APENAS: {quantidade} unidades"
                )
        
        if not linhas_relatorio:
            linhas_relatorio.append("Nenhum produto com estoque baixo.")

        self.__tela_relatorios.mostra_relatorio(f"Produtos com Estoque Abaixo de {LIMITE_MINIMO} Unidades", linhas_relatorio)

    def abre_tela(self) -> None:
        mapa_opcoes = {
            1: self.relatorio_vendas_finalizadas,
            2: self.relatorio_clientes_por_valor,
            3: self.relatorio_estoque_baixo,
            4: self.relatorio_cafes_mais_vendidos,
            5: self.relatorio_maquinas_mais_vendidas,
            6: self.relatorio_empresas_fornecedoras_mais_ativas
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
