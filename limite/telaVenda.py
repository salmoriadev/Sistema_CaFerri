"""
    Gerencia a interface com o usuário para todas as operações de Venda.

    Esta classe atua como a camada de apresentação (View) para o módulo de
    vendas no padrão MVC, sendo a única responsável pela interação direta
    com o usuário via interface gráfica (FreeSimpleGUI). Ela isola completamente
    a lógica de visualização, garantindo que o Controlador não precise lidar
    com elementos de tela.

    Responsabilidades e Funcionalidades:

    1. Menu Principal de Vendas (tela_opcoes):
       - Apresenta as operações de alto nível: Iniciar Nova Venda, Listar,
         Excluir (Cancelar) e Gerenciar Venda em Andamento.
       - Retorna um código inteiro para o controlador decidir o fluxo.

    2. Submenu de Gerenciamento (tela_opcoes_gerenciar_venda):
       - Exibido apenas quando uma venda está ativa ("Em andamento").
       - Oferece operações granulares: Adicionar Produto, Diminuir Quantidade,
         Remover Item Inteiro, Listar Carrinho e Finalizar Venda.

    3. Coleta de Dados (pega_dados_...):
       - Utiliza janelas modais (pop-ups) para solicitar informações como
         IDs (venda, cliente, produto) e quantidades.
       - Realiza a validação primária de tipos (ex: garante que IDs sejam
         números inteiros) para evitar erros de execução no controlador.
       - Retorna os dados estruturados em dicionários (ex: {'id_venda': 1, ...})
         ou None caso o usuário cancele a operação.

    4. Exibição de Dados (mostra_venda, mostra_mensagem):
       - Formata os objetos complexos de venda (contendo cliente, status,
         lista de produtos e totais) em um texto legível.
       - Realiza a formatação monetária (R$) que é responsabilidade da View.
       - Exibe listas longas em janelas com barra de rolagem (Scrolled Popup).
       - Padroniza mensagens de feedback (sucesso/erro) em pop-ups simples.

    A classe mantém o estado da janela atual em `self.__window` e gerencia
    o ciclo de vida (abrir/ler/fechar) das janelas do FreeSimpleGUI.
"""

from typing import Dict, List, Optional
import FreeSimpleGUI as sg


