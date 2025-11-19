"""
Gerencia a interface gráfica para todas as operações relacionadas aos Fornecedores de Café.

Esta classe atua como a camada de apresentação (View) no padrão MVC para o
módulo de gerenciamento de fornecedores de café. Utiliza FreeSimpleGUI para
criar interfaces gráficas modais, isolando a lógica de visualização do controlador.

Responsabilidades:
- Exibir menu principal com opções de CRUD para fornecedores de café
- Coletar dados do usuário através de formulários validados
- Exibir listas e detalhes de fornecedores formatados
- Gerenciar ciclo de vida das janelas (abrir/fechar)
- Validar entradas do usuário (CNPJ, campos obrigatórios) antes de retornar dados
"""

from typing import Dict, List, Optional

import FreeSimpleGUI as sg


class TelaEmpresaCafe:
    def __init__(self):
        """
        Inicializa a tela de fornecedores de café, criando referência para a
        janela principal que será configurada no método init_opcoes.
        """
        self.__window = None

    def init_opcoes(self):
        """
        Configura e cria a janela principal do menu de fornecedores de café.
        Define tema, layout com título, subtítulo e botões de opções
        (Adicionar, Alterar, Listar, Excluir, Retornar). A janela é armazenada
        em self.__window.
        """
        sg.theme('DarkBrown3')

        botoes = [
            [sg.Button('Adicionar Fornecedor', key='1', font='Any 14',
                       expand_x=True, button_color=('#F0E6D2', '#8B5A3C'))],
            [sg.Button('Alterar Fornecedor', key='2', font='Any 14',
                       expand_x=True, button_color=('#F0E6D2', '#8B5A3C'))],
            [sg.Button('Listar Fornecedores', key='3', font='Any 14',
                       expand_x=True, button_color=('#F0E6D2', '#8B5A3C'))],
            [sg.Button('Excluir Fornecedor', key='4', font='Any 14',
                       expand_x=True, button_color=('#F0E6D2', '#8B5A3C'))],
            [sg.Button('Retornar', key='0', font='Any 14',
                       expand_x=True, button_color=('#F0E6D2', '#8B5A3C'))]
        ]

        layout = [
            [sg.Column([[sg.Text('Fornecedores de Café', font=("Helvica", 28), pad=(
                (0, 0), (20, 10)), text_color='#F0E6D2')]], justification='center', background_color='#6B4423')],
            [sg.Column([[sg.Text('Escolha uma opção', font=("Helvica", 18), pad=(
                (0, 0), (0, 20)), text_color='#E8D5B7')]], justification='center', background_color='#6B4423')],
            [sg.Column([[sg.Frame('Opções', botoes, font='Any 16', title_color='#F0E6D2',
                       background_color='#6B4423', border_width=2)]], justification='center', background_color='#6B4423')]
        ]

        self.__window = sg.Window('Fornecedores de Café', layout, element_justification='center', size=(
            580, 580), background_color='#6B4423')

    def tela_opcoes(self) -> int:
        """
        Exibe o menu principal de fornecedores de café e captura a escolha do usuário.
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

    def pega_dados_empresa_cafe(self, is_alteracao: bool = False) -> Optional[dict]:
        """
        Exibe formulário modal para coleta de dados de um fornecedor de café.
        Adapta campos conforme contexto: oculta CNPJ em alterações (imutável).
        Valida que todos os campos obrigatórios estão preenchidos antes de
        retornar. Mantém janela aberta em caso de erro para correção.
        Retorna dicionário com dados validados ou None se cancelado.
        """
        campos = [
            [sg.Text('Nome:'), sg.Input(key='nome')],
            [sg.Text('Endereço:'), sg.Input(key='endereco')],
            [sg.Text('Telefone:'), sg.Input(key='telefone')],
            [sg.Text('Tipo de Café:'), sg.Input(key='tipo_cafe')]
        ]

        if not is_alteracao:
            campos.insert(1, [sg.Text('CNPJ:'), sg.Input(key='cnpj')])

        layout = campos + [
            [sg.Button('Salvar', bind_return_key=True), sg.Button('Cancelar')]
        ]

        window = sg.Window('Dados do Fornecedor', layout, modal=True)
        dados = None

        while True:
            event, values = window.read()
            if event in (sg.WINDOW_CLOSED, 'Cancelar'):
                break
            if event == 'Salvar':
                obrigatorios = ['nome', 'endereco', 'telefone', 'tipo_cafe']
                if not is_alteracao:
                    obrigatorios.append('cnpj')

                if all(values.get(campo, '').strip() for campo in obrigatorios):
                    dados = {
                        "nome": values['nome'].strip(),
                        "endereco": values['endereco'].strip(),
                        "telefone": values['telefone'].strip(),
                        "tipo_cafe": values['tipo_cafe'].strip()
                    }
                    if not is_alteracao:
                        dados["cnpj"] = values['cnpj'].strip()
                    break
                self.mostra_mensagem("Preencha todos os campos obrigatórios.")

        window.close()
        return dados

    def mostra_empresa_cafe(self, dados_empresa: dict) -> None:
        """
        Exibe detalhes de um fornecedor de café específico em popup formatado.
        Recebe dicionário com dados do fornecedor e formata para exibição legível.
        """
        texto = (
            f"NOME: {dados_empresa['nome']}\n"
            f"CNPJ: {dados_empresa.get('cnpj', '-')}\n"
            f"TIPO DE CAFÉ: {dados_empresa['tipo_cafe']}"
        )
        sg.popup('Fornecedor', texto)

    def seleciona_empresa_cafe(self) -> str:
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
        Exibe lista formatada de todos os fornecedores de café cadastrados em
        janela modal com área de texto scrollável. Formata cada fornecedor com
        nome, CNPJ e tipo de café. Exibe mensagem apropriada se lista estiver
        vazia. Janela permanece aberta até usuário fechar explicitamente.
        """
        sg.theme('DarkBrown3')
        texto = "--- LISTA DE FORNECEDORES DE CAFÉ ---\n\n"
        if not fornecedores:
            texto += "Nenhum fornecedor cadastrado."
        else:
            for fornecedor in fornecedores:
                texto += f"NOME: {fornecedor['nome']}\n"
                texto += f"CNPJ: {fornecedor['cnpj']}\n"
                texto += f"TIPO DE CAFÉ: {fornecedor['tipo_cafe']}\n\n"

        layout = [
            [sg.Multiline(texto, size=(60, 20), disabled=True,
                          background_color='#6B4423', text_color='#F0E6D2', key='-TEXTO-')],
            [sg.Button('Fechar', button_color=(
                '#F0E6D2', '#8B5A3C'), size=(10, 1))]
        ]

        window = sg.Window('Fornecedores de Café', layout,
                           modal=True, background_color='#6B4423', size=(550, 550))

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
