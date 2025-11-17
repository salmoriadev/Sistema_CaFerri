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
        sg.ChangeLookAndFeel('LightBrown1')

        botoes = [
            [sg.Button('Vendas Finalizadas', key='1', expand_x=True)],
            [sg.Button('Clientes por Valor Gasto', key='2', expand_x=True)],
            [sg.Button('Estoque Baixo', key='3', expand_x=True)],
            [sg.Button('Cafés Mais Vendidos', key='4', expand_x=True)],
            [sg.Button('Máquinas Mais Vendidas', key='5', expand_x=True)],
            [sg.Button('Empresas Mais Ativas', key='6', expand_x=True)],
            [sg.Button('Retornar', key='0', expand_x=True)]
        ]

        layout = [
            [sg.Text('Relatórios', font=('Helvetica', 22), justification='center')],
            [sg.Text('Escolha um relatório', font=('Helvetica', 14))],
            [sg.Frame('Opções', botoes, font='Any 12')]
        ]

        self.__window = sg.Window('Relatórios', layout, element_justification='center', size=(480, 360))

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
        texto = f"---------- {titulo.upper()} ----------\n"
        if not linhas_relatorio:
            texto += "Nenhum dado para exibir."
        else:
            texto += "\n".join(linhas_relatorio)
        texto += "\n----------------------------------------"

        sg.popup_scrolled('Relatório', texto, size=(600, 400))

    def mostra_mensagem(self, msg: str):
        sg.popup("", msg)

    def close(self):
        if self.__window:
            self.__window.Close()
            self.__window = None

    def open(self):
        button, values = self.__window.Read()
        return button, values