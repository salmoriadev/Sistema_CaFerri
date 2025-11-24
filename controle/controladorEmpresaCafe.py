""" Orquestra a lógica de negócio para o gerenciamento de Fornecedores de Café.

    Esta classe desempenha o papel de Controller, estabelecendo a comunicação
    entre a interface do usuário (`TelaEmpresaCafe`) e os modelos de dados
    (`FornecedoraCafe`). É o componente central para todas as operações de
    CRUD (Criar, Ler, Alterar, Excluir) relacionadas aos fornecedores de café.
    
    Herda de `BuscaProdutoMixin` para reutilizar a funcionalidade de verificação
    de CNPJs de empresas duplicados, garantindo que cada empresa tenha um
    identificador único em todo o sistema.
    """


from controle.buscaProdutoMixin import BuscaProdutoMixin
from limite.telaEmpresaCafe import TelaEmpresaCafe
from entidade.fornecedora_cafe import FornecedoraCafe
from Excecoes.fornecedorNaoEncontradoException import FornecedorNaoEncontradoException
from DAOs.fornecedora_cafe_dao import FornecedoraCafeDAO


class ControladorEmpresaCafe(BuscaProdutoMixin):
    def __init__(self, controlador_sistema):
        self._controlador_sistema = controlador_sistema
        self.__fornecedores_cafe = FornecedoraCafeDAO()
        self.__tela_empresa_cafe = TelaEmpresaCafe()

    def tem_empresas(self) -> bool:
        return len(list(self.__fornecedores_cafe.get_all())) > 0

    def pega_fornecedor_por_cnpj(self, cnpj: str) -> FornecedoraCafe:
        """
        Recupera um fornecedor de café específico pelo CNPJ. Lança exceção
        se não encontrado. Usado internamente e por outros controladores
        (ex: ControladorCafe para validar fornecedor antes de criar café).
        """
        fornecedor = self.__fornecedores_cafe.get(cnpj)
        if fornecedor is None:
            raise FornecedorNaoEncontradoException()
        return fornecedor

    def incluir_fornecedor(self) -> None:
        """
        Processa o cadastro de um novo fornecedor de café. Coleta dados do
        usuário através da tela, valida que não existe fornecedor (de café
        ou máquina) com o mesmo CNPJ usando mixin e persiste o novo fornecedor.
        Exibe mensagens de sucesso ou erro conforme o resultado.
        """
        dados_fornecedor = self.__tela_empresa_cafe.pega_dados_empresa_cafe(
            is_alteracao=False)
        if not dados_fornecedor:
            return

        if self.existe_fornecedor_com_cnpj(dados_fornecedor["cnpj"]):
            self.__tela_empresa_cafe.mostra_mensagem(
                "ERRO: Já existe um fornecedor com este CNPJ!")
        else:
            novo_fornecedor = FornecedoraCafe(
                dados_fornecedor["nome"], dados_fornecedor["cnpj"],
                dados_fornecedor["endereco"], dados_fornecedor["telefone"],
                dados_fornecedor["tipo_cafe"]
            )
            self.__fornecedores_cafe.add(novo_fornecedor)
            self.__tela_empresa_cafe.mostra_mensagem(
                "Fornecedor de café cadastrado com sucesso!")

    def alterar_fornecedor(self) -> None:
        """
        Processa a alteração de um fornecedor existente. Lista fornecedores
        disponíveis, permite seleção por CNPJ, coleta novos dados e atualiza
        propriedades (exceto CNPJ que é imutável). Exibe lista atualizada
        após sucesso.
        """
        if not list(self.__fornecedores_cafe.get_all()):
            self.__tela_empresa_cafe.mostra_mensagem(
                "Nenhum fornecedor cadastrado para alterar!")
            return

        self.lista_fornecedores()
        cnpj_fornecedor = self.__tela_empresa_cafe.seleciona_empresa_cafe()
        if not cnpj_fornecedor:
            return
        fornecedor = self.pega_fornecedor_por_cnpj(cnpj_fornecedor)
        novos_dados = self.__tela_empresa_cafe.pega_dados_empresa_cafe(
            is_alteracao=True)
        if not novos_dados:
            return
        fornecedor.nome = novos_dados["nome"]
        fornecedor.endereco = novos_dados["endereco"]
        fornecedor.telefone = novos_dados["telefone"]
        fornecedor.tipo_cafe = novos_dados["tipo_cafe"]

        self.__fornecedores_cafe.update(fornecedor)

        self.__tela_empresa_cafe.mostra_mensagem(
            "Fornecedor alterado com sucesso!")
        self.lista_fornecedores()

    def lista_fornecedores(self) -> None:
        """
        Exibe lista formatada de todos os fornecedores de café cadastrados.
        Extrai informações relevantes (nome, CNPJ, tipo de café) e delega a
        exibição para a tela. Usado tanto para visualização quanto como passo
        intermediário em operações de alteração e exclusão.
        """
        fornecedores = list(self.__fornecedores_cafe.get_all())
        if not fornecedores:
            self.__tela_empresa_cafe.mostra_mensagem(
                "Nenhum fornecedor de café cadastrado!")
            return

        dados_fornecedores = []
        for fornecedor in fornecedores:
            dados_fornecedores.append({
                "nome": fornecedor.nome,
                "cnpj": fornecedor.cnpj,
                "tipo_cafe": fornecedor.tipo_cafe
            })
        self.__tela_empresa_cafe.mostra_lista_fornecedores(dados_fornecedores)

    def excluir_fornecedor(self) -> None:
        """
        Processa a exclusão de um fornecedor. Lista fornecedores, permite
        seleção por CNPJ, valida que não existem cafés usando este fornecedor
        (mantendo integridade referencial) e remove do repositório. Exibe
        lista atualizada após exclusão bem-sucedida.
        """
        if not list(self.__fornecedores_cafe.get_all()):
            self.__tela_empresa_cafe.mostra_mensagem(
                "Nenhum fornecedor cadastrado para excluir!")
            return

        self.lista_fornecedores()
        cnpj_fornecedor = self.__tela_empresa_cafe.seleciona_empresa_cafe()
        if not cnpj_fornecedor:
            return
        fornecedor = self.pega_fornecedor_por_cnpj(cnpj_fornecedor)

        # Verifica se existe algum café usando este fornecedor
        cafes_usando_fornecedor = []
        for cafe in self._controlador_sistema.controlador_cafe.cafes:
            if cafe.empresa_fornecedora == fornecedor:
                cafes_usando_fornecedor.append(cafe)

        if cafes_usando_fornecedor:
            self.__tela_empresa_cafe.mostra_mensagem(
                f"ERRO: Não é possível excluir este fornecedor!")
            self.__tela_empresa_cafe.mostra_mensagem(
                f"Existem {len(cafes_usando_fornecedor)} café(s) cadastrado(s) que utilizam este fornecedor.")
            self.__tela_empresa_cafe.mostra_mensagem(
                "Exclua os cafés primeiro ou altere o fornecedor deles.")
            return

        self.__fornecedores_cafe.remove(fornecedor.cnpj)
        self.__tela_empresa_cafe.mostra_mensagem(
            "Fornecedor excluído com sucesso!")
        self.lista_fornecedores()

    def retornar(self) -> None:
        self._controlador_sistema.abre_tela()

    def abre_tela(self) -> None:
        mapa_opcoes = {
            1: self.incluir_fornecedor, 2: self.alterar_fornecedor,
            3: self.lista_fornecedores, 4: self.excluir_fornecedor,
            0: self.retornar
        }
        while True:
            try:
                opcao = self.__tela_empresa_cafe.tela_opcoes()
                if opcao is None:
                    break
                if opcao == 0:
                    self.retornar()
                    break

                funcao_escolhida = mapa_opcoes.get(opcao)
                if funcao_escolhida:
                    funcao_escolhida()
                else:
                    self.__tela_empresa_cafe.mostra_mensagem(
                        "Opção inválida! Por favor, digite um número do menu.")
            except FornecedorNaoEncontradoException as e:
                self.__tela_empresa_cafe.mostra_mensagem(f"ERRO: {e}")
            except TypeError as e:
                self.__tela_empresa_cafe.mostra_mensagem(f"ERRO: {e}")
