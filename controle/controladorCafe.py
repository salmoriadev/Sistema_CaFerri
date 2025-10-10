from Excecoes.fornecedorNaoEncontradoException import FornecedorNaoEncontradoException
from controle.buscaProdutoMixin import BuscaProdutoMixin
from limite.telaCafe import TelaCafe
from entidade.cafe import Cafe
from Excecoes.cafeNaoEncontradoException import CafeNaoEncontradoException
from Excecoes.perfilRecomendadoNaoExisteException import PerfilRecomendadoNaoExisteException

class ControladorCafe(BuscaProdutoMixin):
    def __init__(self, controlador_sistema) -> None:
        self.__cafes = []
        self._controlador_sistema = controlador_sistema
        self.__tela_cafe = TelaCafe()
    
    @property
    def cafes(self) -> list:
        return self.__cafes

    def pega_cafe_por_id(self, id: int) -> Cafe:
        if not isinstance(id, int):
            raise TypeError("O ID do café deve ser um número inteiro.")
        for cafe in self.__cafes:
            if cafe.id == id:
                return cafe
        raise CafeNaoEncontradoException()

    def incluir_cafe(self) -> None:
        dados_cafe = self.__tela_cafe.pega_dados_cafe(is_alteracao=False)

        if self.id_produto_ja_existe(dados_cafe["id"]):
            self.__tela_cafe.mostra_mensagem("ERRO: Já existe um produto (café ou máquina) com este ID!")
            return
        empresa_fornecedora = self._controlador_sistema.controlador_empresa_cafe.pega_fornecedor_por_cnpj(dados_cafe["empresa_fornecedora"])
        novo_cafe = Cafe(
            dados_cafe["nome"], dados_cafe["preco_compra"], dados_cafe["preco_venda"],
            dados_cafe["id"], dados_cafe["data_fabricacao"], dados_cafe["origem"],
            dados_cafe["variedade"], dados_cafe["altitude"], dados_cafe["moagem"],
            dados_cafe["notas_sensoriais"], dados_cafe["perfil_recomendado"],
            empresa_fornecedora
        )
        self.__cafes.append(novo_cafe)
        self.__tela_cafe.mostra_mensagem("Café cadastrado com sucesso!")

    def alterar_cafe(self) -> None:
        if not self.__cafes:
            self.__tela_cafe.mostra_mensagem("Nenhum café cadastrado para alterar!")
            return

        self.lista_cafe()
        id_cafe = self.__tela_cafe.seleciona_cafe()
        cafe = self.pega_cafe_por_id(id_cafe)

        novos_dados = self.__tela_cafe.pega_dados_cafe(is_alteracao=True)
        
        cafe.nome = novos_dados["nome"]
        cafe.preco_compra = novos_dados["preco_compra"]
        cafe.preco_venda = novos_dados["preco_venda"]
        cafe.data_fabricacao = novos_dados["data_fabricacao"]
        cafe.origem = novos_dados["origem"]
        cafe.variedade = novos_dados["variedade"]
        cafe.altitude = novos_dados["altitude"]
        cafe.moagem = novos_dados["moagem"]
        cafe.notas_sensoriais = novos_dados["notas_sensoriais"]
        cafe.perfil_recomendado = novos_dados["perfil_recomendado"]
        cafe.empresa_fornecedora = self._controlador_sistema.controlador_empresa_cafe.pega_fornecedor_por_cnpj(novos_dados["empresa_fornecedora"])
        
        self.__tela_cafe.mostra_mensagem("Café alterado com sucesso!")
        self.lista_cafe()

    def buscar_cafes_por_perfil(self, perfil: str) -> list:
        cafes_encontrados = []
        for cafe in self.__cafes:
            if cafe.perfil_recomendado.perfil == perfil:
                cafes_encontrados.append(cafe)
        return cafes_encontrados

    def lista_cafe(self) -> None:
        if not self.__cafes:
            self.__tela_cafe.mostra_mensagem("Nenhum café cadastrado!")
            return

        self.__tela_cafe.mostra_mensagem("--- LISTA DE CAFÉS ---")
        for cafe in self.__cafes:
            dados_cafe = {
                "id": cafe.id,
                "nome": cafe.nome,
                "preco_venda": cafe.preco_venda,
                "perfil_recomendado": cafe.perfil_recomendado.perfil,
                "empresa_fornecedora_nome": cafe.empresa_fornecedora.nome
            }
            self.__tela_cafe.mostra_cafe(dados_cafe)

    def excluir_cafe(self) -> None:
        if not self.__cafes:
            self.__tela_cafe.mostra_mensagem("Nenhum café cadastrado para excluir!")
            return

        self.lista_cafe()
        id_cafe = self.__tela_cafe.seleciona_cafe()
        cafe = self.pega_cafe_por_id(id_cafe)
        
        self.__cafes.remove(cafe)
        self.__tela_cafe.mostra_mensagem("Café excluído com sucesso!")
        self.lista_cafe()

    def retornar(self) -> None:
        self._controlador_sistema.abre_tela()

    def abre_tela(self) -> None:
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

            except (CafeNaoEncontradoException, PerfilRecomendadoNaoExisteException, TypeError, FornecedorNaoEncontradoException) as e:
                self.__tela_cafe.mostra_mensagem(f"Ocorreu um erro: {e}")
