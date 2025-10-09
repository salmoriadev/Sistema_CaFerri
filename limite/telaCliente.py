import getpass
from entidade.perfil_consumidor import PerfilConsumidor

class TelaCliente:
    def tela_opcoes(self) -> int:
        print("\n-------- Clientes ----------")
        print("1 - Incluir Cliente")
        print("2 - Alterar Cliente")
        print("3 - Listar Clientes")
        print("4 - Excluir Cliente")
        print("5 - Ver Recomendações de Café")
        print("0 - Retornar")
        while True:
            try:
                opcao = int(input("Escolha a opção: "))
                return opcao
            except ValueError:
                self.mostra_mensagem("Erro: Entrada inválida. Por favor, digite um número inteiro.")

    def pega_dados_cliente(self, is_alteracao: bool = False) -> dict:
        print("\n-------- DADOS DO CLIENTE ----------")
        
        if not is_alteracao:
            while True:
                try:
                    id_cliente = int(input("ID: "))
                    if id_cliente >= 0:
                        break
                    self.mostra_mensagem("Erro: O ID não pode ser um número negativo.")
                except ValueError:
                    self.mostra_mensagem("Erro: Entrada inválida para ID.")

        while True:
            nome = input("Nome: ")
            if nome.strip():
                break
            self.mostra_mensagem("Erro: Nome inválido.")

        while True:
            email = input("Email: ")
            if email.strip() and '@' in email and '.' in email:
                break
            self.mostra_mensagem("Erro: Email inválido.")

        senha = None
        if is_alteracao:
            alterar_senha = input("Deseja alterar a senha? (s/n): ").lower()
            if alterar_senha == 's':
                while True:
                    senha = input("Nova Senha: ")
                    if senha:
                        break
                    self.mostra_mensagem("Erro: A senha não pode ser vazia.")
        else:
            while True:
                senha = input("Senha: ")
                if senha:
                    break
                self.mostra_mensagem("Erro: A senha não pode ser vazia.")
        while True:
            try:
                saldo = float(input("Saldo: R$ "))
                if saldo >= 0:
                    break
                self.mostra_mensagem("Erro: O saldo não pode ser negativo.")
            except ValueError:
                self.mostra_mensagem("Erro: Entrada inválida para saldo.")

        perfis_disponiveis = PerfilConsumidor("Doce e Suave").possiveis_perfis
        print("--- Perfis de Consumidor Disponíveis ---")
        for i, p in enumerate(perfis_disponiveis, 1):
            print(f"{i} - {p}")
        
        while True:
            try:
                escolha = int(input("Escolha o número do perfil: "))
                if 1 <= escolha <= len(perfis_disponiveis):
                    perfil_selecionado = perfis_disponiveis[escolha - 1]
                    break
                self.mostra_mensagem("Erro: Número de perfil inválido.")
            except ValueError:
                self.mostra_mensagem("Erro: Por favor, digite um número.")
        
        print("------------------------------------")
        
        if is_alteracao:
            dados = {
                "nome": nome, "email": email, "saldo": saldo, "perfil": perfil_selecionado
            }
            if senha:
                dados["senha"] = senha
            return dados
        else:
            return {
                "id": id_cliente,
                "nome": nome,
                "email": email,
                "senha": senha,
                "saldo": saldo,
                "perfil": perfil_selecionado
            }

    def mostra_cliente(self, dados_cliente: dict) -> None:
        print("--------------------------------")
        print("ID DO CLIENTE: ", dados_cliente["id"])
        print("NOME: ", dados_cliente["nome"])
        print("EMAIL: ", dados_cliente["email"])
        print(f"SALDO: R$ {dados_cliente['saldo']:.2f}")
        print("PERFIL: ", dados_cliente["perfil"])
        print("--------------------------------")

    def seleciona_cliente(self) -> int:
        while True:
            try:
                id_cliente = int(input("ID do cliente que deseja selecionar: "))
                return id_cliente
            except ValueError:
                self.mostra_mensagem("Erro: Entrada inválida. Por favor, digite um número inteiro.")

    def mostra_mensagem(self, msg: str) -> None:
        print(msg)
        
    def pedir_senha(self) -> str:
        return getpass.getpass("Digite sua senha: ")
