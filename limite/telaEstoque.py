"""
    Gerencia a interface com o usuário para todas as operações de Estoque.

    Esta classe atua como a camada de apresentação (View) para o módulo de
    controle de estoque. Sua responsabilidade exclusiva é a interação com o
    usuário através do console, desacoplando a lógica de negócio do
    `ControladorEstoque` da entrada e saída de dados.
"""
import FreeSimpleGUI as sg

class TelaEstoque:

    def __init__(self):
        self.__window = None

    def init_opcoes(self):
        sg.ChangeLookAndFeel('BluePurple') 
        
        opcoes_layout = [
            [sg.Radio('Listar Inventário', "RD1", key='1', font='Any 12')],
            [sg.Radio('Adicionar Novo Produto ao Estoque', "RD1", key='2', font='Any 12')],
            [sg.Radio('Repor Estoque de um Produto', "RD1", key='3', font='Any 12')],
            [sg.Radio('Dar Baixa Manual de um Produto', "RD1", key='4', font='Any 12')],
            [sg.Radio('Retornar', "RD1", key='0', default=True, font='Any 12')]
        ]

        layout = [
            [sg.Column([[sg.Text('-------- Estoque ---------', font=("Helvica", 25), pad=((0,0),(20,10)))]], justification='center')],
            [sg.Column([[sg.Text('Escolha sua opção', font=("Helvica", 15), pad=((0,0),(0,20)))]], justification='center')],
            [sg.Column([[sg.Frame('Opções de Estoque', opcoes_layout, font='Any 14', title_color='black')]], justification='center')],
            [sg.Column([[
                sg.Button('Confirmar', font='Any 12', pad=((10,10),(25,15))), 
                sg.Cancel('Cancelar', font='Any 12', pad=((10,10),(25,15)))
            ]], justification='center')]
        ]
        
        self.__window = sg.Window('Gerenciador de Estoque', layout, element_justification='center', size=(550, 450))

    def tela_opcoes(self) -> int:
        self.init_opcoes() 
        button, values = self.open()

        if button in (None, 'Cancelar') or values['0']:
            self.close()
            return 0 

        if button == 'Confirmar':
            for i in range(1, 5):
                key = str(i)
                if values.get(key) == True:
                    self.close()
                    return i
        
        self.close()
        return None 
    
    def pega_dados_produto_estoque(self) -> dict:
        print("\n---- Dados do Produto no Estoque ----")
        try:
            id_produto = int(input("ID do Produto: "))
            quantidade = int(input("Quantidade: "))
            if quantidade < 0:
                self.mostra_mensagem("Quantidade não pode ser negativa.")
                return None
            return {"id_produto": id_produto, "quantidade": quantidade}
        except ValueError:
            self.mostra_mensagem("Entrada inválida! IDs e quantidade devem ser números.")
            return None

    def mostra_mensagem(self, msg: str) -> None:
        print(msg)