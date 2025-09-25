import hashlib
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
        if not self.__clientes:
            self.__tela_cliente.mostra_mensagem("Nenhum cliente cadastrado!")
            return
        self.lista_clientes()  
        id = self.__tela_cliente.seleciona_cliente()
        cliente = self.pega_cliente_por_id(id)
        senha = hashlib.sha256(self.__tela_cliente.pedir_senha().encode('utf-8')).hexdigest()
        if senha != cliente.senha:
            self.__tela_cliente.mostra_mensagem("Senha incorreta!")
            return
        if cliente is not None:
            novos_dados = self.__tela_cliente.pega_dados_cliente()
            cliente.nome = novos_dados["nome"]
            cliente.email = novos_dados["email"]
            cliente.senha = hashlib.sha256(novos_dados["senha"].encode('utf-8')).hexdigest()
            cliente.saldo = novos_dados["saldo"]
            cliente.perfil_do_consumidor = novos_dados["perfil"]
            self.__tela_cliente.mostra_mensagem("Cliente alterado com sucesso!")
            self.lista_clientes()
        else:
            self.__tela_cliente.mostra_mensagem("Cliente não encontrado!")

    def lista_clientes(self):
        if not self.__clientes:
            self.__tela_cliente.mostra_mensagem("Nenhum cliente cadastrado!")
        else:
            for cliente in self.__clientes:
                dados_cliente = {
                    "id": cliente.id,
                    "nome": cliente.nome,
                    "email": cliente.email,
                    "saldo": cliente.saldo,
                    "perfil": cliente.perfil_do_consumidor.perfil
                }
                self.__tela_cliente.mostra_cliente(dados_cliente)

    def excluir_cliente(self):
        if not self.__clientes:
            self.__tela_cliente.mostra_mensagem("Nenhum cliente cadastrado!")
            return
        
        self.lista_clientes()
        id = self.__tela_cliente.seleciona_cliente()
        cliente = self.pega_cliente_por_id(id)
        senha = hashlib.sha256(self.__tela_cliente.pedir_senha().encode('utf-8')).hexdigest()
        if senha != cliente.senha:
            self.__tela_cliente.mostra_mensagem("Senha incorreta!")
            return
        if cliente is not None:
            self.__clientes.remove(cliente)
            self.__tela_cliente.mostra_mensagem("Cliente excluído com sucesso!")
            self.lista_clientes()
        else:
            self.__tela_cliente.mostra_mensagem("Cliente não encontrado!")
    
    def retornar(self):
        self.__controlador_sistema.abre_tela()

    def abre_tela(self):
        lista_opcoes = {
            1: self.incluir_cliente,
            2: self.alterar_cliente,
            3: self.lista_clientes,
            4: self.excluir_cliente,
            0: self.retornar
        }
        while True:
            opcao = self.__tela_cliente.tela_opcoes()
            if opcao in lista_opcoes:
                funcao_escolhida = lista_opcoes[opcao]
                funcao_escolhida()
                if opcao == 0:
                    break
            else:
                self.__tela_cliente.mostra_mensagem("Opção inválida! Tente novamente.")