class TelaSistema:
    def tela_opcoes(self) -> None:
        print("-------- Caferri ---------")
        print("Escolha sua opcao")
        print("1 - Fornecedores de cafés")
        print("2 - Fornecedores de máquinas de cafés")
        print("3 - Clientes")
        print("4 - Cafés")
        print("5 - Máquinas de cafés")
        print("6 - Estoque")
        print("7 - Vendas")
        print("8 - Gerar Relatório")
        print("0 - Finalizar sistema")

        try:
            opcao = int(input("Escolha a opcao: "))
            return opcao
        except ValueError:
            print("\nEntrada inválida! Por favor, digite apenas um número.")
            return None
    
    def mostra_mensagem(self, msg: str) -> None:
        print(msg)