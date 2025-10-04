from limite.telaEmpresaMaquina import TelaEmpresaMaquina
from entidade.fornecedora_maquina import FornecedoraMaquina
from Excecoes.fornecedorNaoEncontradoException import FornecedorNaoEncontradoException

class ControladorEmpresaMaquina:
    def __init__(self, controlador_sistema):
        self._controlador_sistema = controlador_sistema
        self.__fornecedores_maquina = []
        self.__tela_empresa_maquina = TelaEmpresaMaquina()

    def pega_fornecedor_por_cnpj(self, cnpj: str) -> FornecedoraMaquina:
        for fornecedor in self.__fornecedores_maquina:
            if fornecedor.cnpj == cnpj:
                return fornecedor
        raise FornecedorNaoEncontradoException

    def incluir_fornecedor(self):
        dados_fornecedor = self.__tela_empresa_maquina.pega_dados_empresa_maquina(is_alteracao=False)
        
        try:
            self.pega_fornecedor_por_cnpj(dados_fornecedor["cnpj"])
            self.__tela_empresa_maquina.mostra_mensagem("ERRO: Já existe um fornecedor com este CNPJ!")
        except FornecedorNaoEncontradoException:
            novo_fornecedor = FornecedoraMaquina(
                dados_fornecedor["nome"], dados_fornecedor["cnpj"],
                dados_fornecedor["endereco"], dados_fornecedor["telefone"],
                dados_fornecedor["pais_de_origem"]
            )
            self.__fornecedores_maquina.append(novo_fornecedor)
            self.__tela_empresa_maquina.mostra_mensagem("Fornecedor de máquina cadastrado com sucesso!")

    def alterar_fornecedor(self):
        if not self.__fornecedores_maquina:
            self.__tela_empresa_maquina.mostra_mensagem("Nenhum fornecedor cadastrado para alterar!")
            return

        self.lista_fornecedores()
        cnpj_fornecedor = self.__tela_empresa_maquina.seleciona_empresa_maquina()
        fornecedor = self.pega_fornecedor_por_cnpj(cnpj_fornecedor)

        novos_dados = self.__tela_empresa_maquina.pega_dados_empresa_maquina(is_alteracao=True)
        
        fornecedor.nome = novos_dados["nome"]
        fornecedor.endereco = novos_dados["endereco"]
        fornecedor.telefone = novos_dados["telefone"]
        fornecedor.pais_de_origem = novos_dados["pais_de_origem"]
        
        self.__tela_empresa_maquina.mostra_mensagem("Fornecedor alterado com sucesso!")
        self.lista_fornecedores()

    def lista_fornecedores(self):
        if not self.__fornecedores_maquina:
            self.__tela_empresa_maquina.mostra_mensagem("Nenhum fornecedor de máquina cadastrado!")
            return

        self.__tela_empresa_maquina.mostra_mensagem("--- LISTA DE FORNECEDORES DE MÁQUINA ---")
        for fornecedor in self.__fornecedores_maquina:
            dados_fornecedor = {
                "nome": fornecedor.nome,
                "cnpj": fornecedor.cnpj,
                "pais_de_origem": fornecedor.pais_de_origem
            }
            self.__tela_empresa_maquina.mostra_empresa_maquina(dados_fornecedor)

    def excluir_fornecedor(self):
        if not self.__fornecedores_maquina:
            self.__tela_empresa_maquina.mostra_mensagem("Nenhum fornecedor cadastrado para excluir!")
            return

        self.lista_fornecedores()
        cnpj_fornecedor = self.__tela_empresa_maquina.seleciona_empresa_maquina()
        fornecedor = self.pega_fornecedor_por_cnpj(cnpj_fornecedor)
        
        self.__fornecedores_maquina.remove(fornecedor)
        self.__tela_empresa_maquina.mostra_mensagem("Fornecedor excluído com sucesso!")
        self.lista_fornecedores()

    def retornar(self):
        self._controlador_sistema.abre_tela()

    def abre_tela(self):
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