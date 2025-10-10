class TelaRelatorio:
    def tela_opcoes(self) -> int:
        print("\n---------- RELATÓRIOS ----------")
        print("[1] -> Relatório de Vendas Finalizadas")
        print("[2] -> Relatório de Clientes por Valor Gasto")
        print("[3] -> Relatório de Estoque Baixo")
        print("[0] -> Retornar ao Menu Principal")
        print("---------------------------------")

        while True:
            try:
                opcao = int(input("Escolha uma opção: "))
                return opcao
            except ValueError:
                print("ERRO: Por favor, digite um número válido.")

    def mostra_relatorio(self, titulo: str, linhas_relatorio: list):
        print(f"\n---------- {titulo.upper()} ----------")
        if not linhas_relatorio:
            print("Nenhum dado para exibir.")
        else:
            for linha in linhas_relatorio:
                print(linha)
        print("----------------------------------------")

    def mostra_mensagem(self, msg: str):
        print(msg)