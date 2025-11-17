"""
    Gerencia a interface gráfica para todas as operações relacionadas a Clientes.

    Esta classe atua como a camada de Visão (View) no padrão MVC, sendo responsável
    exclusivamente pela interação com o usuário através de janelas gráficas
    utilizando a biblioteca FreeSimpleGUI. Ela isola a lógica de apresentação,
    garantindo que o Controlador receba apenas dados validados e formatados.

    Funcionalidades e Responsabilidades:

    1. Menu Principal de Clientes (tela_opcoes):
       - Exibe as operações disponíveis: Incluir, Alterar, Listar, Excluir e
         Ver Recomendações.
       - Retorna o código da operação escolhida para o controlador.

    2. Formulário de Cadastro/Alteração (pega_dados_cliente):
       - Renderiza um formulário dinâmico que se adapta ao contexto:
         - Na INCLUSÃO: Exige ID e Senha.
         - Na ALTERAÇÃO: Oculta o campo ID (imutável) e torna o campo Senha
           opcional (para caso o usuário deseje trocá-la).
       - Utiliza ComboBox para seleção de perfis, evitando erros de digitação.
       - Realiza validações de entrada (campos vazios, tipos numéricos, formato
         de e-mail) antes de retornar os dados, mantendo a janela aberta em
         caso de erro para correção imediata.

    3. Seleção e Segurança:
       - Fornece janelas modais específicas para selecionar clientes pelo ID
         e para solicitar confirmação de senha (input mascarado) antes de
         operações críticas.

    4. Exibição de Dados:
       - Utiliza uma janela de log (sg.Print) para listar clientes, adequada
         para exibir múltiplos registros em sequência sem interromper o fluxo.
       - Utiliza pop-ups padronizados para mensagens de feedback.
"""

from typing import Dict, List, Optional
import FreeSimpleGUI as sg


