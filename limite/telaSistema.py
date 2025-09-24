class TelaSistema:
    #fazer aqui tratamento dos dados, caso a entrada seja diferente do esperado
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
        opcao = int(input("Escolha a opcao:"))
        return opcao