"""
    Gerencia a interface principal do sistema, atuando como o ponto de
    entrada para o usuário.

    Esta classe é a camada de apresentação (View) do `ControladorSistema`
    e sua responsabilidade primária é exibir o menu principal, que serve
    como um portal de navegação para todas as outras funcionalidades do
    sistema, como o gerenciamento de clientes, produtos, estoque e vendas.

    Ela é responsável por:
    - Apresentar as opções de alto nível ao usuário.
    - Capturar a opção selecionada, incluindo um tratamento de erro para
      garantir que a entrada seja um número inteiro válido.
    - Fornecer um método padronizado (`mostra_mensagem`) para que o
      controlador principal possa exibir mensagens de feedback, como
      avisos ou erros, de forma consistente.
    """

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