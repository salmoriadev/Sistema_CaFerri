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

class ControladorEmpresaCafe(BuscaProdutoMixin):
    def __init__(self, controlador_sistema):
        self._controlador_sistema = controlador_sistema
        self.__fornecedores_cafe = []
        self.__tela_empresa_cafe = TelaEmpresaCafe()

    def tem_empresas(self) -> bool:
        return len(self.__fornecedores_cafe) > 0

    def pega_fornecedor_por_cnpj(self, cnpj: str) -> FornecedoraCafe:
        for fornecedor in self.__fornecedores_cafe:
            if fornecedor.cnpj == cnpj:
                return fornecedor
        raise FornecedorNaoEncontradoException()

    def incluir_fornecedor(self) -> None:
        dados_fornecedor = self.__tela_empresa_cafe.pega_dados_empresa_cafe(is_alteracao=False)

        if self.existe_fornecedor_com_cnpj(dados_fornecedor["cnpj"]):
            self.__tela_empresa_cafe.mostra_mensagem(
                "ERRO: Já existe um fornecedor com este CNPJ!")
        else:
            novo_fornecedor = FornecedoraCafe(
                dados_fornecedor["nome"], dados_fornecedor["cnpj"],
                dados_fornecedor["endereco"], dados_fornecedor["telefone"],
                dados_fornecedor["tipo_cafe"]
            )
            self.__fornecedores_cafe.append(novo_fornecedor)
            self.__tela_empresa_cafe.mostra_mensagem(
                "Fornecedor de café cadastrado com sucesso!")

    def alterar_fornecedor(self) -> None:
        if not self.__fornecedores_cafe:
            self.__tela_empresa_cafe.mostra_mensagem(
                "Nenhum fornecedor cadastrado para alterar!")
            return

        self.lista_fornecedores()
        cnpj_fornecedor = self.__tela_empresa_cafe.seleciona_empresa_cafe()
        fornecedor = self.pega_fornecedor_por_cnpj(cnpj_fornecedor)
        novos_dados = self.__tela_empresa_cafe.pega_dados_empresa_cafe(is_alteracao=True)
        fornecedor.nome = novos_dados["nome"]
        fornecedor.endereco = novos_dados["endereco"]
        fornecedor.telefone = novos_dados["telefone"]
        fornecedor.tipo_cafe = novos_dados["tipo_cafe"]
        
        self.__tela_empresa_cafe.mostra_mensagem("Fornecedor alterado com sucesso!")
        self.lista_fornecedores()

    def lista_fornecedores(self) -> None:
        if not self.__fornecedores_cafe:
            self.__tela_empresa_cafe.mostra_mensagem("Nenhum fornecedor de café cadastrado!")
            return

        self.__tela_empresa_cafe.mostra_mensagem("--- LISTA DE FORNECEDORES DE CAFÉ ---")
        for fornecedor in self.__fornecedores_cafe:
            dados_fornecedor = {
                "nome": fornecedor.nome,
                "cnpj": fornecedor.cnpj,
                "tipo_cafe": fornecedor.tipo_cafe
            }
            self.__tela_empresa_cafe.mostra_empresa_cafe(dados_fornecedor)

    def excluir_fornecedor(self) -> None:
        if not self.__fornecedores_cafe:
            self.__tela_empresa_cafe.mostra_mensagem("Nenhum fornecedor cadastrado para excluir!")
            return

        self.lista_fornecedores()
        cnpj_fornecedor = self.__tela_empresa_cafe.seleciona_empresa_cafe()
        fornecedor = self.pega_fornecedor_por_cnpj(cnpj_fornecedor)
        
        # Verifica se existe algum café usando este fornecedor
        cafes_usando_fornecedor = []
        for cafe in self._controlador_sistema.controlador_cafe.cafes:
            if cafe.empresa_fornecedora == fornecedor:
                cafes_usando_fornecedor.append(cafe)
        
        if cafes_usando_fornecedor:
            self.__tela_empresa_cafe.mostra_mensagem(f"ERRO: Não é possível excluir este fornecedor!")
            self.__tela_empresa_cafe.mostra_mensagem(
                f"Existem {len(cafes_usando_fornecedor)} café(s) cadastrado(s) que utilizam este fornecedor.")
            self.__tela_empresa_cafe.mostra_mensagem(
                "Exclua os cafés primeiro ou altere o fornecedor deles.")
            return
        
        self.__fornecedores_cafe.remove(fornecedor)
        self.__tela_empresa_cafe.mostra_mensagem("Fornecedor excluído com sucesso!")
        self.lista_fornecedores()

    def retornar(self) -> None:
        self._controlador_sistema.abre_tela()

    def abre_tela(self) -> None:
        lista_opcoes = {
            1: self.incluir_fornecedor, 2: self.alterar_fornecedor,
            3: self.lista_fornecedores, 4: self.excluir_fornecedor,
            0: self.retornar
        }
        while True:
            try:
                opcao = self.__tela_empresa_cafe.tela_opcoes()
                funcao_escolhida = lista_opcoes.get(opcao)
                if funcao_escolhida:
                    funcao_escolhida()
                    if opcao == 0:
                        break
                else:
                    self.__tela_empresa_cafe.mostra_mensagem("Opção inválida!")
            except FornecedorNaoEncontradoException as e:
                self.__tela_empresa_cafe.mostra_mensagem(f"ERRO: {e}")
            except TypeError as e:
                self.__tela_empresa_cafe.mostra_mensagem(f"ERRO: {e}")