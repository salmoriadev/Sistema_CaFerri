"""
    Gerencia a interface com o usuário para todas as operações de Estoque.

    Esta classe atua como a camada de apresentação (View) para o módulo de
    controle de estoque.
"""
from typing import Dict, List, Optional, Union

import FreeSimpleGUI as sg


class TelaEstoque:

    def __init__(self):
        self.__window = None

    def init_opcoes(self):
        sg.ChangeLookAndFeel('BluePurple') 
        
        botoes_opcoes = [
            [sg.Button('Listar Inventário', key='1', font='Any 12', pad=(5, 5), expand_x=True)],
            [sg.Button('Adicionar Novo Produto ao Estoque', key='2', font='Any 12', pad=(5, 5), expand_x=True)],
            [sg.Button('Repor Estoque de um Produto', key='3', font='Any 12', pad=(5, 5), expand_x=True)],
            [sg.Button('Dar Baixa Manual de um Produto', key='4', font='Any 12', pad=(5, 5), expand_x=True)],
            [sg.Button('Retornar', key='0', font='Any 12', pad=(5, 5), expand_x=True)]
        ]

        layout = [
            [sg.Column([[sg.Text('-------- Estoque ---------', font=("Helvica", 25), pad=((0,0),(20,10)))]], justification='center')],
            [sg.Column([[sg.Text('Escolha sua opção', font=("Helvica", 15), pad=((0,0),(0,20)))]], justification='center')],
            [sg.Column([[sg.Frame('Opções de Estoque', botoes_opcoes, font='Any 14', title_color='black')]], justification='center')]
        ]
        
        self.__window = sg.Window('Gerenciador de Estoque', layout, element_justification='center', size=(550, 400))

    def tela_opcoes(self) -> int:
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
                        self.mostra_mensagem("Quantidade não pode ser negativa.")
                        continue
                    dados = {"id_produto": id_produto, "quantidade": quantidade}
                    break
                except (ValueError, TypeError):
                    self.mostra_mensagem("IDs e quantidade devem ser números inteiros.")

        window.close()
        return dados

    def mostra_inventario(self, itens: List[Dict[str, Union[str, int]]]) -> None:
        linhas = ["---------- INVENTÁRIO ATUAL ----------"]
        for item in itens:
            linhas.append(
                f"-> PRODUTO: {item['nome']} (ID: {item['id']}) | QUANTIDADE: {item['quantidade']}"
            )
        linhas.append("------------------------------------")
        sg.popup_scrolled('Inventário', "\n".join(linhas))

    def mostra_mensagem(self, msg: str) -> None:
        sg.popup("", msg)

    def close(self):
        if self.__window:
            self.__window.Close()
            self.__window = None

    def open(self):
        button, values = self.__window.Read()
        return button, values