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
        sg.ChangeLookAndFeel('LightBrown1')

        botoes = [
            [sg.Button('Adicionar Fornecedor', key='1', font='Any 12', expand_x=True)],
            [sg.Button('Alterar Fornecedor', key='2', font='Any 12', expand_x=True)],
            [sg.Button('Listar Fornecedores', key='3', font='Any 12', expand_x=True)],
            [sg.Button('Excluir Fornecedor', key='4', font='Any 12', expand_x=True)],
            [sg.Button('Retornar', key='0', font='Any 12', expand_x=True)]
        ]

        layout = [
            [sg.Column([[sg.Text('Fornecedores de Máquinas', font=("Helvica", 24), pad=((0,0),(20,10)))]], justification='center')],
            [sg.Column([[sg.Text('Escolha uma opção', font=("Helvica", 15), pad=((0,0),(0,20)))]], justification='center')],
            [sg.Column([[sg.Frame('Opções', botoes, font='Any 14')]], justification='center')]
        ]

        self.__window = sg.Window('Fornecedores de Máquinas', layout, element_justification='center', size=(520, 420))

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

        window = sg.Window('Dados do Fornecedor de Máquinas', layout, modal=True)
        dados = None

        while True:
            event, values = window.read()
            if event in (sg.WINDOW_CLOSED, 'Cancelar'):
                break
            if event == 'Salvar':
                obrigatorios = ['nome', 'endereco', 'telefone', 'pais_de_origem']
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
            [sg.Button('Selecionar', bind_return_key=True), sg.Button('Cancelar')]
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
        linhas = ["--- LISTA DE FORNECEDORES DE MÁQUINAS ---"]
        for fornecedor in fornecedores:
            linhas.append(f"NOME: {fornecedor['nome']}")
            linhas.append(f"CNPJ: {fornecedor['cnpj']}")
            linhas.append(f"PAÍS DE ORIGEM: {fornecedor['pais_de_origem']}")
            linhas.append("")
        sg.popup_scrolled('Fornecedores de Máquinas', "\n".join(linhas).strip())

    def mostra_mensagem(self, msg: str) -> None:
        sg.popup("", msg)

    def close(self):
        if self.__window:
            self.__window.Close()
            self.__window = None

    def open(self):
        button, values = self.__window.Read()
        return button, values