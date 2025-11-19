"""
    Orquestra a lógica de negócio para o gerenciamento de Máquinas de Café.

    Esta classe conecta a interface do usuário (`TelaMaquinaCafe`) 
    com os dados (`MaquinaDeCafe`). É responsável por todas as operações de
    CRUD (Criar, Ler, Alterar, Excluir) relacionadas às máquinas.

    Herda de `BuscaProdutoMixin` para reutilizar a funcionalidade de verificação
    de IDs de produtos duplicados, garantindo que cada café ou máquina tenha um
    identificador único em todo o sistema.
    """


from Excecoes.fornecedorNaoEncontradoException import FornecedorNaoEncontradoException
from controle.buscaProdutoMixin import BuscaProdutoMixin
from limite.telaMaquinaDeCafe import TelaMaquinaCafe
from entidade.maquina_de_cafe import MaquinaDeCafe
from Excecoes.maquinaNaoEncontradaException import MaquinaNaoEncontradaException
from DAOs.maquina_de_cafe_dao import MaquinaDeCafeDAO


class ControladorMaquinaDeCafe(BuscaProdutoMixin):
    def __init__(self, controlador_sistema) -> None:
        self._controlador_sistema = controlador_sistema
        self.__tela_maquina = TelaMaquinaCafe()
        self.__maquina_dao = MaquinaDeCafeDAO()

    @property
    def maquinas(self) -> list:
        return list(self.__maquina_dao.get_all())

    def pega_maquina_por_id(self, id: int) -> MaquinaDeCafe:
        """
        Recupera uma máquina específica pelo ID. Valida que o ID é um inteiro
        e lança exceção apropriada se a máquina não for encontrada. Usado
        internamente e por outros controladores que precisam acessar máquinas
        específicas.
        """
        if not isinstance(id, int):
            raise TypeError("O ID da máquina deve ser um número inteiro.")
        maquina = self.__maquina_dao.get(id)
        if maquina is None:
            raise MaquinaNaoEncontradaException()
        return maquina

    def incluir_maquina(self) -> None:
        """
        Processa o cadastro de uma nova máquina. Coleta dados do usuário através
        da tela, valida que não existe produto com o mesmo ID (usando mixin),
        verifica existência do fornecedor e persiste a nova máquina. Exibe
        mensagens de sucesso ou erro conforme o resultado da operação.
        """
        dados_maquina = self.__tela_maquina.pega_dados_maquina(
            is_alteracao=False)

        if self.id_produto_ja_existe(dados_maquina["id"]):
            self.__tela_maquina.mostra_mensagem(
                "ERRO: Já existe um produto (café ou máquina) com este ID!")
            return
        empresa_fornecedora = self._controlador_sistema.controlador_empresa_maquina.pega_fornecedor_por_cnpj(
            dados_maquina["empresa_fornecedora"])
        nova_maquina = MaquinaDeCafe(
            dados_maquina["nome"], dados_maquina["preco_compra"], dados_maquina["preco_venda"],
            dados_maquina["id"], dados_maquina["data_fabricacao"], empresa_fornecedora
        )
        self.__maquina_dao.add(nova_maquina)
        self.__tela_maquina.mostra_mensagem("Máquina cadastrada com sucesso!")

    def alterar_maquina(self) -> None:
        """
        Processa a alteração de uma máquina existente. Lista máquinas disponíveis,
        permite seleção, coleta novos dados do usuário e atualiza todas as
        propriedades da máquina. Valida fornecedor antes de atualizar e exibe
        lista atualizada após sucesso.
        """
        if not self.maquinas:
            self.__tela_maquina.mostra_mensagem(
                "Nenhuma máquina cadastrada para alterar!")
            return

        self.lista_maquina()
        id_maquina = self.__tela_maquina.seleciona_maquina()
        maquina = self.pega_maquina_por_id(id_maquina)

        novos_dados = self.__tela_maquina.pega_dados_maquina(is_alteracao=True)

        maquina.nome = novos_dados["nome"]
        maquina.preco_compra = novos_dados["preco_compra"]
        maquina.preco_venda = novos_dados["preco_venda"]
        maquina.data_fabricacao = novos_dados["data_fabricacao"]
        maquina.empresa_fornecedora = self._controlador_sistema.controlador_empresa_maquina.pega_fornecedor_por_cnpj(
            novos_dados["empresa_fornecedora"])
        self.__maquina_dao.update(maquina)

        self.__tela_maquina.mostra_mensagem("Máquina alterada com sucesso!")
        self.lista_maquina()

    def lista_maquina(self) -> None:
        """
        Exibe lista formatada de todas as máquinas cadastradas. Extrai informações
        relevantes (ID, nome, preço, fornecedor) e delega a exibição para a tela.
        Usado tanto para visualização quanto como passo intermediário em operações
        de alteração e exclusão.
        """
        if not self.maquinas:
            self.__tela_maquina.mostra_mensagem("Nenhuma máquina cadastrada!")
            return

        dados_maquinas = []
        for maquina in self.maquinas:
            dados_maquinas.append({
                "id": maquina.id,
                "nome": maquina.nome,
                "preco_venda": maquina.preco_venda,
                "empresa_fornecedora_nome": maquina.empresa_fornecedora.nome
            })
        self.__tela_maquina.mostra_lista_maquinas(dados_maquinas)

    def excluir_maquina(self) -> None:
        """
        Processa a exclusão de uma máquina. Lista máquinas disponíveis, permite
        seleção, remove a máquina do estoque se estiver cadastrada (mantendo
        integridade referencial) e remove do repositório. Exibe lista atualizada
        após exclusão bem-sucedida.
        """
        if not self.maquinas:
            self.__tela_maquina.mostra_mensagem(
                "Nenhuma máquina cadastrada para excluir!")
            return

        self.lista_maquina()
        id_maquina = self.__tela_maquina.seleciona_maquina()
        maquina = self.pega_maquina_por_id(id_maquina)

        estoque = self._controlador_sistema.controlador_estoque.estoque
        estoque.remover_produto_do_estoque(maquina)

        self.__maquina_dao.remove(maquina.id)
        self.__tela_maquina.mostra_mensagem("Máquina excluída com sucesso!")
        self.lista_maquina()

    def retornar(self) -> None:
        self._controlador_sistema.abre_tela()

    def abre_tela(self) -> None:
        mapa_opcoes = {
            1: self.incluir_maquina, 2: self.alterar_maquina,
            3: self.lista_maquina, 4: self.excluir_maquina,
            0: self.retornar
        }
        while True:
            try:
                opcao = self.__tela_maquina.tela_opcoes()
                if opcao == 0:
                    self.retornar()
                    break

                funcao_escolhida = mapa_opcoes.get(opcao)
                if funcao_escolhida:
                    funcao_escolhida()
                else:
                    self.__tela_maquina.mostra_mensagem(
                        "Opção inválida! Por favor, digite um número do menu.")

            except (MaquinaNaoEncontradaException,
                    TypeError, ValueError,
                    FornecedorNaoEncontradoException) as e:
                self.__tela_maquina.mostra_mensagem(f"Ocorreu um erro: {e}")
