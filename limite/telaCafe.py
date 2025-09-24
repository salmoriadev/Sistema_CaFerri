class TelaCafe():
  # fazer aqui tratamento dos dados, caso a entrada seja diferente do esperado
  def tela_opcoes(self):
    print("-------- Cafés ----------")
    print("Escolha a opcao")
    print("1 - Adicionar Café")
    print("2 - Alterar atributos do Café")
    print("3 - Listar Cafés")
    print("4 - Excluir Café")
    print("0 - Retornar")
    print("Para adicionar o café criado ao estoque, você deve ir ao menu do estoque e adicionar esse café.")

    opcao = int(input("Escolha a opcao: "))
    return opcao

  # fazer aqui tratamento dos dados, caso a entrada seja diferente do esperado
  def pega_dados_café(self):
    print("-------- DADOS CAFÉ ----------")
    nome = input("Nome: ")
    preco_compra = float(input("Preço de Compra: "))
    preco_venda = float(input("Preço de Venda: "))
    estoque = int(input("Estoque: "))
    id = int(input("ID: "))
    data_fabricacao = input("Data de Fabricação: ")
    origem = input("Origem: ")
    variedade = input("Variedade: ")
    altitude = int(input("Altitude: "))
    moagem = input("Moagem: ")
    notas_sensoriais = input("Notas Sensoriais: ")
    perfil_recomendado = input("Perfil Recomendado: ")

    return {"nome": nome, "preco_compra": preco_compra, "preco_venda": preco_venda, "estoque": estoque, "id": id, "data_fabricacao": data_fabricacao, "origem": origem, "variedade": variedade, "altitude": altitude, "moagem": moagem, "notas_sensoriais": notas_sensoriais, "perfil_recomendado": perfil_recomendado}


  # fazer aqui tratamento dos dados, caso a entrada seja diferente do esperado
  def mostra_cafe(self, dados_cafe):
    print("NOME DO CAFÉ: ", dados_cafe["nome"])
    print("PREÇO DE COMPRA: ", dados_cafe["preco_compra"])
    print("PREÇO DE VENDA: ", dados_cafe["preco_venda"])
    print("ESTOQUE: ", dados_cafe["estoque"])
    print("ID: ", dados_cafe["id"])
    print("DATA DE FABRICAÇÃO: ", dados_cafe["data_fabricacao"])
    print("ORIGEM: ", dados_cafe["origem"])
    print("VARIEDADE: ", dados_cafe["variedade"])
    print("ALTITUDE: ", dados_cafe["altitude"])
    print("MOAGEM: ", dados_cafe["moagem"])
    print("NOTAS SENSORIAIS: ", dados_cafe["notas_sensoriais"])
    print("PERFIL RECOMENDADO: ", dados_cafe["perfil_recomendado"])
    print("\n")

  # fazer aqui tratamento dos dados, caso a entrada seja diferente do esperado
  def seleciona_cafe(self):
    id = int(input("ID do café que deseja selecionar: "))
    return id

  def mostra_mensagem(self, msg):
    print(msg)