from limite.telaCliente import TelaCliente
class ControladorCliente:
    def __init__(self, controlador_sistema):
        self.__clientes = []
        self.__controlador_sistema = controlador_sistema
        self.__tela_cliente = TelaCliente()