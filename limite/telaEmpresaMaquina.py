""" Gerencia a interface com o usuário para todas as operações relacionadas
    aos Fornecedores de Máquinas.

    Esta classe atua como a camada de apresentação (View) dedicada à entidade
    `FornecedoraMaquina. Sua função é ser a ponte entre o usuário e o sistema,
    sendo responsável por toda a interação via console para este módulo.
"""


class TelaEmpresaMaquina:
    def tela_opcoes(self) -> int:
        print("\n-------- Fornecedores de Máquinas ----------")
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

    def pega_dados_empresa_maquina(self, is_alteracao: bool = False) -> dict:
        print("\n-------- DADOS DO FORNECEDOR DE MÁQUINAS ----------")

        while True:
            nome = input("Nome: ")
            if nome.strip():
                break
            self.mostra_mensagem("Erro: O nome não pode ser vazio.")
        
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
            self.mostra_mensagem("Erro: O endereço не pode ser vazio.")

        while True:
            telefone = input("Telefone: ")
            if telefone.strip():
                break
            self.mostra_mensagem("Erro: O telefone não pode ser vazio.")

        while True:
            pais_de_origem = input("País de Origem da Marca: ")
            if pais_de_origem.strip():
                break
            self.mostra_mensagem("Erro: O país de origem não pode ser vazio.")
        
        print("-------------------------------------------------")
        
        dados = {
            "nome": nome,
            "endereco": endereco,
            "telefone": telefone,
            "pais_de_origem": pais_de_origem
        }
        if cnpj is not None:
            dados["cnpj"] = cnpj
        
        return dados

    def mostra_empresa_maquina(self, dados_empresa: dict) -> None:
        print("---------------------------------")
        print(f"NOME: {dados_empresa['nome']}")
        print(f"CNPJ: {dados_empresa['cnpj']}")
        print(f"PAÍS DE ORIGEM: {dados_empresa['pais_de_origem']}")
        print("---------------------------------")

    def seleciona_empresa_maquina(self) -> str:
        """Pede o CNPJ da empresa para selecioná-la."""
        while True:
            cnpj = input("CNPJ do fornecedor que deseja selecionar: ")
            if cnpj.strip():
                return cnpj
            self.mostra_mensagem("Erro: O CNPJ não pode ser vazio.")

    def mostra_mensagem(self, msg: str) -> None:
        print(msg)