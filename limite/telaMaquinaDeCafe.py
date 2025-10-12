from datetime import datetime

class TelaMaquinaCafe:
    def tela_opcoes(self) -> int:
        print("\n-------- Máquinas de Café ----------")
        print("1 - Adicionar Máquina")
        print("2 - Alterar Máquina")
        print("3 - Listar Máquinas")
        print("4 - Excluir Máquina")
        print("0 - Retornar")

        
        while True:
            try:
                opcao = int(input("Escolha a opção: "))
                return opcao
            except ValueError:
                self.mostra_mensagem("Erro: Por favor, digite um número inteiro válido.")

    def pega_dados_maquina(self, is_alteracao: bool = False) -> dict:
        print("\n-------- DADOS DA MÁQUINA DE CAFÉ ----------")

        while True:
            nome = input("Nome: ")
            if nome.strip():
                break
            self.mostra_mensagem("Erro: Nome inválido.")

        while True:
            try:
                preco_compra = float(input("Preço de Compra: R$ "))
                if preco_compra >= 0:
                    break
                self.mostra_mensagem("Erro: O preço não pode ser negativo.")
            except ValueError:
                self.mostra_mensagem("Erro: Entrada inválida para preço.")

        while True:
            try:
                preco_venda = float(input("Preço de Venda: R$ "))
                if preco_venda >= 0:
                    break
                self.mostra_mensagem("Erro: O preço não pode ser negativo.")
            except ValueError:
                self.mostra_mensagem("Erro: Entrada inválida para preço.")

        id_maquina = None
        if not is_alteracao:
            while True:
                try:
                    id_maquina = int(input("ID: "))
                    if id_maquina >= 0:
                        break
                    self.mostra_mensagem("Erro: O ID não pode ser negativo.")
                except ValueError:
                    self.mostra_mensagem("Erro: Entrada inválida para ID.")

        while True:
            data_fabricacao = input("Data de Fabricação (DD/MM/AAAA): ")
            try:
                datetime.strptime(data_fabricacao, '%d/%m/%Y')
                break
            except ValueError:
                self.mostra_mensagem("Erro: Formato de data inválido.")

        while True:
            cnpj = input("Digite o CNPJ da empresa fornecedora: ")
            if cnpj.strip():
                cnpj_empresa_fornecedora = cnpj
                break

        print("------------------------------------------")

        dados = {
            "nome": nome,
            "preco_compra": preco_compra,
            "preco_venda": preco_venda,
            "data_fabricacao": data_fabricacao,
            "empresa_fornecedora": cnpj_empresa_fornecedora
        }

        if id_maquina is not None:
            dados["id"] = id_maquina
        
        return dados

    def mostra_maquina(self, dados_maquina: dict) -> None:
        print("---------------------------------")
        print(f"ID: {dados_maquina['id']}")
        print(f"NOME: {dados_maquina['nome']}")
        print(f"PREÇO VENDA: R$ {dados_maquina['preco_venda']:.2f}")
        print(f"FORNECEDORA: {dados_maquina['empresa_fornecedora_nome']}")
        print("---------------------------------")


    def seleciona_maquina(self) -> int:
        while True:
            try:
                id_maquina = int(input("ID da máquina que deseja selecionar: "))
                return id_maquina
            except ValueError:
                self.mostra_mensagem("Erro: ID inválido. Por favor, insira um número inteiro.")

    def mostra_mensagem(self, msg: str) -> None:
        print(msg)
