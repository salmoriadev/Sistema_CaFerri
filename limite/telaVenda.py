class TelaVenda:

    def tela_opcoes(self) -> int:
        print("\n-------- Vendas ----------")
        print("1 - Iniciar Nova Venda")
        print("2 - Listar Vendas")
        print("3 - Excluir Venda (Cancelar)")
        print("0 - Retornar")

        try:
            opcao = int(input("Escolha a opção: "))
            return opcao
        except ValueError:
            self.mostra_mensagem("Entrada inválida! Digite um número.")
            return None

    def tela_opcoes_gerenciar_venda(self) -> int:
        print("\n--- Gerenciando Venda ---")
        print("1 - Adicionar Produto")
        print("2 - Remover Produto")
        print("3 - Listar Produtos no Carrinho")
        print("4 - Finalizar Venda")
        print("0 - Salvar e Sair")

        try:
            opcao = int(input("Escolha a opção: "))
            return opcao
        except ValueError:
            self.mostra_mensagem("Entrada inválida! Digite um número.")
            return None

    def pega_dados_iniciar_venda(self) -> dict:
        print("---- Iniciando Nova Venda ----")
        try:
            id_venda = int(input("ID da Venda: "))
            id_cliente = int(input("ID do Cliente: "))
            return {"id_venda": id_venda, "id_cliente": id_cliente}
        except ValueError:
            self.mostra_mensagem("Entrada inválida! IDs devem ser números.")
            return None

    def pega_dados_produto(self) -> dict:
        print("---- Adicionar/Remover Produto ----")
        try:
            id_produto = int(input("ID do Produto: "))
            try:
                quantidade = int(input("Quantidade: "))
            except ValueError:
                quantidade = 1 
            return {"id_produto": id_produto, "quantidade": quantidade}
        except ValueError:
            self.mostra_mensagem("Entrada inválida! ID deve ser um número.")
            return None

    def mostra_venda(self, dados_venda: dict) -> None:
        print("------------------------------")
        print(f"ID da Venda: {dados_venda['id_venda']}")
        print(f"Cliente: {dados_venda['cliente_nome']}")
        print(f"Valor Total: R$ {dados_venda['valor_total']:.2f}")
        print(f"Status: {dados_venda['status']}")
        print("Produtos:")
        if dados_venda['produtos']:
            for produto_dict in dados_venda['produtos']:
                print(f"  - {produto_dict['nome']}: ({produto_dict['quantidade']} x {produto_dict['preco_unitario']}) = {produto_dict['subtotal']}")
        else:
            print("  (Carrinho vazio)")
        print("------------------------------")

    def seleciona_venda(self) -> int:
        try:
            id_venda = int(input("Digite o ID da venda que deseja selecionar: "))
            return id_venda
        except ValueError:
            self.mostra_mensagem("Entrada inválida! ID deve ser um número.")
            return None

    def mostra_mensagem(self, msg: str):
        print(msg)