"""
    Gerencia a interface com o usuário para a geração e exibição de
    todos os relatórios do sistema.

    Atuando como a camada de apresentação (View) para o módulo de relatórios,
    esta classe é responsável por interagir com o usuário para determinar
    qual relatório deve ser gerado."""


class TelaRelatorio:
    def tela_opcoes(self) -> int:
        print("\n---------- RELATÓRIOS ----------")
        print("[1] -> Relatório de Vendas Finalizadas")
        print("[2] -> Relatório de Clientes por Valor Gasto")
        print("[3] -> Relatório de Estoque Baixo")
        print("[4] -> Relatório de Cafés Mais Vendidos")
        print("[5] -> Relatório de Máquinas Mais Vendidas")
        print("[6] -> Relatório de Empresas Fornecedoras Mais Ativas")
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