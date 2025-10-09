import hashlib
from limite.telaCliente import TelaCliente
from entidade.cliente import Cliente
from Excecoes.clienteNaoEncontradoException import ClienteNaoEncontradoException
from Excecoes.perfilRecomendadoNaoExisteException import PerfilRecomendadoNaoExisteException

class ControladorCliente:
    def __init__(self, controlador_sistema) -> None:
        self.__clientes = []
        self.__controlador_sistema = controlador_sistema
        self.__tela_cliente = TelaCliente()

    def tem_clientes(self) -> bool:
        return len(self.__clientes) > 0

    def pega_cliente_por_id(self, id: int) -> Cliente:
        if not isinstance(id, int):
            raise TypeError("O ID do cliente deve ser um número inteiro.")
        for cliente in self.__clientes:
            if cliente.id == id:
                return cliente
        raise ClienteNaoEncontradoException

    def incluir_cliente(self) -> None:
        dados_cliente = self.__tela_cliente.pega_dados_cliente(is_alteracao=False)

        for cliente in self.__clientes:
            if cliente.id == dados_cliente["id"]:
                self.__tela_cliente.mostra_mensagem("ERRO: Já existe um cliente com este ID!")
                return

        novo_cliente = Cliente(
            dados_cliente["id"], dados_cliente["nome"], dados_cliente["email"],
            hashlib.sha256(dados_cliente["senha"].encode('utf-8')).hexdigest(),
            dados_cliente["saldo"], dados_cliente["perfil"]
        )
        self.__clientes.append(novo_cliente)
        self.__tela_cliente.mostra_mensagem("Cliente cadastrado com sucesso!")

    def alterar_cliente(self) -> None:
        if not self.__clientes:
            self.__tela_cliente.mostra_mensagem("Nenhum cliente cadastrado para alterar!")
            return

        self.lista_clientes()
        id_cliente = self.__tela_cliente.seleciona_cliente()
        cliente = self.pega_cliente_por_id(id_cliente)

        senha = hashlib.sha256(self.__tela_cliente.pedir_senha().encode('utf-8')).hexdigest()
        if senha != cliente.senha_cifrada:
            self.__tela_cliente.mostra_mensagem("Senha incorreta! Alteração cancelada.")
            return

        novos_dados = self.__tela_cliente.pega_dados_cliente(is_alteracao=True)
        cliente.nome = novos_dados["nome"]
        cliente.email = novos_dados["email"]
        if "senha" in novos_dados:
            cliente.senha_cifrada = hashlib.sha256(novos_dados["senha"].encode('utf-8')).hexdigest()
        cliente.saldo = novos_dados["saldo"]
        cliente.perfil_do_consumidor = novos_dados["perfil"]
        
        self.__tela_cliente.mostra_mensagem("Cliente alterado com sucesso!")
        self.lista_clientes()

    def lista_clientes(self) -> None:
        if not self.__clientes:
            self.__tela_cliente.mostra_mensagem("Nenhum cliente cadastrado!")
            return

        self.__tela_cliente.mostra_mensagem("--- LISTA DE CLIENTES ---")
        for cliente in self.__clientes:
            dados_cliente = {
                "id": cliente.id, "nome": cliente.nome, "email": cliente.email,
                "saldo": cliente.saldo, "perfil": cliente.perfil_do_consumidor.perfil
            }
            self.__tela_cliente.mostra_cliente(dados_cliente)

    def excluir_cliente(self) -> None:
        if not self.__clientes:
            self.__tela_cliente.mostra_mensagem("Nenhum cliente cadastrado para excluir!")
            return
            
        self.lista_clientes()
        id_cliente = self.__tela_cliente.seleciona_cliente()
        cliente = self.pega_cliente_por_id(id_cliente)

        senha = hashlib.sha256(self.__tela_cliente.pedir_senha().encode('utf-8')).hexdigest()
        if senha != cliente.senha_cifrada:
            self.__tela_cliente.mostra_mensagem("Senha incorreta! Exclusão cancelada.")
            return
            
        self.__clientes.remove(cliente)
        self.__tela_cliente.mostra_mensagem("Cliente excluído com sucesso!")
        self.lista_clientes()

    def ver_recomendacoes_de_cafe(self) -> None:
        if not self.__clientes:
            self.__tela_cliente.mostra_mensagem("Nenhum cliente cadastrado para ver recomendações!")
            return
            
        self.lista_clientes()
        id_cliente = self.__tela_cliente.seleciona_cliente()
        
        try:
            cliente = self.pega_cliente_por_id(id_cliente)
            perfil_do_cliente = cliente.perfil_do_consumidor.perfil
            cafes_recomendados = self.__controlador_sistema.controlador_cafe.buscar_cafes_por_perfil(perfil_do_cliente)
            self.__tela_cliente.mostra_mensagem(f"\n--- Recomendações para {cliente.nome} (Perfil: {perfil_do_cliente}) ---")
            for cafe in cafes_recomendados:
                self.__tela_cliente.mostra_mensagem(f"  - ID: {cafe.id}, Nome: {cafe.nome}, Preço: R$ {cafe.preco_venda:.2f}")
            if not cafes_recomendados:
                self.__tela_cliente.mostra_mensagem("Nenhum café encontrado para o perfil do cliente.")
            self.__tela_cliente.mostra_mensagem("----------------------------------------------------")

        except ClienteNaoEncontradoException as e:
            self.__tela_cliente.mostra_mensagem(f"ERRO: {e}")

    def retornar(self) -> None:
        self.__controlador_sistema.abre_tela()

    def abre_tela(self) -> None:
        lista_opcoes = {
            1: self.incluir_cliente, 2: self.alterar_cliente,
            3: self.lista_clientes, 4: self.excluir_cliente,
            5: self.ver_recomendacoes_de_cafe,
            0: self.retornar
        }
        while True:
            try:
                opcao = self.__tela_cliente.tela_opcoes()
                if opcao == 0:
                    self.retornar()
                    break
                
                funcao_escolhida = lista_opcoes.get(opcao)
                if funcao_escolhida:
                    funcao_escolhida()
                else:
                    self.__tela_cliente.mostra_mensagem("Opção inválida! Por favor, digite um número do menu.")
            
            except (ClienteNaoEncontradoException, PerfilRecomendadoNaoExisteException, TypeError) as e:
                self.__tela_cliente.mostra_mensagem(f"Ocorreu um erro: {e}")
