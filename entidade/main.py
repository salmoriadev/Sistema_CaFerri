from cafe import Cafe
from cliente import Cliente
from estoque import Estoque
from fornecedora_cafe import FornecedoraCafe
from fornecedora_maquina import FornecedoraMaquina
from maquina_de_cafe import MaquinaDeCafe
from perfil_consumidor import PerfilConsumidor
from venda import Venda

def linha_separadora():
    print("=" * 60)

def demonstrar_perfis_consumidor():
    print("TESTE: PERFIS DE CONSUMIDOR")
    linha_separadora()
    
    perfil_doce_suave = PerfilConsumidor("Doce e Suave")
    perfil_acido_e_frutado = PerfilConsumidor("Ácido e Frutado")
    perfil_intenso_e_encorpado = PerfilConsumidor("Intenso e Encorpado")
    
    print(f"Perfil Doce e Suave - Recomendações: {perfil_doce_suave.recomendar_cafes()}")
    print(f"Perfil Ácido e Frutado - Recomendações: {perfil_acido_e_frutado.recomendar_cafes()}")
    print(f"Perfil Intenso e Encorpado - Recomendações: {perfil_intenso_e_encorpado.recomendar_cafes()}")

    return perfil_doce_suave, perfil_acido_e_frutado, perfil_intenso_e_encorpado

def demonstrar_fornecedores():
    print("\nTESTE: FORNECEDORES")
    linha_separadora()
    
    fornecedor_cafe = FornecedoraCafe(
        "Fazenda Ferri", 
        "12.345.678/0001-90", 
        "Rua do Café, 123", 
        "(11) 9999-8888",
        "Arábica Premium"
    )
    
    fornecedor_maquina = FornecedoraMaquina(
        "DevCafe Ltda", 
        "98.765.432/0001-10", 
        "Av. Industrial, 456", 
        "(11) 8888-9999",
        "Itália"
    )
    
    print(f"Fornecedor de Café: {fornecedor_cafe.nome} - Tipo: {fornecedor_cafe.tipo_cafe}")
    print(f"Fornecedor de Máquinas: {fornecedor_maquina.nome} - País: {fornecedor_maquina.pais_de_origem}")
    
    return fornecedor_cafe, fornecedor_maquina

def demonstrar_produtos(perfil_doce_suave, perfil_acido_e_frutado):
    print("\nTESTE: PRODUTOS")
    linha_separadora()
    
    cafe1 = Cafe(
        "Café Especial da Montanha", 50.0, 80.0, 100, 1, "2024-01-15",
        "Brasil - Minas Gerais", "Bourbon Amarelo", 1200, "Moído Médio",
        "Notas de chocolate e caramelo", perfil_doce_suave
    )
    
    cafe2 = Cafe(
        "Café Gourmet Single Origin", 80.0, 120.0, 50, 2, "2024-02-10",
        "Colômbia", "Geisha", 1800, "Grãos Inteiros",
        "Notas florais e cítricas", perfil_acido_e_frutado
    )
    
    maquina1 = MaquinaDeCafe(
        "Máquina Espresso Professional", 1500.0, 2500.0, 10, 3, "2024-01-20",
        "EP-Pro 3000"
    )
    
    print("CAFÉS CADASTRADOS:")
    print(f"1. {cafe1.exibir_informacoes()}")
    print(f"\n2. {cafe2.exibir_informacoes()}")
    
    print(f"\nMÁQUINA CADASTRADA:")
    print(f"Nome: {maquina1.nome}, Modelo: {maquina1.modelo}")
    print(f"Preço: R$ {maquina1.preco_venda}, Lucro: R$ {maquina1.calcular_lucro()}")
    
    return cafe1, cafe2, maquina1

def demonstrar_estoque(cafe1, cafe2, maquina1):
    print("\nTESTE: ESTOQUE")
    linha_separadora()
    
    estoque = Estoque()
    
    estoque.adicionar_produto(cafe1, 50)
    estoque.adicionar_produto(cafe2, 30)
    estoque.adicionar_produto(maquina1, 5)
    
    print("PRODUTOS EM ESTOQUE:")
    produtos_estoque = estoque.listar_produtos()
    for produto, quantidade in produtos_estoque.items():
        print(f"- {produto.nome}: {quantidade} unidades")
    
    print(f"\nCafés disponíveis: {len(estoque.cafes)} tipos")
    
    return estoque

