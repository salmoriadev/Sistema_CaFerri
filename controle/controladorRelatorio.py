"""
    Orquestra a lógica de negócio para a geração de todos os relatórios
    de inteligência de negócio do sistema.
    Ela centraliza toda a lógica de análise de dados, mantendo os outros
    controladores focados em suas responsabilidades operacionais (CRUD) e
    delegando a exibição final dos resultados para a `TelaRelatorio`.
    """

from limite.telaRelatorio import TelaRelatorio
from Excecoes.clienteNaoEncontradoException import ClienteNaoEncontradoException
from entidade.cafe import Cafe
from entidade.maquina_de_cafe import MaquinaDeCafe
from datetime import datetime
import os


class ControladorRelatorios:
    def __init__(self, controlador_sistema) -> None:
        self.__controlador_sistema = controlador_sistema
        self.__tela_relatorios = TelaRelatorio()

    def __salvar_relatorio_em_arquivo(self, titulo: str, linhas_relatorio: list) -> str:
        """
        Salva relatório em arquivo .txt com timestamp único. Cria pasta 'relatorios'
        se não existir. Retorna o caminho do arquivo gerado. Em caso de erro na escrita,
        retorna string vazia sem interromper a exibição do relatório na tela.
        """
        try:
            pasta = "relatorios"
            if not os.path.exists(pasta):
                os.makedirs(pasta)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo_safe = titulo.replace(" ", "_").replace("/", "-")
            nome_arquivo = os.path.join(pasta, f"{nome_arquivo_safe}_{timestamp}.txt")

            with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
                arquivo.write("=" * 60 + "\n")
                arquivo.write(f"{titulo.upper()}\n")
                arquivo.write("=" * 60 + "\n\n")
                arquivo.write("\n".join(linhas_relatorio))
                arquivo.write(f"\n\n{'=' * 60}\n")
                arquivo.write(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")

            return nome_arquivo
        except (IOError, OSError, PermissionError):
            # Falha ao salvar arquivo não impede exibição do relatório na tela
            return ""

    def relatorio_vendas_finalizadas(self):
        """
        Gera relatório de todas as vendas finalizadas no sistema. Filtra
        vendas por status "Finalizada", extrai informações relevantes (ID,
        cliente, valor) e calcula total arrecadado. Formata dados para
        exibição na tela de relatórios e salva automaticamente em arquivo .txt.
        """
        vendas_finalizadas = [
            v for v in self.__controlador_sistema.controlador_venda.vendas if (
                v.status_venda == "Finalizada")]

        linhas_relatorio = []
        total_arrecadado = 0.0

        for venda in vendas_finalizadas:
            linhas_relatorio.append(
                f"ID: {venda.id_venda} | Cliente: {venda.cliente.nome} | "
                f"Valor: R$ {venda.valor_total:.2f}"
            )
            total_arrecadado += venda.valor_total

        linhas_relatorio.append(
            f"\nTOTAL ARRECADADO: R$ {total_arrecadado:.2f}")

        self.__salvar_relatorio_em_arquivo("Vendas Finalizadas", linhas_relatorio)
        self.__tela_relatorios.mostra_relatorio(
            "Vendas Finalizadas", linhas_relatorio)

    def relatorio_cafes_mais_vendidos(self):
        """
        Analisa vendas finalizadas para identificar cafés mais vendidos.
        Contabiliza quantidade vendida de cada café em todas as vendas,
        ordena por quantidade (decrescente) e formata para exibição.
        Mostra mensagem se nenhum café foi vendido. Salva automaticamente
        em arquivo .txt.
        """
        vendas_finalizadas = [
            v for v in self.__controlador_sistema.controlador_venda.vendas if (
                v.status_venda == "Finalizada")]
        contagem_cafes = {}

        for venda in vendas_finalizadas:
            for produto, quantidade in venda.carrinho.items():
                if isinstance(produto, Cafe):
                    # Usa ID como chave para agrupar produtos iguais
                    cafe_id = produto.id
                    if cafe_id not in contagem_cafes:
                        contagem_cafes[cafe_id] = {'produto': produto, 'total': 0}
                    contagem_cafes[cafe_id]['total'] += quantidade

        cafes_ordenados = sorted(
            contagem_cafes.values(), key=lambda item: item['total'], reverse=True)

        linhas_relatorio = []
        for item in cafes_ordenados:
            cafe = item['produto']
            total_vendido = item['total']
            linhas_relatorio.append(
                f"Café: {cafe.nome} (ID: {cafe.id}) | Total Vendido: {total_vendido} unidades")

        if not linhas_relatorio:
            linhas_relatorio.append("Nenhum café vendido até o momento.")
        self.__salvar_relatorio_em_arquivo("Cafés Mais Vendidos", linhas_relatorio)
        self.__tela_relatorios.mostra_relatorio(
            "Cafés Mais Vendidos", linhas_relatorio)

    def relatorio_maquinas_mais_vendidas(self):
        """
        Analisa vendas finalizadas para identificar máquinas mais vendidas.
        Filtra produtos que são máquinas, contabiliza quantidades vendidas,
        ordena por quantidade (decrescente) e formata para exibição.
        Mostra mensagem se nenhuma máquina foi vendida. Salva automaticamente
        em arquivo .txt.
        """
        vendas_finalizadas = [
            v for v in self.__controlador_sistema.controlador_venda.vendas if (
                v.status_venda == "Finalizada")]
        contagem_maquinas = {}

        for venda in vendas_finalizadas:
            for produto, quantidade in venda.carrinho.items():
                if isinstance(produto, MaquinaDeCafe):
                    # Usa ID como chave para agrupar produtos iguais
                    maquina_id = produto.id
                    if maquina_id not in contagem_maquinas:
                        contagem_maquinas[maquina_id] = {'produto': produto, 'total': 0}
                    contagem_maquinas[maquina_id]['total'] += quantidade

        maquinas_ordenadas = sorted(
            contagem_maquinas.values(), key=lambda item: item['total'], reverse=True)

        linhas_relatorio = []
        for item in maquinas_ordenadas:
            maquina = item['produto']
            total_vendido = item['total']
            linhas_relatorio.append(
                f"Máquina: {maquina.nome} (ID: {maquina.id}) | "
                f"Total Vendido: {total_vendido} unidades")

        if not linhas_relatorio:
            linhas_relatorio.append("Nenhuma máquina vendida até o momento.")
        self.__salvar_relatorio_em_arquivo("Máquinas Mais Vendidas", linhas_relatorio)
        self.__tela_relatorios.mostra_relatorio(
            "Máquinas Mais Vendidas", linhas_relatorio)

    def relatorio_empresas_fornecedoras_mais_ativas(self):
        """
        Analisa vendas para identificar fornecedores mais ativos. Agrupa
        produtos vendidos por fornecedor (cafés e máquinas), contabiliza
        total de unidades vendidas de cada fornecedor e ordena por volume.
        Usa reflexão para identificar produtos com atributo empresa_fornecedora.
        Salva automaticamente em arquivo .txt.
        """
        vendas_finalizadas = [
            v for v in self.__controlador_sistema.controlador_venda.vendas if (
                v.status_venda == "Finalizada")]
        contagem_empresas = {}

        for venda in vendas_finalizadas:
            for produto, quantidade in venda.carrinho.items():
                if hasattr(produto, 'empresa_fornecedora'):
                    fornecedor = produto.empresa_fornecedora
                    if fornecedor is not None:
                        contagem_empresas[fornecedor] = contagem_empresas.get(
                            fornecedor, 0) + quantidade

        empresas_ordenadas = sorted(
            contagem_empresas.items(), key=lambda item: item[1], reverse=True)

        linhas_relatorio = []
        for empresa, total_vendido in empresas_ordenadas:
            if empresa is not None:
                linhas_relatorio.append(
                    f"Empresa: {empresa.nome} (CNPJ: {empresa.cnpj}) | "
                    f"Total de Produtos Vendidos: {total_vendido} unidades")

        if not linhas_relatorio:
            linhas_relatorio.append(
                "Nenhuma venda de produtos de fornecedores registrada.")

        self.__salvar_relatorio_em_arquivo("Empresas Fornecedoras Mais Ativas", linhas_relatorio)
        self.__tela_relatorios.mostra_relatorio(
            "Empresas Fornecedoras Mais Ativas", linhas_relatorio)

    def relatorio_clientes_por_valor(self):
        """
        Analisa vendas para calcular total gasto por cada cliente. Agrupa
        vendas por ID do cliente, soma valores totais e ordena por valor
        (decrescente). Trata casos onde cliente foi excluído após venda,
        exibindo informação apropriada. Formata dados para exibição e salva
        automaticamente em arquivo .txt.
        """
        gastos_por_cliente = {}
        vendas_finalizadas = [
            v for v in self.__controlador_sistema.controlador_venda.vendas if (
                v.status_venda == "Finalizada")]

        for venda in vendas_finalizadas:
            cliente_id = venda.cliente.id
            gastos_por_cliente[cliente_id] = gastos_por_cliente.get(
                cliente_id, 0) + venda.valor_total

        clientes_ordenados = sorted(
            gastos_por_cliente.items(), key=lambda item: item[1], reverse=True)

        linhas_relatorio = []
        for cliente_id, total_gasto in clientes_ordenados:
            try:
                cliente = self.__controlador_sistema.controlador_cliente.pega_cliente_por_id(
                    cliente_id)
                linhas_relatorio.append(
                    f"Cliente: {cliente.nome} (ID: {cliente_id}) | Total Gasto: R$ {total_gasto:.2f}")
            except ClienteNaoEncontradoException:
                linhas_relatorio.append(
                    f"Cliente ID: {cliente_id} (Excluído) | Total Gasto: R$ {total_gasto:.2f}")

        self.__salvar_relatorio_em_arquivo("Clientes por Valor Gasto", linhas_relatorio)
        self.__tela_relatorios.mostra_relatorio(
            "Clientes por Valor Gasto", linhas_relatorio)

    def relatorio_estoque_baixo(self):
        """
        Identifica produtos com estoque abaixo do limite mínimo (5 unidades).
        Itera sobre todos os produtos em estoque, filtra aqueles com quantidade
        igual ou menor ao limite e formata alerta para exibição. Mostra mensagem
        se nenhum produto estiver com estoque baixo. Salva automaticamente
        em arquivo .txt.
        """
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

        titulo_relatorio = f"Produtos com Estoque Abaixo de {LIMITE_MINIMO} Unidades"
        self.__salvar_relatorio_em_arquivo(titulo_relatorio, linhas_relatorio)
        self.__tela_relatorios.mostra_relatorio(
            titulo_relatorio, linhas_relatorio)

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
            if opcao is None:
                break

            if opcao == 0:
                break

            funcao_escolhida = mapa_opcoes.get(opcao)
            if funcao_escolhida:
                funcao_escolhida()
            else:
                self.__tela_relatorios.mostra_mensagem(
                    "Opção inválida, por favor escolha uma das opções listadas.")
