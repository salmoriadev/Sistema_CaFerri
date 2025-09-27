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
        print("\n-------- DADOS DO CLIENTE ----------")

        while True:
            try:
                id_cliente = int(input("ID: "))
                if id_cliente >= 0:
                    break
                print("Erro: O ID não pode ser um número negativo. Tente novamente.")
            except ValueError:
                print("Erro: Entrada inválida. Por favor, insira um número inteiro.")

        while True:
            nome = input("Nome: ")
            if nome.strip():
                break
            print("Erro: Nome inválido. Tente novamente.")

        while True:
            email = input("Email: ")
            if email.strip() and '@' in email and '.' in email:
                break
            print("Erro: Email inválido. Tente novamente.")

        while True:
            senha = input("Senha: ")
            if senha:
                break
            print("Erro: A senha não pode ser vazia. Tente novamente.")

        while True:
            try:
                saldo = float(input("Saldo: "))
                if saldo >= 0:
                    break
                print("Erro: O saldo não pode ser negativo. Tente novamente.")
            except ValueError:
                print("Erro: Entrada inválida. Por favor, insira um número (ex: 150.75).")

        while True:
            perfil = input("Perfil do Consumidor: ")
            if perfil.strip():
                break
            print("Erro: O perfil do consumidor não pode ser vazio. Tente novamente.")
        
        print("------------------------------------")
        
        return {
            "id": id_cliente,
            "nome": nome,
            "email": email,
            "senha": senha,
            "saldo": saldo,
            "perfil": perfil
        }

    
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
        
    def pedir_senha(self):
        senha = input("Digite sua senha: ")
        return senha
