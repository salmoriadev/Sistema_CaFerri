"""
Gerencia a interface gráfica para todas as operações de Estoque.

Esta classe atua como a camada de apresentação (View) no padrão MVC para o
módulo de controle de estoque. Utiliza FreeSimpleGUI para criar interfaces
gráficas modais, isolando a lógica de visualização do controlador.

Responsabilidades:
- Exibir menu principal com opções de gerenciamento de estoque
- Coletar dados de produtos e quantidades através de formulários validados
- Exibir inventário completo formatado
- Gerenciar ciclo de vida das janelas (abrir/fechar)
- Validar entradas do usuário (IDs e quantidades) antes de retornar dados
"""
from typing import Dict, List, Optional, Union

import FreeSimpleGUI as sg


class TelaEstoque:

    def __init__(self):
        """
        Inicializa a tela de estoque, criando referência para a janela principal
        que será configurada no método init_opcoes.
        """
        self.__window = None

    def init_opcoes(self):
        """
        Configura e cria a janela principal do menu de estoque. Define tema,
        layout com título, subtítulo e botões de opções (Listar, Adicionar,
        Repor, Baixa Manual, Retornar). A janela é armazenada em self.__window.
        """
        sg.theme('DarkBrown2')

        botoes_opcoes = [
            [sg.Button('Listar Inventário', key='1', font='Any 12', pad=(
                5, 5), expand_x=True, button_color=('#F5E6D2', '#9B7A5A'))],
            [sg.Button('Adicionar Novo Produto ao Estoque', key='2', font='Any 12', pad=(
                5, 5), expand_x=True, button_color=('#F5E6D2', '#9B7A5A'))],
            [sg.Button('Repor Estoque de um Produto', key='3', font='Any 12', pad=(
                5, 5), expand_x=True, button_color=('#F5E6D2', '#9B7A5A'))],
            [sg.Button('Dar Baixa Manual de um Produto', key='4', font='Any 12', pad=(
                5, 5), expand_x=True, button_color=('#F5E6D2', '#9B7A5A'))],
            [sg.Button('Retornar', key='0', font='Any 12', pad=(
                5, 5), expand_x=True, button_color=('#F5E6D2', '#9B7A5A'))]
        ]

        layout = [
            [sg.Column([[sg.Text('-------- Estoque ---------', font=("Helvica", 25), pad=((0, 0),
                       (20, 10)), text_color='#F5E6D2')]], justification='center', background_color='#7A5A3A')],
            [sg.Column([[sg.Text('Escolha sua opção', font=("Helvica", 15), pad=(
                (0, 0), (0, 20)), text_color='#E8D5B7')]], justification='center', background_color='#7A5A3A')],
            [sg.Column([[sg.Frame('Opções de Estoque', botoes_opcoes, font='Any 14', title_color='#F5E6D2',
                       background_color='#7A5A3A', border_width=2)]], justification='center', background_color='#7A5A3A')]
        ]

        self.__window = sg.Window('Gerenciador de Estoque', layout, element_justification='center', size=(
            580, 580), background_color='#7A5A3A')

    def tela_opcoes(self) -> int:
        """
        Exibe o menu principal de estoque e captura a escolha do usuário.
        Retorna o código numérico da opção selecionada (1-4) ou 0 para retornar.
        Retorna None se a janela for fechada sem seleção válida.
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
        return None

    def pega_dados_produto_estoque(self) -> Optional[Dict[str, int]]:
        """
        Exibe formulário modal para coleta de ID do produto e quantidade.
        Valida que ambos são números inteiros e que quantidade não é negativa.
        Mantém janela aberta em caso de erro para correção. Retorna dicionário
        com dados validados ou None se cancelado.
        """
        layout = [
            [sg.Text('ID do Produto:'), sg.Input(key='id_produto')],
            [sg.Text('Quantidade:'), sg.Input(key='quantidade')],
            [sg.Button('Salvar', bind_return_key=True), sg.Button('Cancelar')]
        ]

        window = sg.Window('Dados do Estoque', layout, modal=True)
        dados = None

        while True:
            event, values = window.read()
            if event in (sg.WINDOW_CLOSED, 'Cancelar'):
                break
            if event == 'Salvar':
                try:
                    id_produto = int(values['id_produto'])
                    quantidade = int(values['quantidade'])
                    if quantidade < 0:
                        self.mostra_mensagem(
                            "Quantidade não pode ser negativa.")
                        continue
                    dados = {"id_produto": id_produto,
                             "quantidade": quantidade}
                    break
                except (ValueError, TypeError):
                    self.mostra_mensagem(
                        "IDs e quantidade devem ser números inteiros.")

        window.close()
        return dados

    def mostra_inventario(self, itens: List[Dict[str, Union[str, int]]]) -> None:
        """
        Exibe inventário completo em popup scrollável. Formata cada item com
        nome do produto, ID e quantidade disponível. Usa popup_scrolled para
        permitir visualização de listas longas. Exibe cabeçalho e rodapé
        formatados para melhor legibilidade.
        """
        linhas = ["---------- INVENTÁRIO ATUAL ----------"]
        for item in itens:
            linhas.append(
                f"-> PRODUTO: {item['nome']} (ID: {item['id']}) | QUANTIDADE: {item['quantidade']}"
            )
        linhas.append("------------------------------------")
        sg.popup_scrolled('Inventário', "\n".join(linhas))

    def mostra_mensagem(self, msg: str) -> None:
        """
        Exibe mensagem de feedback (sucesso, erro, aviso) em popup simples.
        Usado pelo controlador para comunicar resultados de operações ao usuário.
        """
        sg.popup("", msg)

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
