from limite.telaCliente import TelaCliente
from entidade.cliente import Cliente

class ControladorCliente:
    def __init__(self, controlador_sistema):
        self.__clientes = []
        self.__controlador_sistema = controlador_sistema
        self.__tela_cliente = TelaCliente()

    def pega_cliente_por_id(self, id: int):
        for cliente in self.__clientes:
            if cliente.id == id:
                return cliente
        return None
    
    def incluir_cliente(self):
        dados_cliente = self.__tela_cliente.pega_dados_cliente()
        cliente_existente = self.pega_cliente_por_id(dados_cliente["id"])
        if cliente_existente is None:
            novo_cliente = Cliente(dados_cliente["id"], dados_cliente["nome"], dados_cliente["email"], dados_cliente["senha"], dados_cliente["saldo"], dados_cliente["perfil"])
            self.__clientes.append(novo_cliente)
        else:
            self.__tela_cliente.mostra_mensagem("Cliente já existente!")

    def alterar_cliente(self):
        id = self.__tela_cliente.seleciona_cliente()
        if id is None:
            return
        cliente = self.pega_cliente_por_id(id)
        if cliente:
            novos_dados = self.__tela_cliente.pega_dados_cliente()
            cliente.nome = novos_dados["nome"]
            cliente.email = novos_dados["email"]
            cliente.senha = novos_dados["senha"]
            cliente.saldo = novos_dados["saldo"]
            cliente.perfil = novos_dados["perfil"]
        else:
            self.__tela_cliente.mostra_mensagem("Cliente não encontrado!")