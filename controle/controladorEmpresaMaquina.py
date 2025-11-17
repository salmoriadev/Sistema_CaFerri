"""
    Orquestra a lógica de negócio para o gerenciamento de Fornecedores de Máquinas.

    Esta classe desempenha o papel de Controller, estabelecendo a comunicação
    entre a interface do usuário (`TelaEmpresaMaquina`) e os modelos de dados
    (`FornecedoraMaquina`). É o componente central para todas as operações de
    CRUD (Criar, Ler, Alterar, Excluir) relacionadas aos fornecedores de Maquinas.
    
    Herda de `BuscaProdutoMixin` para reutilizar a funcionalidade de verificação
    de CNPJs de empresas duplicados, garantindo que cada empresa tenha um
    identificador único em todo o sistema.
    """


from controle.buscaProdutoMixin import BuscaProdutoMixin
from limite.telaEmpresaMaquina import TelaEmpresaMaquina
from entidade.fornecedora_maquina import FornecedoraMaquina
from Excecoes.fornecedorNaoEncontradoException import FornecedorNaoEncontradoException

class ControladorEmpresaMaquina(BuscaProdutoMixin):
    def __init__(self, controlador_sistema):
        self._controlador_sistema = controlador_sistema
        self.__fornecedores_maquina = []
        self.__tela_empresa_maquina = TelaEmpresaMaquina()

    def tem_empresas(self) -> bool:
        return len(self.__fornecedores_maquina) > 0

    def pega_fornecedor_por_cnpj(self, cnpj: str) -> FornecedoraMaquina:
        for fornecedor in self.__fornecedores_maquina:
            if fornecedor.cnpj == cnpj:
                return fornecedor
        raise FornecedorNaoEncontradoException()

    def incluir_fornecedor(self) -> None:
        dados_fornecedor = self.__tela_empresa_maquina.pega_dados_empresa_maquina(is_alteracao=False)
        if not dados_fornecedor:
            return

        if self.existe_fornecedor_com_cnpj(dados_fornecedor["cnpj"]):
            self.__tela_empresa_maquina.mostra_mensagem("ERRO: Já existe um fornecedor com este CNPJ!")
        else:
            novo_fornecedor = FornecedoraMaquina(
                dados_fornecedor["nome"], dados_fornecedor["cnpj"],
                dados_fornecedor["endereco"], dados_fornecedor["telefone"],
                dados_fornecedor["pais_de_origem"]
            )
            self.__fornecedores_maquina.append(novo_fornecedor)
            self.__tela_empresa_maquina.mostra_mensagem("Fornecedor de máquina cadastrado com sucesso!")

    def alterar_fornecedor(self) -> None:
        if not self.__fornecedores_maquina:
            self.__tela_empresa_maquina.mostra_mensagem("Nenhum fornecedor cadastrado para alterar!")
            return

        self.lista_fornecedores()
        cnpj_fornecedor = self.__tela_empresa_maquina.seleciona_empresa_maquina()
        if not cnpj_fornecedor:
            return
        fornecedor = self.pega_fornecedor_por_cnpj(cnpj_fornecedor)

        novos_dados = self.__tela_empresa_maquina.pega_dados_empresa_maquina(is_alteracao=True)
        if not novos_dados:
            return
        
        fornecedor.nome = novos_dados["nome"]
        fornecedor.endereco = novos_dados["endereco"]
        fornecedor.telefone = novos_dados["telefone"]
        fornecedor.pais_de_origem = novos_dados["pais_de_origem"]
        
        self.__tela_empresa_maquina.mostra_mensagem("Fornecedor alterado com sucesso!")
        self.lista_fornecedores()

    def lista_fornecedores(self) -> None:
        if not self.__fornecedores_maquina:
            self.__tela_empresa_maquina.mostra_mensagem("Nenhum fornecedor de máquina cadastrado!")
            return

        dados_listados = []
        for fornecedor in self.__fornecedores_maquina:
            dados_listados.append({
                "nome": fornecedor.nome,
                "cnpj": fornecedor.cnpj,
                "pais_de_origem": fornecedor.pais_de_origem
            })
        self.__tela_empresa_maquina.mostra_lista_fornecedores(dados_listados)

    def excluir_fornecedor(self) -> None:
        if not self.__fornecedores_maquina:
            self.__tela_empresa_maquina.mostra_mensagem("Nenhum fornecedor cadastrado para excluir!")
            return

        self.lista_fornecedores()
        cnpj_fornecedor = self.__tela_empresa_maquina.seleciona_empresa_maquina()
        if not cnpj_fornecedor:
            return
        fornecedor = self.pega_fornecedor_por_cnpj(cnpj_fornecedor)
        
        # Verifica se existe alguma máquina usando este fornecedor
        maquinas_usando_fornecedor = []
        for maquina in self._controlador_sistema.controlador_maquina_de_cafe.maquinas:
            if maquina.empresa_fornecedora == fornecedor:
                maquinas_usando_fornecedor.append(maquina)
        
        if maquinas_usando_fornecedor:
            self.__tela_empresa_maquina.mostra_mensagem(
                f"ERRO: Não é possível excluir este fornecedor!")
            self.__tela_empresa_maquina.mostra_mensagem(
                f"Existem {len(maquinas_usando_fornecedor)} máquina(s) cadastrada(s) que utilizam este fornecedor.")
            self.__tela_empresa_maquina.mostra_mensagem(
                "Exclua as máquinas primeiro ou altere o fornecedor delas.")
            return
        
        self.__fornecedores_maquina.remove(fornecedor)
        self.__tela_empresa_maquina.mostra_mensagem("Fornecedor excluído com sucesso!")
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
                opcao = self.__tela_empresa_maquina.tela_opcoes()
                funcao_escolhida = lista_opcoes.get(opcao)
                if funcao_escolhida:
                    if opcao == 0:
                        funcao_escolhida()
                        break
                    funcao_escolhida()
                else:
                    self.__tela_empresa_maquina.mostra_mensagem("Opção inválida!")
            except FornecedorNaoEncontradoException as e:
                self.__tela_empresa_maquina.mostra_mensagem(f"ERRO: {e}")
            except TypeError as e:
                self.__tela_empresa_maquina.mostra_mensagem(f"ERRO: {e}")