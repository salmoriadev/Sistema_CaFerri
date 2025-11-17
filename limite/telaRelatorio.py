"""
    Gerencia a interface com o usuário para a geração e exibição de
    todos os relatórios do sistema.
"""

from typing import List, Optional

import FreeSimpleGUI as sg


class TelaRelatorio:
    def __init__(self):
        self.__window = None

    def init_opcoes(self):
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
        sg.popup("", msg)

    def close(self):
        if self.__window:
            self.__window.Close()
            self.__window = None

    def open(self):
        button, values = self.__window.Read()
        return button, values
