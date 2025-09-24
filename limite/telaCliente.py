class TelaCliente:
    def tela_opcoes(self):
        print("\n-------- Clientes ----------")
        print("Escolha a opção")
        print("1 - Incluir Cliente")
        print("2 - Alterar Cliente")
        print("3 - Listar Clientes")
        print("4 - Excluir Cliente")
        print("0 - Retornar")
        
        try:
            opcao = int(input("Escolha a opção: "))
            return opcao
        except ValueError:
            print("Entrada inválida! Digite um número.")
            return None

    
    def pega_dados_cliente(self):
        print("-------- DADOS DO CLIENTE ----------")
        id = int(input("ID: "))
        nome = input("Nome: ")
        email = input("Email: ")
        senha = input("Senha: ")
        saldo = float(input("Saldo: "))
        perfil = input("Perfil do Consumidor: ")

        return {"id": id, "nome": nome, "email": email, "senha": senha, "saldo": saldo, "perfil": perfil}

    
    def mostra_cliente(self, dados_cliente):
        print("--------------------------------")
        print("ID DO CLIENTE: ", dados_cliente["id"])
        print("NOME: ", dados_cliente["nome"])
        print("EMAIL: ", dados_cliente["email"])
        print("SALDO: R$", dados_cliente["saldo"])
        print("PERFIL: ", dados_cliente["perfil"])
        print("--------------------------------")

    
    def seleciona_cliente(self) -> int:
        try:
            id = int(input("ID do cliente que deseja selecionar: "))
            return id
        except ValueError:
            print("Entrada inválida! Digite um número.")
            return None

    def mostra_mensagem(self, msg: str):
        print(msg)
