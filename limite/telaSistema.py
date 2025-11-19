"""
    Gerencia a interface principal do sistema, atuando como o ponto de
    entrada para o usuário.

    Esta classe é a camada de apresentação (View) do `ControladorSistema`
    e sua responsabilidade primária é exibir o menu principal, que serve
    como um portal de navegação para todas as outras funcionalidades do
    sistema, como o gerenciamento de clientes, produtos, estoque e vendas.

    Ela é responsável por:
    - Apresentar as opções de alto nível ao usuário.
    - Capturar a opção selecionada, incluindo um tratamento de erro para
      garantir que a entrada seja um número inteiro válido.
    - Fornecer um método padronizado (`mostra_mensagem`) para que o
      controlador principal possa exibir mensagens de feedback, como
      avisos ou erros, de forma consistente.
    """

import FreeSimpleGUI as sg


class TelaSistema:

    def __init__(self):
        """
        Inicializa a tela principal do sistema, criando referência para a janela
        e configurando os componentes iniciais.
        """
        self.__window = None
        self.init_components()

    def init_components(self):
        """
        Configura e cria a janela principal do sistema. Define tema, layout com
        título, subtítulo e botões de opções para todos os módulos disponíveis.
        A janela é armazenada em self.__window.
        """

        sg.theme('DarkBrown4')

        layout_titulo = [
            [sg.Text('Caferri', font=("Helvica", 28), pad=(
                (0, 0), (20, 10)), text_color='#E8D5B7')]
        ]

        layout_subtitulo = [
            [sg.Text('Escolha sua opção', font=("Helvica", 16),
                     pad=((0, 0), (0, 15)), text_color='#D4C4A8')]
        ]

        botoes_opcoes = [
            [sg.Button('Fornecedores de cafés', key='1', font='Any 12', pad=(
                5, 5), expand_x=True, button_color=('#E8D5B7', '#5C3D2E'))],
            [sg.Button('Fornecedores de máquinas de cafés', key='2', font='Any 12', pad=(
                5, 5), expand_x=True, button_color=('#E8D5B7', '#5C3D2E'))],
            [sg.Button('Clientes', key='3', font='Any 12', pad=(
                5, 5), expand_x=True, button_color=('#E8D5B7', '#5C3D2E'))],
            [sg.Button('Cafés', key='4', font='Any 12', pad=(5, 5),
                       expand_x=True, button_color=('#E8D5B7', '#5C3D2E'))],
            [sg.Button('Máquinas de cafés', key='5', font='Any 12', pad=(
                5, 5), expand_x=True, button_color=('#E8D5B7', '#5C3D2E'))],
            [sg.Button('Estoque', key='6', font='Any 12', pad=(5, 5),
                       expand_x=True, button_color=('#E8D5B7', '#5C3D2E'))],
            [sg.Button('Vendas', key='7', font='Any 12', pad=(5, 5),
                       expand_x=True, button_color=('#E8D5B7', '#5C3D2E'))],
            [sg.Button('Gerar Relatório', key='8', font='Any 12', pad=(
                5, 5), expand_x=True, button_color=('#E8D5B7', '#5C3D2E'))],
            [sg.Button('Finalizar sistema', key='0', font='Any 12', pad=(
                5, 5), expand_x=True, button_color=('#E8D5B7', '#5C3D2E'))]
        ]

        layout_frame = [
            [sg.Frame('Módulos do Sistema', botoes_opcoes, font='Any 14',
                      title_color='#E8D5B7', background_color='#3D2817', border_width=2)]
        ]

        layout = [
            [sg.Column(layout_titulo, justification='center',
                       element_justification='center', background_color='#3D2817')],
            [sg.Column(layout_subtitulo, justification='center',
                       element_justification='center', background_color='#3D2817')],
            [sg.Column(layout_frame, justification='center',
                       background_color='#3D2817')]
        ]

        self.__window = sg.Window('Sistema Caferri', layout, element_justification='center', size=(
            580, 580), background_color='#3D2817')

    def tela_opcoes(self) -> int:
        """
        Exibe o menu principal do sistema e captura a escolha do usuário.
        Retorna o código numérico da opção selecionada (1-8) ou 0 para finalizar.
        Retorna None se a janela for fechada sem seleção válida.
        """
        self.init_components()
        button, _ = self.open()

        if button in (None, '0', 'Finalizar sistema'):
            self.close()
            return 0

        opcoes_validas = {'1', '2', '3', '4', '5', '6', '7', '8'}
        if button in opcoes_validas:
            self.close()
            return int(button)

        self.close()
        return None

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