def demonstrar_clientes(perfil_doce_suave, perfil_acido_e_frutado):
    print("\nTESTE: CLIENTES")
    linha_separadora()
    
    cliente1 = Cliente(1, "João Silva", "joao@email.com", "senha123", 500.0, "Doce e Suave")
    cliente2 = Cliente(2, "Maria Santos", "maria@email.com", "senha456", 800.0, "Ácido e Frutado")
    
    print("CLIENTES CADASTRADOS:")
    print(f"1. {cliente1.exibir_informacoes()}")
    print(f"\n2. {cliente2.exibir_informacoes()}")
    
    print(f"\nTeste de senha João (senha123): {cliente1.pedir_senha('senha123')}")
    print(f"Teste de senha João (senhaerrada): {cliente1.pedir_senha('senhaerrada')}")
    
    print(f"\nRecomendações para {cliente1.nome}: {cliente1.mostrar_recomendacoes()}")
    print(f"Recomendações para {cliente2.nome}: {cliente2.mostrar_recomendacoes()}")
    
    return cliente1, cliente2

def demonstrar_vendas(cliente1, cafe1, cafe2, estoque):
    print("\nTESTE: VENDAS")
    linha_separadora()
    
    print(f"Saldo inicial do cliente {cliente1.nome}: R$ {cliente1.saldo}")
    
    venda1 = Venda(1, cliente1, cafe1)
    print(f"Venda criada - Valor inicial: R$ {venda1.valor_total}")
    
    venda1.adicionar_produto(cafe2, 2)
    print(f"Após adicionar 2x {cafe2.nome}: R$ {venda1.valor_total}")
    
    print(f"Produtos na venda: {len(venda1.listar_produtos())} itens")
    
    resultado = venda1.finalizar_venda(estoque)
    print(f"Resultado da venda: {resultado}")
    
    if venda1.status_venda == "Finalizada":
        print(f"Saldo final do cliente: R$ {cliente1.saldo}")
        print(f"Data da venda: {venda1.data_venda}")
        
        print(f"\nEstoque após a venda:")
        produtos_estoque = estoque.listar_produtos()
        for produto, quantidade in produtos_estoque.items():
            if produto.nome in [cafe1.nome, cafe2.nome]:
                print(f"- {produto.nome}: {quantidade} unidades restantes")
    
    return venda1

def demonstrar_operacoes_avancadas(cliente1, perfil_intenso):
    print("\nTESTE: OPERAÇÕES AVANÇADAS")
    linha_separadora()
    
    print("Testando alteração de senha...")
    resultado_senha = cliente1.alterar_senha("senha123", "novaSenha789")
    print(f"Alteração de senha: {'Sucesso' if resultado_senha else 'Falha'}")
    
    print(f"Teste com nova senha: {cliente1.pedir_senha('novaSenha789')}")
    
    print(f"\nPerfil atual: {cliente1.perfil_do_consumidor.perfil}")
    cliente1.perfil_do_consumidor = perfil_intenso
    print(f"Novo perfil: {cliente1.perfil_do_consumidor.perfil}")
    print(f"Novas recomendações: {cliente1.mostrar_recomendacoes()}")

def menu_interativo():
    print("\nMENU INTERATIVO")
    linha_separadora()
    
    opcoes = {
        "1": "Exibir todos os perfis de consumidor",
        "2": "Exibir fornecedores",
        "3": "Exibir produtos",
        "4": "Exibir estoque",
        "5": "Exibir clientes",
        "6": "Simular venda",
        "7": "Operações avançadas",
        "8": "Sair"
    }
    
    print("OPÇÕES DISPONÍVEIS:")
    for key, value in opcoes.items():
        print(f"{key}. {value}")
    
    opcao = input("\nEscolha uma opção (1-8): ").strip()
    return opcao


def main():
    print("SISTEMA DO CAFERRI")
    linha_separadora()
    
    perfil_doce_suave, perfil_acido_e_frutado, perfil_intenso = demonstrar_perfis_consumidor()
    fornecedor_cafe, fornecedor_maquina = demonstrar_fornecedores()
    cafe1, cafe2, maquina1 = demonstrar_produtos(perfil_doce_suave, perfil_acido_e_frutado)
    estoque = demonstrar_estoque(cafe1, cafe2, maquina1)
    cliente1, cliente2 = demonstrar_clientes(perfil_doce_suave, perfil_acido_e_frutado)
    
    while True:
        opcao = menu_interativo()
        
        if opcao == "1":
            demonstrar_perfis_consumidor()
        elif opcao == "2":
            demonstrar_fornecedores()
        elif opcao == "3":
            demonstrar_produtos(perfil_doce_suave, perfil_acido_e_frutado)
        elif opcao == "4":
            demonstrar_estoque(cafe1, cafe2, maquina1)
        elif opcao == "5":
            demonstrar_clientes(perfil_doce_suave, perfil_acido_e_frutado)
        elif opcao == "6":
            novo_cliente = Cliente(3, "Pedro Costa", "pedro@email.com", "123", 300.0, "Doce e Suave")
            nova_venda = Venda(2, novo_cliente, cafe1)
            resultado = nova_venda.finalizar_venda(estoque)
            print(f"Nova venda: {resultado}")
        elif opcao == "7":
            demonstrar_operacoes_avancadas(cliente2, perfil_intenso)
        elif opcao == "8":
            print("Obrigado por usar o sistema!")
            break
        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    main()