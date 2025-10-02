class TelaSistema:
    def tela_opcoes(self):
        print("-------- Caferri ---------")
        print("Escolha sua opcao")
        print("1 - Cafés")
        print("2 - Maquinas de Cafés")
        print("3 - Clientes")
        print("4 - Estoque")
        print("5 - Vendas")
        print("6 - Fornecedores de cafés")
        print("7 - Fornecedores de máquinas de cafés")
        print("0 - Finalizar sistema")

        try:
            opcao = int(input("Escolha a opcao: "))
            return opcao
        except ValueError:
            print("\nEntrada inválida! Por favor, digite apenas um número.")
            return None
    
    def mostra_mensagem(self, msg: str):
        print(msg)