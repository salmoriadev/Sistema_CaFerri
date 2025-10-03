class TelaEstoque:
    def tela_opcoes(self):
        print("\n-------- Estoque ----------")
        print("1 - Listar Inventário")
        print("2 - Adicionar Novo Produto ao Estoque")
        print("3 - Repor Estoque de um Produto")
        print("4 - Dar Baixa Manual de um Produto")
        print("0 - Retornar")
        
        try:
            opcao = int(input("Escolha a opção: "))
            return opcao
        except ValueError:
            self.mostra_mensagem("Entrada inválida! Digite um número.")
            return None

    def pega_dados_produto_estoque(self):
        print("\n---- Dados do Produto no Estoque ----")
        try:
            id_produto = int(input("ID do Produto: "))
            quantidade = int(input("Quantidade: "))
            if quantidade < 0:
                self.mostra_mensagem("Quantidade não pode ser negativa.")
                return None
            return {"id_produto": id_produto, "quantidade": quantidade}
        except ValueError:
            self.mostra_mensagem("Entrada inválida! IDs e quantidade devem ser números.")
            return None

    def mostra_estoque(self, dados_estoque: dict):
        print("\n---------- INVENTÁRIO ATUAL ----------")
        if not dados_estoque:
            print("O estoque está vazio.")
        else:
            for produto, quantidade in dados_estoque.items():
                print(f"-> PRODUTO: {produto.nome} (ID: {produto.id}) | QUANTIDADE: {quantidade}")
        print("------------------------------------")

    def mostra_mensagem(self, msg: str):
        print(msg)