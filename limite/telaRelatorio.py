"""
Gerencia a interface gráfica para a geração e exibição de todos os relatórios do sistema.

Esta classe atua como a camada de apresentação (View) no padrão MVC para o
módulo de relatórios. Utiliza FreeSimpleGUI para criar interfaces gráficas modais,
isolando a lógica de visualização do controlador.

Responsabilidades:
- Exibir menu principal com opções de relatórios disponíveis
- Exibir relatórios formatados em janelas scrolláveis
- Gerenciar ciclo de vida das janelas (abrir/fechar)
- Formatar dados de relatórios para exibição legível
"""

from typing import List, Optional

import FreeSimpleGUI as sg


class TelaRelatorio:
    def __init__(self):
        """
        Inicializa a tela de relatórios, criando referência para a janela principal
        que será configurada no método init_opcoes.
        """
        self.__window = None

    def init_opcoes(self):
        """
        Configura e cria a janela principal do menu de relatórios. Define tema,
        layout com título, subtítulo e botões de opções para cada tipo de
        relatório disponível. A janela é armazenada em self.__window.
        """
        sg.theme('DarkBrown4')

        botoes = [
            [sg.Button('Vendas Finalizadas', key='1', font='Any 14', expand_x=True,
                       button_color=('#E8D5B7', '#5C3D2E'))],
            [sg.Button('Clientes por Valor Gasto', key='2', font='Any 14',
                       expand_x=True, button_color=('#E8D5B7', '#5C3D2E'))],
            [sg.Button('Estoque Baixo', key='3', font='Any 14', expand_x=True,
                       button_color=('#E8D5B7', '#5C3D2E'))],
            [sg.Button('Cafés Mais Vendidos', key='4', font='Any 14', expand_x=True,
                       button_color=('#E8D5B7', '#5C3D2E'))],
            [sg.Button('Máquinas Mais Vendidas', key='5', font='Any 14',
                       expand_x=True, button_color=('#E8D5B7', '#5C3D2E'))],
            [sg.Button('Empresas Mais Ativas', key='6', font='Any 14', expand_x=True,
                       button_color=('#E8D5B7', '#5C3D2E'))],
            [sg.Button('Retornar', key='0', font='Any 14', expand_x=True,
                       button_color=('#E8D5B7', '#5C3D2E'))]
        ]

        layout = [
            [sg.Column([[sg.Text('Relatórios', font=('Helvetica', 28), pad=((0, 0), (20, 10)),
                                 text_color='#E8D5B7')]], justification='center', background_color='#3D2817')],
            [sg.Column([[sg.Text('Escolha um relatório', font=('Helvetica', 18), pad=(
                (0, 0), (0, 20)), text_color='#D4C4A8')]], justification='center', background_color='#3D2817')],
            [sg.Column([[sg.Frame('Opções', botoes, font='Any 16', title_color='#E8D5B7',
                                  background_color='#3D2817', border_width=2)]], justification='center', background_color='#3D2817')]
        ]

        self.__window = sg.Window('Relatórios', layout, element_justification='center', size=(
            580, 580), background_color='#3D2817')

    def tela_opcoes(self) -> Optional[int]:
        """
        Exibe o menu principal de relatórios e captura a escolha do usuário.
        Retorna o código numérico da opção selecionada (1-6) ou 0 para retornar.
        Retorna None se a janela for fechada sem seleção válida.
        """
        self.init_opcoes()
        button, _ = self.open()

        if button in (None, '0', 'Retornar'):
            self.close()
            return 0

        if button in {'1', '2', '3', '4', '5', '6'}:
            self.close()
            return int(button)

        self.close()
        return None

    def mostra_relatorio(self, titulo: str, linhas_relatorio: List[str]):
        """
        Exibe relatório formatado em janela modal com área de texto scrollável.
        Recebe título do relatório e lista de linhas formatadas. Adiciona
        cabeçalho e rodapé para melhor legibilidade. Janela permanece aberta
        até usuário fechar explicitamente. Exibe mensagem apropriada se não
        houver dados para exibir.
        """
        sg.theme('DarkBrown4')
        texto = f"---------- {titulo.upper()} ----------\n\n"
        if not linhas_relatorio:
            texto += "Nenhum dado para exibir."
        else:
            texto += "\n".join(linhas_relatorio)
        texto += "\n\n----------------------------------------"

        layout = [
            [sg.Multiline(texto, size=(60, 20), disabled=True,
                          background_color='#3D2817', text_color='#E8D5B7', key='-TEXTO-')],
            [sg.Button('Fechar', button_color=(
                '#E8D5B7', '#5C3D2E'), size=(10, 1))]
        ]

        window = sg.Window('Relatório', layout, modal=True,
                           background_color='#3D2817', size=(550, 550))

        while True:
            event, _ = window.read()
            if event in (sg.WINDOW_CLOSED, 'Fechar'):
                break

        window.close()

    def mostra_mensagem(self, msg: str):
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
