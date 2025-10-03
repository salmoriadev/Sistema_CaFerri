from limite.telaCafe import TelaCafe
from entidade.cafe import Cafe
from Excecoes.cafeNaoEncontradoException import CafeNaoEncontradoException
from Excecoes.perfilRecomendadoNaoExisteException import PerfilRecomendadoNaoExisteException
from Excecoes.produtoNaoEncontradoException import ProdutoNaoEncontradoException

class ControladorCafe:
    def __init__(self, controlador_sistema):
        self.__cafes = []
        self.__controlador_sistema = controlador_sistema
        self.__tela_cafe = TelaCafe()

    def pega_cafe_por_id(self, id: int):
        if not isinstance(id, int):
            raise TypeError("O ID do café deve ser um número inteiro.")
        for cafe in self.__cafes:
            if cafe.id == id:
                return cafe
        raise CafeNaoEncontradoException(id)

    def incluir_cafe(self):
        dados_cafe = self.__tela_cafe.pega_dados_cafe()

        if self.__controlador_sistema.id_produto_ja_existe(dados_cafe["id"]):
            self.__tela_cafe.mostra_mensagem("ERRO: Já existe um produto (café ou máquina) com este ID!")
            return

        novo_cafe = Cafe(
            dados_cafe["nome"], dados_cafe["preco_compra"], dados_cafe["preco_venda"],
            dados_cafe["id"], dados_cafe["data_fabricacao"], dados_cafe["origem"],
            dados_cafe["variedade"], dados_cafe["altitude"], dados_cafe["moagem"],
            dados_cafe["notas_sensoriais"], dados_cafe["perfil_recomendado"]
        )
        self.__cafes.append(novo_cafe)
        self.__tela_cafe.mostra_mensagem("Café cadastrado com sucesso!")

    def alterar_cafe(self):
        if not self.__cafes:
            self.__tela_cafe.mostra_mensagem("Nenhum café cadastrado para alterar!")
            return

        self.lista_cafe()
        id_cafe = self.__tela_cafe.seleciona_cafe()
        cafe = self.pega_cafe_por_id(id_cafe)

        novos_dados = self.__tela_cafe.pega_dados_cafe()
        cafe.nome = novos_dados["nome"]
        cafe.preco_compra = novos_dados["preco_compra"]
        cafe.preco_venda = novos_dados["preco_venda"]
        cafe.id = novos_dados["id"]
        cafe.data_fabricacao = novos_dados["data_fabricacao"]
        cafe.origem = novos_dados["origem"]
        cafe.variedade = novos_dados["variedade"]
        cafe.altitude = novos_dados["altitude"]
        cafe.moagem = novos_dados["moagem"]
        cafe.notas_sensoriais = novos_dados["notas_sensoriais"]
        cafe.perfil_recomendado = novos_dados["perfil_recomendado"]
        
        self.__tela_cafe.mostra_mensagem("Café alterado com sucesso!")
        self.lista_cafe()

    def lista_cafe(self):
        if not self.__cafes:
            self.__tela_cafe.mostra_mensagem("Nenhum café cadastrado!")
            return

        self.__tela_cafe.mostra_mensagem("--- LISTA DE CAFÉS ---")
        for cafe in self.__cafes:
            dados_cafe = {
                "id": cafe.id,
                "nome": cafe.nome,
                "preco_venda": cafe.preco_venda,
                "perfil_recomendado": cafe.perfil_recomendado.perfil
            }
            self.__tela_cafe.mostra_cafe(dados_cafe)

    def excluir_cafe(self):
        if not self.__cafes:
            self.__tela_cafe.mostra_mensagem("Nenhum café cadastrado para excluir!")
            return

        self.lista_cafe()
        id_cafe = self.__tela_cafe.seleciona_cafe()
        cafe = self.pega_cafe_por_id(id_cafe)
        
        self.__cafes.remove(cafe)
        self.__tela_cafe.mostra_mensagem("Café excluído com sucesso!")
        self.lista_cafe()

    def retornar(self):
        self.__controlador_sistema.abre_tela()

    def abre_tela(self):
        lista_opcoes = {
            1: self.incluir_cafe, 2: self.alterar_cafe,
            3: self.lista_cafe, 4: self.excluir_cafe,
            0: self.retornar
        }
        while True:
            try:
                opcao = self.__tela_cafe.tela_opcoes()
                if opcao == 0:
                    self.retornar()
                    break
                
                funcao_escolhida = lista_opcoes.get(opcao)
                if funcao_escolhida:
                    funcao_escolhida()
                else:
                    self.__tela_cafe.mostra_mensagem("Opção inválida! Por favor, digite um número do menu.")
            
            except (CafeNaoEncontradoException, PerfilRecomendadoNaoExisteException, TypeError) as e:
                self.__tela_cafe.mostra_mensagem(f"Ocorreu um erro: {e}")
