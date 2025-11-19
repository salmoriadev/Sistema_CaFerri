"""
Gerencia a interface gráfica para todas as operações relacionadas a Máquinas de Café.

Esta classe atua como a camada de apresentação (View) no padrão MVC para o
módulo de gerenciamento de máquinas. Utiliza FreeSimpleGUI para criar interfaces
gráficas modais, isolando a lógica de visualização do controlador.

Responsabilidades:
- Exibir menu principal com opções de CRUD para máquinas
- Coletar dados do usuário através de formulários validados
- Exibir listas e detalhes de máquinas formatados
- Gerenciar ciclo de vida das janelas (abrir/fechar)
- Validar entradas do usuário antes de retornar dados ao controlador
"""

from datetime import datetime
from typing import Dict, List, Optional

import FreeSimpleGUI as sg


class TelaMaquinaCafe:
    def __init__(self):
        """
        Inicializa a tela de máquinas, criando referência para a janela principal
        que será configurada no método init_opcoes.
        """
        self.__window = None

    def init_opcoes(self):
        """
        Configura e cria a janela principal do menu de máquinas. Define tema,
        layout com título, subtítulo e botões de opções (Adicionar, Alterar,
        Listar, Excluir, Retornar). A janela é armazenada em self.__window.
        """
        sg.theme('DarkBlue3')
        botoes = [
            [sg.Button('Adicionar Máquina', key='1', font='Any 14', expand_x=True,
                       button_color=('#E0E8F0', '#6B7A8B'))],
            [sg.Button('Alterar Máquina', key='2', font='Any 14', expand_x=True,
                       button_color=('#E0E8F0', '#6B7A8B'))],
            [sg.Button('Listar Máquinas', key='3', font='Any 14', expand_x=True,
                       button_color=('#E0E8F0', '#6B7A8B'))],
            [sg.Button('Excluir Máquina', key='4', font='Any 14', expand_x=True,
                       button_color=('#E0E8F0', '#6B7A8B'))],
            [sg.Button('Retornar', key='0', font='Any 14', expand_x=True,
                       button_color=('#E0E8F0', '#6B7A8B'))]
        ]

        layout = [
            [sg.Column([[sg.Text('Máquinas de Café', font=('Helvetica', 28), pad=((0, 0), (20, 10)),
                                 text_color='#E0E8F0')]], justification='center', background_color='#4A5A6B')],
            [sg.Column([[sg.Text('Escolha uma opção', font=('Helvetica', 18), pad=(
                (0, 0), (0, 20)), text_color='#D4DCE8')]], justification='center', background_color='#4A5A6B')],
            [sg.Column([[sg.Frame('Opções', botoes, font='Any 16', title_color='#E0E8F0',
                                  background_color='#4A5A6B', border_width=2)]], justification='center', background_color='#4A5A6B')]
        ]

        self.__window = sg.Window('Gerenciador de Máquinas', layout, element_justification='center', size=(
            580, 580), background_color='#4A5A6B')

    def tela_opcoes(self) -> Optional[int]:
        """
        Exibe o menu principal de máquinas e captura a escolha do usuário.
        Retorna o código numérico da opção selecionada (1-4) ou 0 para retornar.
        Retorna None se a janela for fechada sem seleção válida.
        """
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
        """
        Exibe formulário modal para coleta de dados de uma máquina. Adapta campos
        conforme contexto: oculta ID em alterações (imutável). Valida todos os
        campos (tipos numéricos, formato de data DD/MM/AAAA, campos obrigatórios)
        antes de retornar. Mantém janela aberta em caso de erro para correção.
        Retorna dicionário com dados validados ou None se cancelado.
        """
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
            [sg.Text('CNPJ Fornecedor:'), sg.Input(key='empresa_fornecedora')]
        ])

        layout = campos + \
            [[sg.Button('Salvar', bind_return_key=True),
              sg.Button('Cancelar')]]
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
                    self.mostra_mensagem(
                        "Preencha todos os campos corretamente.")

        window.close()
        return dados

    def mostra_maquina(self, dados_maquina: dict) -> None:
        """
        Exibe detalhes de uma máquina específica em popup formatado. Recebe
        dicionário com dados da máquina e formata para exibição legível,
        incluindo formatação monetária para preço.
        """
        texto = (
            f"ID: {dados_maquina['id']}\n"
            f"NOME: {dados_maquina['nome']}\n"
            f"PREÇO VENDA: R$ {dados_maquina['preco_venda']:.2f}\n"
            f"FORNECEDORA: {dados_maquina['empresa_fornecedora_nome']}"
        )
        sg.popup('Máquina de Café', texto)

    def seleciona_maquina(self) -> Optional[int]:
        """
        Exibe janela modal para seleção de máquina por ID. Valida que o ID
        é um número inteiro antes de retornar. Retorna None se cancelado
        ou se ID inválido após tentativas de correção.
        """
        layout = [
            [sg.Text('ID da máquina:'), sg.Input(key='id')],
            [sg.Button('Selecionar', bind_return_key=True),
             sg.Button('Cancelar')]
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
        """
        Exibe lista formatada de todas as máquinas cadastradas em janela modal
        com área de texto scrollável. Formata cada máquina com ID e nome.
        Exibe mensagem apropriada se lista estiver vazia. Janela permanece
        aberta até usuário fechar explicitamente.
        """
        sg.theme('DarkBlue3')
        texto = "--- LISTA DE MÁQUINAS ---\n\n"
        if not maquinas:
            texto += "Nenhuma máquina cadastrada."
        else:
            for maquina in maquinas:
                texto += f"ID: {maquina['id']} - {maquina['nome']}\n"

        layout = [
            [sg.Multiline(texto, size=(60, 20), disabled=True,
                          background_color='#4A5A6B', text_color='#E0E8F0', key='-TEXTO-')],
            [sg.Button('Fechar', button_color=(
                '#E0E8F0', '#6B7A8B'), size=(10, 1))]
        ]

        window = sg.Window('Lista de Máquinas', layout, modal=True,
                           background_color='#4A5A6B', size=(550, 550))

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
