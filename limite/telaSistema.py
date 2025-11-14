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
        self.__window = None
        self.init_components()

    def init_components(self):

        sg.ChangeLookAndFeel('LightBrown1') 
        
        layout_titulo = [
            [sg.Text('Caferri', font=("Helvica", 28), pad=((0,0),(20,10)))] 
        ]
        
        layout_subtitulo = [
            [sg.Text('Escolha sua opção', font=("Helvica", 16), pad=((0,0),(0,15)))]
        ]

        layout_opcoes = [
            [sg.Radio('Fornecedores de cafés', "RD1", key='1', font='Any 12')],
            [sg.Radio('Fornecedores de máquinas de cafés', "RD1", key='2', font='Any 12')],
            [sg.Radio('Clientes', "RD1", key='3', font='Any 12')],
            [sg.Radio('Cafés', "RD1", key='4', font='Any 12')],
            [sg.Radio('Máquinas de cafés', "RD1", key='5', font='Any 12')],
            [sg.Radio('Estoque', "RD1", key='6', font='Any 12')],
            [sg.Radio('Vendas', "RD1", key='7', font='Any 12')],
            [sg.Radio('Gerar Relatório', "RD1", key='8', font='Any 12')],
            [sg.Radio('Finalizar sistema', "RD1", key='0', default=True, font='Any 12')]
        ]
        
        layout_frame = [
            [sg.Frame('Módulos do Sistema', layout_opcoes, font='Any 14')]
        ]

        layout_botoes = [
            [
                sg.Button('Confirmar', font='Any 12', pad=((10,10),(25,15))), 
                sg.Cancel('Cancelar', font='Any 12', pad=((10,10),(25,15)))
            ]
        ]

        layout = [
            [sg.Column(layout_titulo, justification='center', element_justification='center')],
            [sg.Column(layout_subtitulo, justification='center', element_justification='center')],
            [sg.Column(layout_frame, justification='center')],
            [sg.Column(layout_botoes, justification='center')]
        ]
        
        self.__window = sg.Window('Sistema Caferri', layout, element_justification='center', size=(550, 550))
    
    def tela_opcoes(self) -> int:
        self.init_components()
        button, values = self.open()

        if button in (None, 'Cancelar'):
            self.close()
            return 0  

        if values['0']:
            self.close()
            return 0  

        if button == 'Confirmar':
            for i in range(1, 9): 
                key = str(i)
                if values.get(key) == True: 
                    self.close()
                    return i  
        
        self.close()
        return None 

    def mostra_mensagem(self, msg: str) -> None:
        sg.popup("", msg)

    def close(self):
        if self.__window:
            self.__window.Close()
            self.__window = None 

    def open(self):
        button, values = self.__window.Read()
        return button, values