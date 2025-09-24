from limite.telaCafe import TelaCafe
from entidade.cafe import Cafe

class ControladorCafe():

  # Fazer lançamento e tratamento de exceções, ao invés de apenas mostrar mensagem na tela.
  def __init__(self, controlador_sistema):
    self.__cafes = []
    self.__controlador_sistema = controlador_sistema
    self.__tela_cafe = TelaCafe()

  def pega_cafe_por_id(self, id: int):
    for cafe in self.__cafes:
      if cafe.id == id:
        return cafe
    return None

  def incluir_cafe(self):
    dados_cafe = self.__tela_cafe.pega_dados_cafe()
    c = self.pega_cafe_por_id(dados_cafe["id"])
    if c is None:
      cafe = Cafe(dados_cafe["nome"], dados_cafe["preco_compra"], dados_cafe["preco_venda"],
                  dados_cafe["estoque"], dados_cafe["id"], dados_cafe["data_fabricacao"], 
                  dados_cafe["origem"], dados_cafe["variedade"], dados_cafe["altitude"], 
                  dados_cafe["moagem"], dados_cafe["notas_sensoriais"], dados_cafe["perfil_recomendado"])
      self.__cafes.append(cafe)
    else:
      self.__tela_cafe.mostra_mensagem("ATENCAO: Cafe já existente")

  def alterar_cafe(self):
    self.lista_cafe()
    codigo_cafe = self.__tela_cafe.seleciona_cafe()
    cafe = self.pega_cafe_por_id(codigo_cafe)

    if cafe is not None:
      novos_dados_cafe = self.__tela_cafe.pega_dados_cafe()
      cafe.titulo = novos_dados_cafe["titulo"]
      cafe.id = novos_dados_cafe["id"]
      self.lista_cafe()
    else:
      self.__tela_cafe.mostra_mensagem("ATENCAO: Cafe não existente")

  # Sugestão: se a lista estiver vazia, mostrar a mensagem de lista vazia
  def lista_cafe(self):
    if len(self.__cafes) == 0:
      self.__tela_cafe.mostra_mensagem("ATENCAO: Nenhum café cadastrado")
    else:
        for cafe in self.__cafes:
            self.__tela_cafe.mostra_cafe({"titulo": cafe.titulo, "id": cafe.id})

  def excluir_cafe(self):
    self.lista_cafe()
    codigo_cafe = self.__tela_cafe.seleciona_cafe()
    cafe = self.pega_cafe_por_id(codigo_cafe)

    if cafe is not None:
      self.__cafes.remove(cafe)
      self.lista_cafe()
    else:
      self.__tela_cafe.mostra_mensagem("ATENCAO: Cafe não existente")

  def retornar(self):
    self.__controlador_sistema.abre_tela()

  def abre_tela(self):
    lista_opcoes = {1: self.incluir_cafe, 2: self.alterar_cafe, 3: self.lista_cafe, 4: self.excluir_cafe, 0: self.retornar}

    continua = True
    while continua:
      lista_opcoes[self.__tela_cafe.tela_opcoes()]()