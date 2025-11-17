"""Gerencia a interface com o usuário para todas as operações relacionadas a Máquinas de Café."""

from datetime import datetime
from typing import Dict, List, Optional

import FreeSimpleGUI as sg


class TelaMaquinaCafe:
    def __init__(self):
        self.__window = None

    def init_opcoes(self):
        sg.ChangeLookAndFeel('LightBrown1')
        botoes = [
            [sg.Button('Adicionar Máquina', key='1', expand_x=True)],
            [sg.Button('Alterar Máquina', key='2', expand_x=True)],
            [sg.Button('Listar Máquinas', key='3', expand_x=True)],
            [sg.Button('Excluir Máquina', key='4', expand_x=True)],
            [sg.Button('Retornar', key='0', expand_x=True)]
        ]

        layout = [
            [sg.Text('Máquinas de Café', font=('Helvetica', 22), justification='center')],
            [sg.Text('Escolha uma opção', font=('Helvetica', 14))],
            [sg.Frame('Opções', botoes, font='Any 12')]
        ]

        self.__window = sg.Window('Gerenciador de Máquinas', layout, element_justification='center', size=(460, 320))

    def tela_opcoes(self) -> Optional[int]:
        self.init_opcoes()
        button, _ = self.open()

        if button in (None, '0', 'Retornar'):
            self.close()
            return 0

        if button in {'1', '2', '3', '4'}:
            self.close()
            return int(button)

        self.close()
        return None

    def pega_dados_maquina(self, is_alteracao: bool = False) -> Optional[dict]:
        campos = [
            [sg.Text('Nome:'), sg.Input(key='nome')],
            [sg.Text('Preço Compra:'), sg.Input(key='preco_compra')],
            [sg.Text('Preço Venda:'), sg.Input(key='preco_venda')]
        ]

        if not is_alteracao:
            campos.append([sg.Text('ID:'), sg.Input(key='id')])

        campos.extend([
            [sg.Text('Data Fabricação (DD/MM/AAAA):'), sg.Input(key='data_fabricacao')],
            [sg.Text('CNPJ Fornecedor:'), sg.Input(key='empresa_fornecedora')]
        ])

        layout = campos + [[sg.Button('Salvar', bind_return_key=True), sg.Button('Cancelar')]]
        window = sg.Window('Dados da Máquina', layout, modal=True)
        dados = None

        while True:
            event, values = window.read()
            if event in (sg.WINDOW_CLOSED, 'Cancelar'):
                break
            if event == 'Salvar':
                try:
                    nome = values['nome'].strip()
                    preco_compra = float(values['preco_compra'])
                    preco_venda = float(values['preco_venda'])
                    if not is_alteracao:
                        id_maquina = int(values['id'])
                    data_fabricacao = values['data_fabricacao'].strip()
                    datetime.strptime(data_fabricacao, '%d/%m/%Y')
                    empresa = values['empresa_fornecedora'].strip()

                    if not all([nome, empresa]):
                        raise ValueError

                    dados = {
                        "nome": nome,
                        "preco_compra": preco_compra,
                        "preco_venda": preco_venda,
                        "data_fabricacao": data_fabricacao,
                        "empresa_fornecedora": empresa
                    }
                    if not is_alteracao:
                        dados["id"] = id_maquina
                    break
                except (ValueError, TypeError):
                    self.mostra_mensagem("Preencha todos os campos corretamente.")

        window.close()
        return dados

    def mostra_maquina(self, dados_maquina: dict) -> None:
        texto = (
            f"ID: {dados_maquina['id']}\n"
            f"NOME: {dados_maquina['nome']}\n"
            f"PREÇO VENDA: R$ {dados_maquina['preco_venda']:.2f}\n"
            f"FORNECEDORA: {dados_maquina['empresa_fornecedora_nome']}"
        )
        sg.popup('Máquina de Café', texto)

    def seleciona_maquina(self) -> Optional[int]:
        layout = [
            [sg.Text('ID da máquina:'), sg.Input(key='id')],
            [sg.Button('Selecionar', bind_return_key=True), sg.Button('Cancelar')]
        ]
        window = sg.Window('Selecionar Máquina', layout, modal=True)
        id_escolhido = None

        while True:
            event, values = window.read()
            if event in (sg.WINDOW_CLOSED, 'Cancelar'):
                break
            if event == 'Selecionar':
                try:
                    id_escolhido = int(values['id'])
                    break
                except (ValueError, TypeError):
                    self.mostra_mensagem("ID inválido.")

        window.close()
        return id_escolhido

    def mostra_lista_maquinas(self, maquinas: List[Dict[str, str]]) -> None:
        linhas = ["--- LISTA DE MÁQUINAS ---"]
        for maquina in maquinas:
            linhas.append(f"ID: {maquina['id']} - {maquina['nome']}")
        sg.popup_scrolled('Máquinas de Café', "\n".join(linhas).strip())

    def mostra_mensagem(self, msg: str) -> None:
        sg.popup("", msg)

    def close(self):
        if self.__window:
            self.__window.Close()
            self.__window = None

    def open(self):
        button, values = self.__window.Read()
        return button, values
