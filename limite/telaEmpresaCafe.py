"""Gerencia a interface com o usuário para todas as operações relacionadas
    aos Fornecedores de Café.

    Esta classe atua como a camada de apresentação (View) dedicada à entidade
    `FornecedoraCafe`. Sua função é ser a ponte entre o usuário e o sistema,
    sendo responsável por toda a interação via console para este módulo.
"""


class TelaEmpresaCafe:
    def tela_opcoes(self) -> int:
        print("\n-------- Fornecedores de Café ----------")
        print("1 - Adicionar Fornecedor")
        print("2 - Alterar Fornecedor")
        print("3 - Listar Fornecedores")
        print("4 - Excluir Fornecedor")
        print("0 - Retornar")
        
        while True:
            try:
                opcao = int(input("Escolha a opção: "))
                return opcao
            except ValueError:
                self.mostra_mensagem("Erro: Por favor, digite um número inteiro válido.")

    def pega_dados_empresa_cafe(self, is_alteracao: bool = False) -> dict:
        print("\n-------- DADOS DO FORNECEDOR DE CAFÉ ----------")

        while True:
            nome = input("Nome: ")
            if nome.strip():
                break
            self.mostra_mensagem("Erro: O nome не pode ser vazio.")
        
        cnpj = None
        if not is_alteracao:
            while True:
                cnpj = input("CNPJ: ")
                if cnpj.strip():
                    break
                self.mostra_mensagem("Erro: O CNPJ não pode ser vazio.")

        while True:
            endereco = input("Endereço: ")
            if endereco.strip():
                break
            self.mostra_mensagem("Erro: O endereço não pode ser vazio.")

        while True:
            telefone = input("Telefone: ")
            if telefone.strip():
                break
            self.mostra_mensagem("Erro: O telefone não pode ser vazio.")

        while True:
            tipo_cafe = input("Tipo de Café (ex: Arábica, Robusta): ")
            if tipo_cafe.strip():
                break
            self.mostra_mensagem("Erro: O tipo de café não pode ser vazio.")
        
        print("---------------------------------------------")
        
        dados = {
            "nome": nome,
            "endereco": endereco,
            "telefone": telefone,
            "tipo_cafe": tipo_cafe
        }
        if cnpj is not None:
            dados["cnpj"] = cnpj
        
        return dados

    def mostra_empresa_cafe(self, dados_empresa: dict) -> None:
        print("---------------------------------")
        print(f"NOME: {dados_empresa['nome']}")
        print(f"CNPJ: {dados_empresa['cnpj']}")
        print(f"TIPO DE CAFÉ: {dados_empresa['tipo_cafe']}")
        print("---------------------------------")

    def seleciona_empresa_cafe(self) -> str:
        """Pede o CNPJ da empresa para selecioná-la."""
        while True:
            cnpj = input("CNPJ do fornecedor que deseja selecionar: ")
            if cnpj.strip():
                return cnpj
            self.mostra_mensagem("Erro: O CNPJ não pode ser vazio.")

    def mostra_mensagem(self, msg: str) -> None:
        print(msg)