class TelaVenda:

    def __init__(self):
        """
        Inicializa a tela de vendas, criando referência para a janela principal
        que será configurada no método init_opcoes.
        """
        self.__window = None

    def init_opcoes(self):
        """
        Configura e cria a janela principal do menu de vendas. Define tema,
        layout com título, subtítulo e botões de opções (Iniciar Nova Venda,
        Listar, Excluir, Gerenciar Venda, Retornar). A janela é armazenada
        em self.__window.
        """
        sg.theme('DarkBrown2')

        botoes_opcoes = [
            [sg.Button('Iniciar Nova Venda', key='1', font='Any 12', pad=(
                5, 5), expand_x=True, button_color=('#F5E6D2', '#9B7A5A'))],
            [sg.Button('Listar Vendas', key='2', font='Any 12', pad=(
                5, 5), expand_x=True, button_color=('#F5E6D2', '#9B7A5A'))],
            [sg.Button('Excluir Venda (Cancelar)', key='3', font='Any 12', pad=(
                5, 5), expand_x=True, button_color=('#F5E6D2', '#9B7A5A'))],
            [sg.Button('Gerenciar Venda em Andamento', key='4', font='Any 12', pad=(
                5, 5), expand_x=True, button_color=('#F5E6D2', '#9B7A5A'))],
            [sg.Button('Retornar', key='0', font='Any 12', pad=(
                5, 5), expand_x=True, button_color=('#F5E6D2', '#9B7A5A'))]
        ]

        layout = [
            [sg.Column([[sg.Text('-------- Vendas ---------', font=("Helvica", 25), pad=((0, 0), (20, 10)),
                       text_color='#F5E6D2')]], justification='center', background_color='#7A5A3A')],
            [sg.Column([[sg.Text('Escolha sua opção', font=("Helvica", 15), pad=(
                (0, 0), (0, 20)), text_color='#E8D5B7')]], justification='center', background_color='#7A5A3A')],
            [sg.Column([[sg.Frame('Opções de Venda', botoes_opcoes, font='Any 14', title_color='#F5E6D2',
                       background_color='#7A5A3A', border_width=2)]], justification='center', background_color='#7A5A3A')]
        ]

        self.__window = sg.Window('Sistema de Vendas', layout, element_justification='center', size=(
            580, 580), background_color='#7A5A3A')

    def tela_opcoes(self) -> int:
        """
        Exibe o menu principal de vendas e captura a escolha do usuário.
        Retorna o código numérico da opção selecionada (1-4) ou 0 para retornar.
        Retorna 0 se a janela for fechada sem seleção válida.
        """
        self.init_opcoes()
        button, _ = self.open()

        if button in (None, '0', 'Retornar'):
            self.close()
            return 0

        opcoes_validas = {'1', '2', '3', '4'}
        if button in opcoes_validas:
            self.close()
            return int(button)

        self.close()
        return 0

    def init_opcoes_gerenciar_venda(self):
        """
        Configura e cria a janela do submenu de gerenciamento de venda em andamento.
        Define tema, layout com título, subtítulo e botões de opções para
        operações no carrinho (Adicionar, Diminuir, Remover, Listar, Finalizar).
        A janela é armazenada em self.__window.
        """
        sg.theme('DarkBrown2')

        botoes_opcoes = [
            [sg.Button('Adicionar Produto', key='1', font='Any 12', pad=(
                5, 5), expand_x=True, button_color=('#F5E6D2', '#9B7A5A'))],
            [sg.Button('Diminuir Quantidade de um Produto', key='2', font='Any 12', pad=(
                5, 5), expand_x=True, button_color=('#F5E6D2', '#9B7A5A'))],
            [sg.Button('Remover Item Inteiro do Carrinho', key='3', font='Any 12', pad=(
                5, 5), expand_x=True, button_color=('#F5E6D2', '#9B7A5A'))],
            [sg.Button('Listar Produtos no Carrinho', key='4', font='Any 12', pad=(
                5, 5), expand_x=True, button_color=('#F5E6D2', '#9B7A5A'))],
            [sg.Button('Finalizar Venda', key='5', font='Any 12', pad=(
                5, 5), expand_x=True, button_color=('#F5E6D2', '#9B7A5A'))],
            [sg.Button('Salvar e Sair', key='0', font='Any 12', pad=(
                5, 5), expand_x=True, button_color=('#F5E6D2', '#9B7A5A'))]
        ]

        layout = [
            [sg.Column([[sg.Text('--- Gerenciando Venda ---', font=("Helvica", 25), pad=((0, 0), (20, 10)),
                       text_color='#F5E6D2')]], justification='center', background_color='#7A5A3A')],
            [sg.Column([[sg.Text('O que deseja fazer?', font=("Helvica", 15), pad=(
                (0, 0), (0, 20)), text_color='#E8D5B7')]], justification='center', background_color='#7A5A3A')],
            [sg.Column([[sg.Frame('Ações do Carrinho', botoes_opcoes, font='Any 14', title_color='#F5E6D2',
                       background_color='#7A5A3A', border_width=2)]], justification='center', background_color='#7A5A3A')]
        ]

        self.__window = sg.Window('Gerenciamento de Venda', layout, element_justification='center', size=(
            580, 580), background_color='#7A5A3A')

    def tela_opcoes_gerenciar_venda(self) -> int:
        """
        Exibe o submenu de gerenciamento de venda e captura a escolha do usuário.
        Retorna o código numérico da opção selecionada (1-5) ou 0 para salvar e sair.
        Retorna 0 se a janela for fechada sem seleção válida.
        """
        self.init_opcoes_gerenciar_venda()
        button, _ = self.open()

        if button in (None, '0', 'Salvar e Sair'):
            self.close()
            return 0

        opcoes_validas = {'1', '2', '3', '4', '5'}
        if button in opcoes_validas:
            self.close()
            return int(button)

        self.close()
        return 0

    def pega_dados_iniciar_venda(self) -> Optional[Dict[str, int]]:
        """
        Exibe formulário modal para iniciar uma nova venda. Solicita ID da venda
        e ID do cliente. Valida que ambos são números inteiros antes de retornar.
        Mantém janela aberta em caso de erro para correção. Retorna dicionário
        com dados validados ou None se cancelado.
        """
        sg.theme('DarkBrown2')
        layout = [
            [sg.Text('Iniciar Nova Venda', font=(
                "Helvica", 18), pad=((0, 0), (10, 10)))],
            [sg.Text('ID da Venda:', size=(15, 1), font='Any 11'),
             sg.Input(key='id_venda')],
            [sg.Text('ID do Cliente:', size=(15, 1), font='Any 11'),
             sg.Input(key='id_cliente')],
            [sg.Button('Confirmar', bind_return_key=True, font='Any 11'),
             sg.Button('Cancelar', font='Any 11')]
        ]

        self.__window = sg.Window(
            'Dados Iniciais', layout, modal=True, element_justification='center')
        dados = None

        while True:
            event, values = self.open()
            if event in (sg.WINDOW_CLOSED, 'Cancelar'):
                break
            if event == 'Confirmar':
                try:
                    id_venda = int(values['id_venda'])
                    id_cliente = int(values['id_cliente'])
                    dados = {"id_venda": id_venda, "id_cliente": id_cliente}
                    break
                except ValueError:
                    self.mostra_mensagem("IDs devem ser números inteiros.")

        self.close()
        return dados

    def pega_dados_produto(self) -> Optional[Dict[str, int]]:
        """
        Exibe formulário modal para coleta de dados de produto (ID e quantidade).
        Valida que ambos são números inteiros antes de retornar. Mantém janela
        aberta em caso de erro para correção. Retorna dicionário com dados
        validados ou None se cancelado.
        """
        sg.theme('DarkBrown2')
        layout = [
            [sg.Text('Dados do Produto', font=(
                "Helvica", 18), pad=((0, 0), (10, 10)))],
            [sg.Text('ID do Produto:', size=(15, 1), font='Any 11'),
             sg.Input(key='id_produto')],
            [sg.Text('Quantidade:', size=(15, 1), font='Any 11'),
             sg.Input(key='quantidade')],
            [sg.Button('Confirmar', bind_return_key=True, font='Any 11'),
             sg.Button('Cancelar', font='Any 11')]
        ]

        self.__window = sg.Window(
            'Selecionar Produto', layout, modal=True, element_justification='center')
        dados = None

        while True:
            event, values = self.open()
            if event in (sg.WINDOW_CLOSED, 'Cancelar'):
                break
            if event == 'Confirmar':
                try:
                    id_produto = int(values['id_produto'])
                    quantidade = int(values['quantidade'])
                    dados = {"id_produto": id_produto,
                             "quantidade": quantidade}
                    break
                except ValueError:
                    self.mostra_mensagem(
                        "ID e Quantidade devem ser números inteiros.")

        self.close()
        return dados

    def seleciona_venda(self) -> Optional[int]:
        """
        Exibe janela modal para seleção de venda por ID. Valida que o ID
        é um número inteiro antes de retornar. Retorna None se cancelado
        ou se ID inválido após tentativas de correção.
        """
        sg.theme('DarkBrown2')
        layout = [
            [sg.Text('Selecionar Venda', font=(
                "Helvica", 18), pad=((0, 0), (10, 10)))],
            [sg.Text('ID da Venda:', size=(15, 1), font='Any 11'),
             sg.Input(key='id_venda')],
            [sg.Button('Confirmar', bind_return_key=True, font='Any 11'),
             sg.Button('Cancelar', font='Any 11')]
        ]

        self.__window = sg.Window(
            'Seleção', layout, modal=True, element_justification='center')
        id_venda = None

        while True:
            event, values = self.open()
            if event in (sg.WINDOW_CLOSED, 'Cancelar'):
                break
            if event == 'Confirmar':
                try:
                    id_venda = int(values['id_venda'])
                    break
                except ValueError:
                    self.mostra_mensagem("O ID deve ser um número inteiro.")

        self.close()
        return id_venda

    def mostra_venda(self, dados_venda: dict) -> None:
        """
        Exibe detalhes completos de uma venda em janela modal com área de texto
        scrollável. Formata informações da venda incluindo ID, cliente, status,
        lista de produtos no carrinho com quantidades e subtotais, e valor total.
        Exibe mensagem apropriada se carrinho estiver vazio. Janela permanece
        aberta até usuário fechar explicitamente.
        """
        sg.theme('DarkBrown2')
        texto = "------------------------------\n"
        texto += f"ID da Venda: {dados_venda['id_venda']}\n"
        texto += f"Cliente: {dados_venda['cliente_nome']}\n"
        texto += f"Status: {dados_venda['status']}\n"
        texto += "\nProdutos no Carrinho:\n"

        if dados_venda['produtos']:
            for item in dados_venda['produtos']:
                texto += f"  - {item['nome']} | Qtd: {item['quantidade']} | Unit: {item['preco_unitario']} | Subtotal: {item['subtotal']}\n"
        else:
            texto += "  (Carrinho vazio)\n"

        texto += f"\nVALOR TOTAL: R$ {dados_venda['valor_total']:.2f}\n"
        texto += "------------------------------"

        layout = [
            [sg.Multiline(texto, size=(60, 20), disabled=True,
                          background_color='#7A5A3A', text_color='#F5E6D2', key='-TEXTO-')],
            [sg.Button('Fechar', button_color=(
                '#F5E6D2', '#9B7A5A'), size=(10, 1))]
        ]

        window = sg.Window('Detalhes da Venda', layout, modal=True,
                           background_color='#7A5A3A', size=(550, 550))

        while True:
            event, _ = window.read()
            if event in (sg.WINDOW_CLOSED, 'Fechar'):
                break

        window.close()

    def mostra_lista_vendas(self, vendas: List[Dict[str, str]]) -> None:
        """
        Exibe lista formatada de todas as vendas registradas em janela modal
        com área de texto scrollável. Formata cada venda com ID, nome do cliente,
        status e valor total. Exibe mensagem apropriada se lista estiver vazia.
        Janela permanece aberta até usuário fechar explicitamente.
        """
        sg.theme('DarkBrown2')
        texto = "--- LISTA DE VENDAS ---\n\n"
        if not vendas:
            texto += "Nenhuma venda registrada."
        else:
            for venda in vendas:
                texto += f"ID: {venda['id_venda']} | Cliente: {venda['cliente_nome']} | "
                texto += f"Status: {venda['status']} | Total: R$ {venda['valor_total']:.2f}\n"

        layout = [
            [sg.Multiline(texto, size=(60, 20), disabled=True,
                          background_color='#7A5A3A', text_color='#F5E6D2', key='-TEXTO-')],
            [sg.Button('Fechar', button_color=(
                '#F5E6D2', '#9B7A5A'), size=(10, 1))]
        ]

        window = sg.Window('Lista de Vendas', layout, modal=True,
                           background_color='#7A5A3A', size=(550, 550))

        while True:
            event, _ = window.read()
            if event in (sg.WINDOW_CLOSED, 'Fechar'):
                break

        window.close()

    def mostra_mensagem(self, msg: str) -> None:
        """
        Exibe mensagem de feedback (sucesso, erro, aviso) em popup simples.
        Usado pelo controlador para comunicar resultados de operações ao usuário.
        """
        sg.popup("", msg, font='Any 12')

    def close(self):
        """
        Fecha a janela principal se estiver aberta e limpa a referência.
        Previne vazamentos de memória e garante que janelas não permaneçam
        abertas após uso.
        """
        if self.__window:
            self.__window.Close()
            self.__window = None

    def open(self):
        """
        Lê eventos da janela principal (cliques de botão, fechamento).
        Retorna tupla com o botão pressionado e valores dos campos de entrada.
        Método de baixo nível usado internamente por outros métodos da classe.
        """
        button, values = self.__window.Read()
        return button, values
