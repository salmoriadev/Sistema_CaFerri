""" Gerencia a interface com o usuário para todas as operações relacionadas
    aos Fornecedores de Máquinas.

    Esta classe atua como a camada de apresentação (View) dedicada à entidade
    `FornecedoraMaquina. Sua função é ser a ponte entre o usuário e o sistema,
    sendo responsável por toda a interação via console para este módulo.
"""

from typing import Dict, List, Optional

import FreeSimpleGUI as sg


class TelaEmpresaMaquina:
    def __init__(self):
        self.__window = None

    def init_opcoes(self):
        sg.theme('DarkBlue3')

        botoes = [
            [sg.Button('Adicionar Fornecedor', key='1', font='Any 14',
                       expand_x=True, button_color=('#E0E8F0', '#6B7A8B'))],
            [sg.Button('Alterar Fornecedor', key='2', font='Any 14',
                       expand_x=True, button_color=('#E0E8F0', '#6B7A8B'))],
            [sg.Button('Listar Fornecedores', key='3', font='Any 14',
                       expand_x=True, button_color=('#E0E8F0', '#6B7A8B'))],
            [sg.Button('Excluir Fornecedor', key='4', font='Any 14',
                       expand_x=True, button_color=('#E0E8F0', '#6B7A8B'))],
            [sg.Button('Retornar', key='0', font='Any 14',
                       expand_x=True, button_color=('#E0E8F0', '#6B7A8B'))]
        ]

        layout = [
            [sg.Column([[sg.Text('Fornecedores de Máquinas', font=("Helvica", 28), pad=(
                (0, 0), (20, 10)), text_color='#E0E8F0')]], justification='center', background_color='#4A5A6B')],
            [sg.Column([[sg.Text('Escolha uma opção', font=("Helvica", 18), pad=(
                (0, 0), (0, 20)), text_color='#D4DCE8')]], justification='center', background_color='#4A5A6B')],
            [sg.Column([[sg.Frame('Opções', botoes, font='Any 16', title_color='#E0E8F0',
                       background_color='#4A5A6B', border_width=2)]], justification='center', background_color='#4A5A6B')]
        ]

        self.__window = sg.Window('Fornecedores de Máquinas', layout, element_justification='center', size=(
            580, 580), background_color='#4A5A6B')

    def tela_opcoes(self) -> int:
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

    def pega_dados_empresa_maquina(self, is_alteracao: bool = False) -> Optional[dict]:
        campos = [
            [sg.Text('Nome:'), sg.Input(key='nome')],
            [sg.Text('Endereço:'), sg.Input(key='endereco')],
            [sg.Text('Telefone:'), sg.Input(key='telefone')],
            [sg.Text('País de Origem:'), sg.Input(key='pais_de_origem')]
        ]

        if not is_alteracao:
            campos.insert(1, [sg.Text('CNPJ:'), sg.Input(key='cnpj')])

        layout = campos + [
            [sg.Button('Salvar', bind_return_key=True), sg.Button('Cancelar')]
        ]

        window = sg.Window(
            'Dados do Fornecedor de Máquinas', layout, modal=True)
        dados = None

        while True:
            event, values = window.read()
            if event in (sg.WINDOW_CLOSED, 'Cancelar'):
                break
            if event == 'Salvar':
                obrigatorios = ['nome', 'endereco',
                                'telefone', 'pais_de_origem']
                if not is_alteracao:
                    obrigatorios.append('cnpj')

                if all(values.get(campo, '').strip() for campo in obrigatorios):
                    dados = {
                        "nome": values['nome'].strip(),
                        "endereco": values['endereco'].strip(),
                        "telefone": values['telefone'].strip(),
                        "pais_de_origem": values['pais_de_origem'].strip()
                    }
                    if not is_alteracao:
                        dados["cnpj"] = values['cnpj'].strip()
                    break
                self.mostra_mensagem("Preencha todos os campos obrigatórios.")

        window.close()
        return dados

    def mostra_empresa_maquina(self, dados_empresa: dict) -> None:
        texto = (
            f"NOME: {dados_empresa['nome']}\n"
            f"CNPJ: {dados_empresa.get('cnpj', '-')}\n"
            f"PAÍS DE ORIGEM: {dados_empresa['pais_de_origem']}"
        )
        sg.popup('Fornecedor de Máquinas', texto)

    def seleciona_empresa_maquina(self) -> Optional[str]:
        layout = [
            [sg.Text('CNPJ do fornecedor:'), sg.Input(key='cnpj')],
            [sg.Button('Selecionar', bind_return_key=True),
             sg.Button('Cancelar')]
        ]
        window = sg.Window('Selecionar Fornecedor', layout, modal=True)
        cnpj_escolhido = None

        while True:
            event, values = window.read()
            if event in (sg.WINDOW_CLOSED, 'Cancelar'):
                break
            if event == 'Selecionar':
                if values['cnpj'].strip():
                    cnpj_escolhido = values['cnpj'].strip()
                    break
                self.mostra_mensagem("O CNPJ não pode ser vazio.")

        window.close()
        return cnpj_escolhido

    def mostra_lista_fornecedores(self, fornecedores: List[Dict[str, str]]) -> None:
        sg.theme('DarkBlue3')
        texto = "--- LISTA DE FORNECEDORES DE MÁQUINAS ---\n\n"
        if not fornecedores:
            texto += "Nenhum fornecedor cadastrado."
        else:
            for fornecedor in fornecedores:
                texto += f"NOME: {fornecedor['nome']}\n"
                texto += f"CNPJ: {fornecedor['cnpj']}\n"
                texto += f"PAÍS DE ORIGEM: {fornecedor['pais_de_origem']}\n\n"

        layout = [
            [sg.Multiline(texto, size=(60, 20), disabled=True,
                          background_color='#4A5A6B', text_color='#E0E8F0', key='-TEXTO-')],
            [sg.Button('Fechar', button_color=(
                '#E0E8F0', '#6B7A8B'), size=(10, 1))]
        ]

        window = sg.Window('Fornecedores de Máquinas', layout,
                           modal=True, background_color='#4A5A6B', size=(550, 550))

        while True:
            event, _ = window.read()
            if event in (sg.WINDOW_CLOSED, 'Fechar'):
                break

        window.close()

    def mostra_mensagem(self, msg: str) -> None:
        sg.popup("", msg)

    def close(self):
        if self.__window:
            self.__window.Close()
            self.__window = None

    def open(self):
        button, values = self.__window.Read()
        return button, values