class TelaCliente:

    def __init__(self):
        self.__window = None

    def init_opcoes(self):
        sg.theme('DarkGreen7')

        botoes_opcoes = [
            [sg.Button('Incluir Cliente', key='1', font='Any 12', pad=(
                5, 5), expand_x=True, button_color=('#E8F5D2', '#6B7D5A'))],
            [sg.Button('Alterar Cliente', key='2', font='Any 12', pad=(
                5, 5), expand_x=True, button_color=('#E8F5D2', '#6B7D5A'))],
            [sg.Button('Listar Clientes', key='3', font='Any 12', pad=(
                5, 5), expand_x=True, button_color=('#E8F5D2', '#6B7D5A'))],
            [sg.Button('Excluir Cliente', key='4', font='Any 12', pad=(
                5, 5), expand_x=True, button_color=('#E8F5D2', '#6B7D5A'))],
            [sg.Button('Ver Recomendações de Café', key='5', font='Any 12', pad=(
                5, 5), expand_x=True, button_color=('#E8F5D2', '#6B7D5A'))],
            [sg.Button('Retornar', key='0', font='Any 12', pad=(
                5, 5), expand_x=True, button_color=('#E8F5D2', '#6B7D5A'))]
        ]

        layout = [
            [sg.Column([[sg.Text('-------- Clientes ---------', font=("Helvica", 25), pad=((0, 0),
                       (20, 10)), text_color='#E8F5D2')]], justification='center', background_color='#4A5D3A')],
            [sg.Column([[sg.Text('Escolha sua opção', font=("Helvica", 15), pad=(
                (0, 0), (0, 20)), text_color='#D4E5C4')]], justification='center', background_color='#4A5D3A')],
            [sg.Column([[sg.Frame('Ações', botoes_opcoes, font='Any 14', title_color='#E8F5D2',
                       background_color='#4A5D3A', border_width=2)]], justification='center', background_color='#4A5D3A')]
        ]

        self.__window = sg.Window('Gerenciamento de Clientes', layout, element_justification='center', size=(
            580, 580), background_color='#4A5D3A')

    def tela_opcoes(self) -> int:
        self.init_opcoes()
        button, _ = self.open()

        if button in (None, '0', 'Retornar'):
            self.close()
            return 0

        opcoes_validas = {'1', '2', '3', '4', '5'}
        if button in opcoes_validas:
            self.close()
            return int(button)

        self.close()
        return 0

    def pega_dados_cliente(self, perfil_mapa: dict, is_alteracao: bool = False) -> Optional[Dict]:
        sg.theme('DarkGreen7')
        perfis_disponiveis = perfil_mapa["perfis_disponiveis"]

        layout_formulario = []

        if not is_alteracao:
            layout_formulario.append(
                [sg.Text('ID:', size=(15, 1)), sg.Input(key='id')])

        layout_formulario.append(
            [sg.Text('Nome:', size=(15, 1)), sg.Input(key='nome')])
        layout_formulario.append(
            [sg.Text('Email:', size=(15, 1)), sg.Input(key='email')])

        if is_alteracao:
            layout_formulario.append([sg.Text('Nova Senha:', size=(
                15, 1)), sg.Input(key='senha', password_char='*')])
            layout_formulario.append([sg.Text(
                '(Deixe em branco para manter a atual)', font='Any 8', text_color='yellow')])
        else:
            layout_formulario.append(
                [sg.Text('Senha:', size=(15, 1)), sg.Input(key='senha', password_char='*')])

        layout_formulario.append(
            [sg.Text('Saldo:', size=(15, 1)), sg.Input(key='saldo')])

        layout_formulario.append([sg.Text('Perfil:', size=(15, 1)),
                                  sg.Combo(perfis_disponiveis, key='perfil', size=(30, 1), readonly=True)])

        layout_formulario.append(
            [sg.Button('Confirmar', bind_return_key=True), sg.Button('Cancelar')])

        titulo = "Alterar Cliente" if is_alteracao else "Incluir Cliente"

        self.__window = sg.Window(titulo, layout_formulario, modal=True)
        dados = None

        while True:
            event, values = self.open()
            if event in (sg.WINDOW_CLOSED, 'Cancelar'):
                break

            if event == 'Confirmar':
                try:
                    nome = values['nome'].strip()
                    if not nome:
                        raise ValueError("Nome inválido.")

                    email = values['email'].strip()
                    if not (email and '@' in email and '.' in email):
                        raise ValueError("Email inválido.")

                    senha = values['senha']
                    if not is_alteracao and not senha:
                        raise ValueError("Senha obrigatória na inclusão.")

                    saldo = float(values['saldo'])
                    if saldo < 0:
                        raise ValueError("Saldo não pode ser negativo.")

                    perfil = values['perfil']
                    if not perfil:
                        raise ValueError("Selecione um perfil.")

                    dados = {
                        "nome": nome, "email": email, "saldo": saldo, "perfil": perfil
                    }

                    if not is_alteracao:
                        id_cliente = int(values['id'])
                        if id_cliente < 0:
                            raise ValueError("ID não pode ser negativo.")
                        dados["id"] = id_cliente
                        dados["senha"] = senha
                    elif senha:
                        dados["senha"] = senha

                    break

                except ValueError as e:
                    sg.popup_error(f"Erro: {e}")

        self.close()
        return dados

    def mostra_cliente(self, dados_cliente: dict) -> None:
        linhas = [
            "--------------------------------",
            f"ID: {dados_cliente['id']}",
            f"NOME: {dados_cliente['nome']}",
            f"EMAIL: {dados_cliente['email']}",
            f"SALDO: R$ {dados_cliente['saldo']:.2f}",
            f"PERFIL: {dados_cliente['perfil']}",
            "--------------------------------"
        ]
        sg.Print("\n".join(linhas))

    def mostra_lista_clientes(self, clientes: List[Dict[str, str]]) -> None:
        sg.theme('DarkGreen7')
        texto = "--- LISTA DE CLIENTES ---\n\n"
        if not clientes:
            texto += "Nenhum cliente cadastrado."
        else:
            for cliente in clientes:
                texto += f"ID: {cliente['id']}\n"
                texto += f"NOME: {cliente['nome']}\n"
                texto += f"EMAIL: {cliente['email']}\n"
                texto += f"SALDO: R$ {cliente['saldo']:.2f}\n"
                texto += f"PERFIL: {cliente['perfil']}\n\n"

        layout = [
            [sg.Multiline(texto, size=(60, 20), disabled=True,
                          background_color='#4A5D3A', text_color='#E8F5D2', key='-TEXTO-')],
            [sg.Button('Fechar', button_color=(
                '#E8F5D2', '#6B7D5A'), size=(10, 1))]
        ]

        window = sg.Window('Lista de Clientes', layout, modal=True,
                           background_color='#4A5D3A', size=(550, 550))

        while True:
            event, _ = window.read()
            if event in (sg.WINDOW_CLOSED, 'Fechar'):
                break

        window.close()

    def mostra_recomendacoes(self, nome_cliente: str, perfil: str, cafes: List[Dict[str, str]]) -> None:
        sg.theme('DarkGreen7')
        texto = f"--- RECOMENDAÇÕES PARA {nome_cliente.upper()} ---\n"
        texto += f"Perfil: {perfil}\n\n"

        if not cafes:
            texto += "Nenhum café encontrado para o perfil do cliente."
        else:
            for cafe in cafes:
                texto += f"ID: {cafe['id']} - {cafe['nome']} | Preço: R$ {cafe['preco']:.2f}\n"

        layout = [
            [sg.Multiline(texto, size=(60, 20), disabled=True,
                          background_color='#4A5D3A', text_color='#E8F5D2', key='-TEXTO-')],
            [sg.Button('Fechar', button_color=(
                '#E8F5D2', '#6B7D5A'), size=(10, 1))]
        ]

        window = sg.Window('Recomendações de Café', layout,
                           modal=True, background_color='#4A5D3A', size=(550, 550))

        while True:
            event, _ = window.read()
            if event in (sg.WINDOW_CLOSED, 'Fechar'):
                break

        window.close()

    def seleciona_cliente(self) -> Optional[int]:
        sg.theme('DarkGreen7')
        layout = [
            [sg.Text('Selecionar Cliente', font=("Helvica", 18))],
            [sg.Text('ID do Cliente:', size=(15, 1)),
             sg.Input(key='id_cliente')],
            [sg.Button('Confirmar', bind_return_key=True),
             sg.Button('Cancelar')]
        ]
        self.__window = sg.Window('Seleção', layout, modal=True)
        id_cliente = None

        while True:
            event, values = self.open()
            if event in (sg.WINDOW_CLOSED, 'Cancelar'):
                break
            if event == 'Confirmar':
                try:
                    id_cliente = int(values['id_cliente'])
                    break
                except ValueError:
                    sg.popup_error("O ID deve ser um número inteiro.")
        self.close()
        return id_cliente

    def pedir_senha(self) -> Optional[str]:
        senha = sg.popup_get_text(
            "Digite sua senha atual para confirmar:", password_char='*', title="Segurança")
        return senha

    def mostra_mensagem(self, msg: str) -> None:
        sg.popup("", msg, font='Any 12')

    def close(self):
        if self.__window:
            self.__window.Close()
            self.__window = None

    def open(self):
        button, values = self.__window.Read()
        return button, values
