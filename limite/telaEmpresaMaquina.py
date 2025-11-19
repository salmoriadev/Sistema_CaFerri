"""
Gerencia a interface gráfica para todas as operações relacionadas aos Fornecedores de Máquinas.

Esta classe atua como a camada de apresentação (View) no padrão MVC para o
módulo de gerenciamento de fornecedores de máquinas. Utiliza FreeSimpleGUI para
criar interfaces gráficas modais, isolando a lógica de visualização do controlador.

Responsabilidades:
- Exibir menu principal com opções de CRUD para fornecedores de máquinas
- Coletar dados do usuário através de formulários validados
- Exibir listas e detalhes de fornecedores formatados
- Gerenciar ciclo de vida das janelas (abrir/fechar)
- Validar entradas do usuário (CNPJ, campos obrigatórios) antes de retornar dados
"""

from typing import Dict, List, Optional

import FreeSimpleGUI as sg


class TelaEmpresaMaquina:
    def __init__(self):
        """
        Inicializa a tela de fornecedores de máquinas, criando referência para a
        janela principal que será configurada no método init_opcoes.
        """
        self.__window = None

    def init_opcoes(self):
        """
        Configura e cria a janela principal do menu de fornecedores de máquinas.
        Define tema, layout com título, subtítulo e botões de opções
        (Adicionar, Alterar, Listar, Excluir, Retornar). A janela é armazenada
        em self.__window.
        """
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
        """
        Exibe o menu principal de fornecedores de máquinas e captura a escolha do usuário.
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

    def pega_dados_empresa_maquina(self, is_alteracao: bool = False) -> Optional[dict]:
        """
        Exibe formulário modal para coleta de dados de um fornecedor de máquinas.
        Adapta campos conforme contexto: oculta CNPJ em alterações (imutável).
        Valida que todos os campos obrigatórios estão preenchidos antes de
        retornar. Mantém janela aberta em caso de erro para correção.
        Retorna dicionário com dados validados ou None se cancelado.
        """
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
        """
        Exibe detalhes de um fornecedor de máquinas específico em popup formatado.
        Recebe dicionário com dados do fornecedor e formata para exibição legível.
        """
        texto = (
            f"NOME: {dados_empresa['nome']}\n"
            f"CNPJ: {dados_empresa.get('cnpj', '-')}\n"
            f"PAÍS DE ORIGEM: {dados_empresa['pais_de_origem']}"
        )
        sg.popup('Fornecedor de Máquinas', texto)

    def seleciona_empresa_maquina(self) -> Optional[str]:
        """
        Exibe janela modal para seleção de fornecedor por CNPJ. Valida que o
        CNPJ não está vazio antes de retornar. Retorna None se cancelado ou
        se CNPJ inválido após tentativas de correção.
        """
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
        """
        Exibe lista formatada de todos os fornecedores de máquinas cadastrados em
        janela modal com área de texto scrollável. Formata cada fornecedor com
        nome, CNPJ e país de origem. Exibe mensagem apropriada se lista estiver
        vazia. Janela permanece aberta até usuário fechar explicitamente.
        """
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
