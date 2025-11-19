"""
    Orquestra toda a lógica de negócio para o gerenciamento de Clientes.

    Atuando como a camada de Controle (Controller), esta classe é responsável
    por mediar as interações entre a interface do usuário (`TelaCliente`) e
    os objetos de dados (`Cliente`). Ela gerencia o ciclo de vida completo
    dos clientes, incluindo as operações de CRUD (Incluir, Alterar, Listar, Excluir).

    Além disso, implementa a lógica de segurança, como a cifragem de senhas
    usando `hashlib` no momento do cadastro e da alteração, e exige a
    confirmação da senha para operações críticas como a modificação e a
    exclusão de dados.

    A classe também colabora ativamente com outros controladores do sistema,
    como o `ControladorCafe`, para executar funcionalidades complexas,
    a exemplo da busca por cafés recomendados com base no perfil do cliente.
    Ela gerencia o fluxo de navegação do menu de clientes e trata exceções
    para garantir uma experiência de usuário robusta e segura.
    """

import hashlib
from entidade.perfil_consumidor import PerfilConsumidor
from limite.telaCliente import TelaCliente
from entidade.cliente import Cliente
from Excecoes.clienteNaoEncontradoException import ClienteNaoEncontradoException
from Excecoes.perfilRecomendadoNaoExisteException import PerfilRecomendadoNaoExisteException
from DAOs.cliente_dao import ClienteDAO


