from Excecoes.cafeNaoEncontradoException import CafeNaoEncontradoException
from Excecoes.perfilRecomendadoNaoExisteException import PerfilRecomendadoNaoExisteException
from entidade.perfil_consumidor import PerfilConsumidor
from limite.telaCafe import TelaCafe
from entidade.cafe import Cafe

class ControladorCafe():

  def __init__(self, controlador_sistema):
    self.__cafes = []
    self.__controlador_sistema = controlador_sistema
    self.__tela_cafe = TelaCafe()

  def pega_cafe_por_id(self, id: int):
    if not isinstance(id, int):
      self.__tela_cafe.mostra_mensagem("Digite um número inteiro!")
      return None
    for cafe in self.__cafes:
      if cafe.id == id:
        return cafe
    return None

  def incluir_cafe(self):
    dados_cafe = self.__tela_cafe.pega_dados_cafe()
    cafe_repetido = self.pega_cafe_por_id(dados_cafe["id"])
    perfil_teste = PerfilConsumidor(dados_cafe["perfil_recomendado"])
    if dados_cafe["perfil_recomendado"] not in perfil_teste.possiveis_perfis:
        raise PerfilRecomendadoNaoExisteException(dados_cafe["perfil_recomendado"])
    elif cafe_repetido is None:
      cafe = Cafe(dados_cafe["nome"], dados_cafe["preco_compra"], dados_cafe["preco_venda"],
                  dados_cafe["id"], dados_cafe["data_fabricacao"], 
                  dados_cafe["origem"], dados_cafe["variedade"], dados_cafe["altitude"], 
                  dados_cafe["moagem"], dados_cafe["notas_sensoriais"], dados_cafe["perfil_recomendado"])
      self.__cafes.append(cafe)
      self.__tela_cafe.mostra_mensagem("Cafe cadastrado!")
    else:
      self.__tela_cafe.mostra_mensagem("ATENCAO: Cafe já existente")

  def alterar_cafe(self):
    self.lista_cafe()
    codigo_cafe = self.__tela_cafe.seleciona_cafe()
    cafe = self.pega_cafe_por_id(codigo_cafe)
    if cafe is None:
        raise CafeNaoEncontradoException(codigo_cafe)
    else:
        self.__tela_cafe.mostra_mensagem("--- Digite os novos dados ---")
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
        if novos_dados["perfil_recomendado"] not in cafe.perfil_recomendado.possiveis_perfis:
            raise PerfilRecomendadoNaoExisteException(novos_dados["perfil_recomendado"])
        else:
            cafe.perfil_recomendado = novos_dados["perfil_recomendado"]
        self.__tela_cafe.mostra_mensagem("Café alterado com sucesso!")
        self.lista_cafe()

  def lista_cafe(self):
    if len(self.__cafes) == 0:
      self.__tela_cafe.mostra_mensagem("ATENCAO: Nenhum café cadastrado")
      return
    for cafe in self.__cafes:
        self.__tela_cafe.mostra_cafe({"nome": cafe.nome, "id": cafe.id, "preco_compra": cafe.preco_compra,
                                     "preco_venda": cafe.preco_venda, "data_fabricacao": cafe.data_fabricacao,
                                     "origem": cafe.origem, "variedade": cafe.variedade, "altitude": cafe.altitude,
                                     "moagem": cafe.moagem, "notas_sensoriais": cafe.notas_sensoriais, "perfil_recomendado": cafe.perfil_recomendado.perfil})

  def excluir_cafe(self):
    self.lista_cafe()
    id_cafe = self.__tela_cafe.seleciona_cafe()
    cafe = self.pega_cafe_por_id(id_cafe)
    if cafe is None:
      raise CafeNaoEncontradoException(id_cafe)
    else:
      self.__cafes.remove(cafe)
      self.lista_cafe()
      return

  def retornar(self):
    self.__controlador_sistema.abre_tela()

  def abre_tela(self):
      lista_opcoes = {1: self.incluir_cafe, 2: self.alterar_cafe, 3: self.lista_cafe, 4: self.excluir_cafe, 0: self.retornar}

      while True:
          opcao = self.__tela_cafe.tela_opcoes()
          if opcao == 0:
            self.retornar()
            break 
          funcao_escolhida = lista_opcoes.get(opcao)
          if funcao_escolhida:
              try:
                  funcao_escolhida()
              except (CafeNaoEncontradoException, PerfilRecomendadoNaoExisteException) as e:
                  self.__tela_cafe.mostra_mensagem(e)
          else:
              self.__tela_cafe.mostra_mensagem("Opção inválida! Por favor, digite um número do menu.")