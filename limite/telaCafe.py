from datetime import datetime


class TelaCafe():

  def tela_opcoes(self):
    print("-------- Cafés ----------")
    print("Escolha a opcao")
    print("1 - Adicionar Café")
    print("2 - Alterar atributos do Café")
    print("3 - Listar Cafés")
    print("4 - Excluir Café")
    print("0 - Retornar")
    print("Para adicionar o café criado ao estoque, você deve ir ao menu do estoque e adicionar esse café.")

    while True:
        try:
            opcao = int(input("Escolha a opcao: "))
            return opcao
        except ValueError:
            self.mostra_mensagem("Erro: Por favor, digite um número inteiro válido.")

  def pega_dados_cafe(self):
    print("\n-------- DADOS DO CAFÉ ----------")
    while True:
        nome = input("Nome: ")
        if nome.strip():
            break
        print("Erro: Nome inválido. Tente novamente.")

    while True:
        try:
            preco_compra = float(input("Preço de Compra: "))
            if preco_compra >= 0:
                break
            print("Erro: O preço não pode ser negativo. Tente novamente.")
        except ValueError:
            print("Erro: Entrada inválida. Por favor, insira um número (ex: 10.50).")

    while True:
        try:
            preco_venda = float(input("Preço de Venda: "))
            if preco_venda >= 0:
                break
            print("Erro: O preço não pode ser negativo. Tente novamente.")
        except ValueError:
            print("Erro: Entrada inválida. Por favor, insira um número (ex: 10.50).")
  
    while True:
        try:
            id_cafe = int(input("ID: "))
            if id_cafe >= 0:
                break
            print("Erro: O ID não pode ser um número negativo. Tente novamente.")
        except ValueError:
            print("Erro: Entrada inválida. Por favor, insira um número inteiro.")

    while True:
        data_fabricacao = input("Data de Fabricação (DD/MM/AAAA): ")
        try:
            datetime.strptime(data_fabricacao, '%d/%m/%Y')
            break
        except ValueError:
            print("Erro: Formato de data inválido. Por favor, use o formato DD/MM/AAAA.")

    while True:
        origem = input("Origem: ")
        if origem.strip():
            break
        print("Erro: A origem não pode ser vazia. Tente novamente.")

    while True:
        variedade = input("Variedade: ")
        if variedade.strip():
            break
        print("Erro: A variedade não pode ser vazia. Tente novamente.")

    while True:
        try:
            altitude = int(input("Altitude (em metros): "))
            if altitude >= 0:
                break
        except ValueError:
            print("Erro: Entrada inválida. Por favor, insira um número inteiro positivo.")
        if altitude < 0:
            print("Erro: Entrada não pode ser negativa. Por favor, insira um número inteiro positivo.")

    while True:
        moagem = input("Moagem: ")
        if moagem.strip():
            break
        print("Erro: A moagem não pode ser vazia. Tente novamente.")

    while True:
        notas_sensoriais = input("Notas Sensoriais: ")
        if notas_sensoriais.strip():
            break
        print("Erro: As notas sensoriais não podem ser vazias. Tente novamente.")

    while True:
        perfil_recomendado = input("Perfil Recomendado: ")
        if perfil_recomendado.strip():
            break
        print("Erro: O perfil recomendado não pode ser vazio. Tente novamente.")
    
    print("---------------------------------")
    
    return {
        "nome": nome,
        "preco_compra": preco_compra,
        "preco_venda": preco_venda,
        "id": id_cafe,
        "data_fabricacao": data_fabricacao,
        "origem": origem,
        "variedade": variedade,
        "altitude": altitude,
        "moagem": moagem,
        "notas_sensoriais": notas_sensoriais,
        "perfil_recomendado": perfil_recomendado,
    }

  def mostra_cafe(self, dados_cafe):
    print("NOME DO CAFÉ: ", dados_cafe["nome"])
    print("PREÇO DE COMPRA: ", dados_cafe["preco_compra"])
    print("PREÇO DE VENDA: ", dados_cafe["preco_venda"])
    print("ID: ", dados_cafe["id"])
    print("DATA DE FABRICAÇÃO: ", dados_cafe["data_fabricacao"])
    print("ORIGEM: ", dados_cafe["origem"])
    print("VARIEDADE: ", dados_cafe["variedade"])
    print("ALTITUDE: ", dados_cafe["altitude"])
    print("MOAGEM: ", dados_cafe["moagem"])
    print("NOTAS SENSORIAIS: ", dados_cafe["notas_sensoriais"])
    print("PERFIL RECOMENDADO: ", dados_cafe["perfil_recomendado"])
    print("\n")

  def seleciona_cafe(self):
    try:
      id = int(input("ID do café que deseja selecionar: "))
      return id
    except ValueError:
      self.mostra_mensagem("Erro: ID inválido. Por favor, insira um número inteiro.")
      return None

  def mostra_mensagem(self, msg):
    print(msg)