class ControladorCliente:
    def __init__(self, controlador_sistema) -> None:
        self.__controlador_sistema = controlador_sistema
        self.__tela_cliente = TelaCliente()
        self.__cliente_dao = ClienteDAO()

    @property
    def clientes(self) -> list:
        return list(self.__cliente_dao.get_all())

    def tem_clientes(self) -> bool:
        return len(self.clientes) > 0

    def pega_cliente_por_id(self, id: int) -> Cliente:
        """
        Recupera um cliente específico pelo ID. Valida que o ID é um inteiro
        e lança exceção apropriada se o cliente não for encontrado. Usado
        internamente e por outros controladores que precisam acessar clientes
        específicos (ex: ControladorVenda para associar cliente a venda).
        """
        if not isinstance(id, int):
            raise TypeError("O ID do cliente deve ser um número inteiro.")
        cliente = self.__cliente_dao.get(id)
        if cliente is None:
            raise ClienteNaoEncontradoException()
        return cliente

    def incluir_cliente(self) -> None:
        """
        Processa o cadastro de um novo cliente. Coleta dados do usuário através
        da tela, valida que não existe cliente com o mesmo ID, criptografa
        senha usando SHA-256 e persiste o novo cliente. Exibe mensagens de
        sucesso ou erro conforme o resultado da operação.
        """
        perfis_mapa = {}
        perfis_mapa["perfis_disponiveis"] = PerfilConsumidor(
            "Doce e Suave").possiveis_perfis
        dados_cliente = self.__tela_cliente.pega_dados_cliente(
            perfis_mapa, is_alteracao=False)

        if dados_cliente is None:
            return

        if self.__cliente_dao.get(dados_cliente["id"]):
            self.__tela_cliente.mostra_mensagem(
                "ERRO: Já existe um cliente com este ID!")
            return

        novo_cliente = Cliente(
            dados_cliente["id"], dados_cliente["nome"], dados_cliente["email"],
            hashlib.sha256(dados_cliente["senha"].encode('utf-8')).hexdigest(),
            dados_cliente["saldo"], dados_cliente["perfil"]
        )
        self.__cliente_dao.add(novo_cliente)
        self.__tela_cliente.mostra_mensagem("Cliente cadastrado com sucesso!")

    def alterar_cliente(self) -> None:
        """
        Processa a alteração de um cliente existente. Lista clientes disponíveis,
        permite seleção, solicita confirmação de senha atual para segurança,
        coleta novos dados e atualiza propriedades. Senha nova é opcional
        (mantém atual se não informada). Exibe lista atualizada após sucesso.
        """
        if not self.clientes:
            self.__tela_cliente.mostra_mensagem(
                "Nenhum cliente cadastrado para alterar!")
            return

        self.lista_clientes()
        id_cliente = self.__tela_cliente.seleciona_cliente()
        if id_cliente is None:
            return
        cliente = self.pega_cliente_por_id(id_cliente)

        senha_digitada = self.__tela_cliente.pedir_senha()

        if senha_digitada is None:
            return

        senha = hashlib.sha256(senha_digitada.encode('utf-8')).hexdigest()
        if senha != cliente.senha_cifrada:
            self.__tela_cliente.mostra_mensagem(
                "Senha incorreta! Alteração cancelada.")
            return

        perfis_mapa = {}
        perfis_mapa["perfis_disponiveis"] = PerfilConsumidor(
            "Doce e Suave").possiveis_perfis
        novos_dados = self.__tela_cliente.pega_dados_cliente(
            perfis_mapa, is_alteracao=True)
        if novos_dados is None:
            return

        cliente.nome = novos_dados["nome"]
        cliente.email = novos_dados["email"]
        if "senha" in novos_dados:
            cliente.senha_cifrada = hashlib.sha256(
                novos_dados["senha"].encode('utf-8')).hexdigest()
        cliente.saldo = novos_dados["saldo"]
        cliente.perfil_do_consumidor = novos_dados["perfil"]

        self.__cliente_dao.update(cliente)
        self.__tela_cliente.mostra_mensagem("Cliente alterado com sucesso!")
        self.lista_clientes()

    def lista_clientes(self) -> None:
        """
        Exibe lista formatada de todos os clientes cadastrados. Extrai informações
        relevantes (ID, nome, email, saldo, perfil) e delega a exibição para a
        tela. Usado tanto para visualização quanto como passo intermediário em
        operações de alteração e exclusão.
        """
        clientes = self.clientes
        if not clientes:
            self.__tela_cliente.mostra_mensagem("Nenhum cliente cadastrado!")
            return

        dados_clientes = []
        for cliente in clientes:
            dados_clientes.append({
                "id": cliente.id, "nome": cliente.nome, "email": cliente.email,
                "saldo": cliente.saldo, "perfil": cliente.perfil_do_consumidor.perfil
            })
        self.__tela_cliente.mostra_lista_clientes(dados_clientes)

    def excluir_cliente(self) -> None:
        """
        Processa a exclusão de um cliente. Lista clientes, permite seleção,
        solicita confirmação de senha para segurança, valida que não existem
        vendas em andamento com o cliente e remove do repositório. Exibe lista
        atualizada após exclusão bem-sucedida.
        """
        if not self.clientes:
            self.__tela_cliente.mostra_mensagem(
                "Nenhum cliente cadastrado para excluir!")
            return

        self.lista_clientes()
        id_cliente = self.__tela_cliente.seleciona_cliente()
        if id_cliente is None:
            return
        cliente = self.pega_cliente_por_id(id_cliente)

        senha_digitada = self.__tela_cliente.pedir_senha()
        if senha_digitada is None:
            return

        senha = hashlib.sha256(senha_digitada.encode('utf-8')).hexdigest()
        if senha != cliente.senha_cifrada:
            self.__tela_cliente.mostra_mensagem(
                "Senha incorreta! Exclusão cancelada.")
            return

        vendas_com_cliente = []
        for venda in self.__controlador_sistema.controlador_venda.vendas:
            if venda.cliente == cliente and venda.status_venda == "Em andamento":
                vendas_com_cliente.append(venda)

        if vendas_com_cliente:
            self.__tela_cliente.mostra_mensagem(
                f"ERRO: Não é possível excluir este cliente!")
            self.__tela_cliente.mostra_mensagem(
                f"Existem {len(vendas_com_cliente)} venda(s) em andamento com este cliente.")
            self.__tela_cliente.mostra_mensagem(
                "Finalize ou cancele as vendas primeiro.")
            return

        self.__cliente_dao.remove(cliente.id)
        self.__tela_cliente.mostra_mensagem("Cliente excluído com sucesso!")
        self.lista_clientes()

    def ver_recomendacoes_de_cafe(self) -> None:
        """
        Gera recomendações personalizadas de cafés para um cliente baseado
        no seu perfil de consumidor. Lista clientes, permite seleção, busca
        cafés que correspondem ao perfil do cliente e exibe lista formatada
        com informações relevantes (ID, nome, preço). Usa colaboração com
        ControladorCafe para realizar a busca por perfil.
        """
        if not self.clientes:
            self.__tela_cliente.mostra_mensagem(
                "Nenhum cliente cadastrado para ver recomendações!")
            return

        self.lista_clientes()
        id_cliente = self.__tela_cliente.seleciona_cliente()

        if id_cliente is None:
            return

        try:
            cliente = self.pega_cliente_por_id(id_cliente)
            perfil_do_cliente = cliente.perfil_do_consumidor.perfil
            cafes_recomendados = self.__controlador_sistema.controlador_cafe.buscar_cafes_por_perfil(
                perfil_do_cliente)

            dados_cafes = []
            for cafe in cafes_recomendados:
                dados_cafes.append({
                    "id": cafe.id,
                    "nome": cafe.nome,
                    "preco": cafe.preco_venda
                })

            self.__tela_cliente.mostra_recomendacoes(
                cliente.nome, perfil_do_cliente, dados_cafes)

        except ClienteNaoEncontradoException as e:
            self.__tela_cliente.mostra_mensagem(f"ERRO: {e}")

    def retornar(self) -> None:
        self.__controlador_sistema.abre_tela()

    def abre_tela(self) -> None:
        mapa_opcoes = {
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

                funcao_escolhida = mapa_opcoes.get(opcao)
                if funcao_escolhida:
                    funcao_escolhida()
                else:
                    self.__tela_cliente.mostra_mensagem(
                        "Opção inválida! Por favor, digite um número do menu.")

            except (ClienteNaoEncontradoException,
                    PerfilRecomendadoNaoExisteException, TypeError) as e:
                self.__tela_cliente.mostra_mensagem(f"Ocorreu um erro: {e}")
