"""    Gerencia a interface com o usuário 
para todas as operações relacionadas a Cafés."""


from datetime import datetime
from typing import Dict, List, Optional

import FreeSimpleGUI as sg


class TelaCafe:
    def __init__(self):
        self.__window = None

    def init_opcoes(self):
        sg.theme('DarkBrown3')
        botoes = [
            [sg.Button('Adicionar Café', key='1', font='Any 14', expand_x=True,
                       button_color=('#F0E6D2', '#8B5A3C'))],
            [sg.Button('Alterar Café', key='2', font='Any 14', expand_x=True,
                       button_color=('#F0E6D2', '#8B5A3C'))],
            [sg.Button('Listar Cafés', key='3', font='Any 14', expand_x=True,
                       button_color=('#F0E6D2', '#8B5A3C'))],
            [sg.Button('Excluir Café', key='4', font='Any 14', expand_x=True,
                       button_color=('#F0E6D2', '#8B5A3C'))],
            [sg.Button('Retornar', key='0', font='Any 14', expand_x=True,
                       button_color=('#F0E6D2', '#8B5A3C'))]
        ]

        layout = [
            [sg.Column([[sg.Text('Cafés', font=('Helvetica', 28), pad=((0, 0), (20, 10)),
                                 text_color='#F0E6D2')]], justification='center', background_color='#6B4423')],
            [sg.Column([[sg.Text('Escolha uma opção', font=('Helvetica', 18), pad=(
                (0, 0), (0, 20)), text_color='#E8D5B7')]], justification='center', background_color='#6B4423')],
            [sg.Column([[sg.Frame('Opções', botoes, font='Any 16', title_color='#F0E6D2',
                                  background_color='#6B4423', border_width=2)]], justification='center', background_color='#6B4423')]
        ]

        self.__window = sg.Window(
            'Gerenciador de Cafés', layout, element_justification='center',
            size=(580, 580), background_color='#6B4423')

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

    def pega_dados_cafe(self, perfil_mapa: dict, is_alteracao: bool = False) -> Optional[dict]:
        perfis_disponiveis = perfil_mapa["perfis_disponiveis"]
        perfil_layout = [
            [sg.Text('Perfil Recomendado:'), sg.Combo(
                perfis_disponiveis, key='perfil_recomendado', readonly=True)]
        ]

        campos = [
            [sg.Text('Nome:'), sg.Input(key='nome')],
            [sg.Text('Preço Compra:'), sg.Input(key='preco_compra')],
            [sg.Text('Preço Venda:'), sg.Input(key='preco_venda')]
        ]

        if not is_alteracao:
            campos.append([sg.Text('ID:'), sg.Input(key='id')])

        campos.extend([
            [sg.Text('Data Fabricação (DD/MM/AAAA):'),
             sg.Input(key='data_fabricacao')],
            [sg.Text('Origem:'), sg.Input(key='origem')],
            [sg.Text('Variedade:'), sg.Input(key='variedade')],
            [sg.Text('Altitude (m):'), sg.Input(key='altitude')],
            [sg.Text('Moagem:'), sg.Input(key='moagem')],
            [sg.Text('Notas Sensoriais:'), sg.Input(key='notas_sensoriais')],
            [sg.Text('CNPJ Fornecedor:'), sg.Input(key='empresa_fornecedora')],
            [sg.Frame('Perfis Disponíveis', perfil_layout)]
        ])

        layout = campos + \
            [[sg.Button('Salvar', bind_return_key=True),
              sg.Button('Cancelar')]]
        window = sg.Window('Dados do Café', layout, modal=True)
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
                        id_cafe = int(values['id'])
                    data_fabricacao = values['data_fabricacao'].strip()
                    datetime.strptime(data_fabricacao, '%d/%m/%Y')
                    origem = values['origem'].strip()
                    variedade = values['variedade'].strip()
                    altitude = int(values['altitude'])
                    moagem = values['moagem'].strip()
                    notas = values['notas_sensoriais'].strip()
                    perfil_recomendado = values['perfil_recomendado']
                    empresa = values['empresa_fornecedora'].strip()

                    if not all([nome, origem, variedade, moagem, notas, empresa, perfil_recomendado]):
                        raise ValueError

                    dados = {
                        "nome": nome,
                        "preco_compra": preco_compra,
                        "preco_venda": preco_venda,
                        "data_fabricacao": data_fabricacao,
                        "origem": origem,
                        "variedade": variedade,
                        "altitude": altitude,
                        "moagem": moagem,
                        "notas_sensoriais": notas,
                        "perfil_recomendado": perfil_recomendado,
                        "empresa_fornecedora": empresa
                    }
                    if not is_alteracao:
                        dados["id"] = id_cafe
                    break
                except (ValueError, TypeError):
                    self.mostra_mensagem(
                        "Preencha todos os campos corretamente.")

        window.close()
        return dados

    def mostra_cafe(self, dados_cafe: dict) -> None:
        texto = (
            f"ID: {dados_cafe['id']}\n"
            f"NOME: {dados_cafe['nome']}\n"
            f"PREÇO VENDA: R$ {dados_cafe['preco_venda']:.2f}\n"
            f"PERFIL: {dados_cafe['perfil_recomendado']}\n"
            f"FORNECEDORA: {dados_cafe['empresa_fornecedora_nome']}"
        )
        sg.popup('Café', texto)

    def seleciona_cafe(self) -> Optional[int]:
        layout = [
            [sg.Text('ID do café:'), sg.Input(key='id')],
            [sg.Button('Selecionar', bind_return_key=True),
             sg.Button('Cancelar')]
        ]
        window = sg.Window('Selecionar Café', layout, modal=True)
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

    def mostra_lista_cafes(self, cafes: List[Dict[str, str]]) -> None:
        sg.theme('DarkBrown3')
        texto = "--- LISTA DE CAFÉS ---\n\n"
        if not cafes:
            texto += "Nenhum café cadastrado."
        else:
            for cafe in cafes:
                texto += f"ID: {cafe['id']} - {cafe['nome']} ({cafe['perfil_recomendado']})\n"

        layout = [
            [sg.Multiline(texto, size=(60, 20), disabled=True,
                          background_color='#6B4423', text_color='#F0E6D2', key='-TEXTO-')],
            [sg.Button('Fechar', button_color=(
                '#F0E6D2', '#8B5A3C'), size=(10, 1))]
        ]

        window = sg.Window('Lista de Cafés', layout, modal=True,
                           background_color='#6B4423', size=(550, 550))

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
