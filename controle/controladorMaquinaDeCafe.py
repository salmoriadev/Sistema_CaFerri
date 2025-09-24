class ControladorMaquinaDeCafe:
    def __init__(self, controlador_sistema):
        self.__maquinas_de_cafe = []
        self.__controlador_sistema = controlador_sistema
        self.__tela_maquina_de_cafe = TelaMaquinaDeCafe()
    
    def abre_tela(self):
        lista_opcoes = {1: self.incluir_maquina_de_cafe, 2: self.alterar_maquina_de_cafe, 3: self.lista_maquina_de_cafe, 4: self.excluir_maquina_de_cafe, 0: self.retornar}

        continua = True
        while continua:
            lista_opcoes[self.__tela_maquina_de_cafe.tela_opcoes()]()