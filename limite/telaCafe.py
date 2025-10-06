from datetime import datetime
from entidade.perfil_consumidor import PerfilConsumidor

class TelaCafe:
    def tela_opcoes(self) -> int:
        print("\n-------- Cafés ----------")
        print("1 - Adicionar Café")
        print("2 - Alterar Café")
        print("3 - Listar Cafés")
        print("4 - Excluir Café")
        print("0 - Retornar")
        
        while True:
            try:
                opcao = int(input("Escolha a opção: "))
                return opcao
            except ValueError:
                self.mostra_mensagem("Erro: Por favor, digite um número inteiro válido.")

    def pega_dados_cafe(self, is_alteracao: bool = False) -> dict:
        print("\n-------- DADOS DO CAFÉ ----------")

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

        id_cafe = None
        if not is_alteracao:
            while True:
                try:
                    id_cafe = int(input("ID: "))
                    if id_cafe >= 0:
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
            origem = input("Origem: ")
            if origem.strip():
                break
            self.mostra_mensagem("Erro: A origem não pode ser vazia.")

        while True:
            variedade = input("Variedade: ")
            if variedade.strip():
                break
            self.mostra_mensagem("Erro: A variedade não pode ser vazia.")

        while True:
            try:
                altitude = int(input("Altitude (em metros): "))
                if altitude >= 0:
                    break
                self.mostra_mensagem("Erro: A altitude não pode ser negativa.")
            except ValueError:
                self.mostra_mensagem("Erro: Entrada inválida para altitude.")

        while True:
            moagem = input("Moagem: ")
            if moagem.strip():
                break
            self.mostra_mensagem("Erro: A moagem не pode ser vazia.")

        while True:
            notas_sensoriais = input("Notas Sensoriais: ")
            if notas_sensoriais.strip():
                break
            self.mostra_mensagem("Erro: As notas sensoriais não podem ser vazias.")

        perfis = PerfilConsumidor("Doce e Suave").possiveis_perfis
        print("--- Perfis de Café Disponíveis ---")
        for i, p in enumerate(perfis, 1):
            print(f"{i} - {p}")
        
        while True:
            try:
                escolha = int(input("Escolha o número do perfil recomendado: "))
                if 1 <= escolha <= len(perfis):
                    perfil_recomendado = perfis[escolha - 1]
                    break
                self.mostra_mensagem("Erro: Número de perfil inválido.")
            except ValueError:
                self.mostra_mensagem("Erro: Por favor, digite um número.")

        while True:
            cnpj = input("Digite o CNPJ da empresa fornecedora: ")
            if cnpj.strip():
                cnpj_empresa_fornecedora = cnpj
                break

        print("---------------------------------")
        
        dados = {
            "nome": nome, "preco_compra": preco_compra, "preco_venda": preco_venda,
            "data_fabricacao": data_fabricacao, "origem": origem,
            "variedade": variedade, "altitude": altitude, "moagem": moagem,
            "notas_sensoriais": notas_sensoriais, "perfil_recomendado": perfil_recomendado,
            "empresa_fornecedora": cnpj_empresa_fornecedora
        }

        if id_cafe is not None:
            dados["id"] = id_cafe
        
        return dados

    def mostra_cafe(self, dados_cafe: dict) -> None:
        print("---------------------------------")
        print(f"ID: {dados_cafe['id']}")
        print(f"NOME: {dados_cafe['nome']}")
        print(f"PREÇO VENDA: R$ {dados_cafe['preco_venda']:.2f}")
        print(f"PERFIL: {dados_cafe['perfil_recomendado']}")
        print(f"FORNECEDORA: {dados_cafe['empresa_fornecedora_nome']}")
        print("---------------------------------")


    def seleciona_cafe(self) -> int:
        while True:
            try:
                id_cafe = int(input("ID do café que deseja selecionar: "))
                return id_cafe
            except ValueError:
                self.mostra_mensagem("Erro: ID inválido. Por favor, insira um número inteiro.")

    def mostra_mensagem(self, msg: str) -> None:
        print(msg)
