from limite.telaMaquinaDeCafe import TelaMaquinaCafe
from entidade.maquina_de_cafe import MaquinaDeCafe
from Excecoes.maquinaNaoEncontradaException import MaquinaNaoEncontradaException

class ControladorMaquinaDeCafe:
    def __init__(self, controlador_sistema):
        self.__maquinas = []
        self.__controlador_sistema = controlador_sistema
        self.__tela_maquina = TelaMaquinaCafe()

    def pega_maquina_por_id(self, id: int):
        if not isinstance(id, int):
            raise TypeError("O ID da máquina deve ser um número inteiro.")
        for maquina in self.__maquinas:
            if maquina.id == id:
                return maquina
        raise MaquinaNaoEncontradaException

    def incluir_maquina(self):
        dados_maquina = self.__tela_maquina.pega_dados_maquina()

        for maquina in self.__maquinas:
            if maquina.id == dados_maquina["id"]:
                self.__tela_maquina.mostra_mensagem("ERRO: Já existe uma máquina com este ID!")
                return

        nova_maquina = MaquinaDeCafe(
            dados_maquina["nome"], dados_maquina["preco_compra"], dados_maquina["preco_venda"],
            dados_maquina["id"], dados_maquina["data_fabricacao"]
        )
        self.__maquinas.append(nova_maquina)
        self.__tela_maquina.mostra_mensagem("Máquina cadastrada com sucesso!")

    def alterar_maquina(self):
        if not self.__maquinas:
            self.__tela_maquina.mostra_mensagem("Nenhuma máquina cadastrada para alterar!")
            return

        self.lista_maquina()
        id_maquina = self.__tela_maquina.seleciona_maquina()
        maquina = self.pega_maquina_por_id(id_maquina)

        novos_dados = self.__tela_maquina.pega_dados_maquina()
        maquina.nome = novos_dados["nome"]
        maquina.preco_compra = novos_dados["preco_compra"]
        maquina.preco_venda = novos_dados["preco_venda"]
        maquina.id = novos_dados["id"]
        maquina.data_fabricacao = novos_dados["data_fabricacao"]

        self.__tela_maquina.mostra_mensagem("Máquina alterada com sucesso!")
        self.lista_maquina()

    def lista_maquina(self):
        if not self.__maquinas:
            self.__tela_maquina.mostra_mensagem("Nenhuma máquina cadastrada!")
            return

        self.__tela_maquina.mostra_mensagem("--- LISTA DE MÁQUINAS ---")
        for maquina in self.__maquinas:
            dados_maquina = {
                "id": maquina.id,
                "nome": maquina.nome,
                "preco_venda": maquina.preco_venda,
            }
            self.__tela_maquina.mostra_maquina(dados_maquina)

    def excluir_maquina(self):
        if not self.__maquinas:
            self.__tela_maquina.mostra_mensagem("Nenhuma máquina cadastrada para excluir!")
            return

        self.lista_maquina()
        id_maquina = self.__tela_maquina.seleciona_maquina()
        maquina = self.pega_maquina_por_id(id_maquina)

        self.__maquinas.remove(maquina)
        self.__tela_maquina.mostra_mensagem("Máquina excluída com sucesso!")
        self.lista_maquina()

    def retornar(self):
        self.__controlador_sistema.abre_tela()

    def abre_tela(self):
        lista_opcoes = {
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
                
                funcao_escolhida = lista_opcoes.get(opcao)
                if funcao_escolhida:
                    funcao_escolhida()
                else:
                    self.__tela_maquina.mostra_mensagem("Opção inválida! Por favor, digite um número do menu.")
            
            except (MaquinaNaoEncontradaException, TypeError) as e:
                self.__tela_maquina.mostra_mensagem(f"Ocorreu um erro: {e}")
