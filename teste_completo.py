"""
Arquivo de teste completo para o Sistema CaFerri.

Este script simula um fluxo completo de operações do sistema, incluindo:
- Criação de fornecedores (café e máquinas)
- Cadastro de clientes
- Cadastro de produtos (cafés e máquinas)
- Gerenciamento de estoque
- Criação e finalização de vendas
- Testes de diferentes cenários e casos de uso

Execute este arquivo para popular o sistema com dados de teste e validar
todas as funcionalidades principais.
"""

import hashlib
from entidade.fornecedora_cafe import FornecedoraCafe
from entidade.fornecedora_maquina import FornecedoraMaquina
from entidade.cliente import Cliente
from entidade.cafe import Cafe
from entidade.maquina_de_cafe import MaquinaDeCafe
from entidade.venda import Venda
from entidade.estoque import Estoque
from DAOs.fornecedora_cafe_dao import FornecedoraCafeDAO
from DAOs.fornecedora_maquina_dao import FornecedoraMaquinaDAO
from DAOs.cliente_dao import ClienteDAO
from DAOs.cafe_dao import CafeDAO
from DAOs.maquina_de_cafe_dao import MaquinaDeCafeDAO
from DAOs.venda_dao import VendaDAO
from DAOs.estoque_dao import EstoqueDAO


def cifrar_senha(senha: str) -> str:
    """Cifra uma senha usando SHA-256."""
    return hashlib.sha256(senha.encode('utf-8')).hexdigest()


def criar_fornecedores():
    """Cria fornecedores de café e máquinas para o sistema."""
    print("\n" + "="*60)
    print("CRIANDO FORNECEDORES")
    print("="*60)
    
    fornecedor_cafe_dao = FornecedoraCafeDAO()
    fornecedor_maquina_dao = FornecedoraMaquinaDAO()
    
    # Fornecedores de Café
    fornecedores_cafe = [
        FornecedoraCafe("Café do Brasil Premium", "12.345.678/0001-90", 
                       "Rua das Flores, 123, São Paulo - SP", 
                       "(11) 98765-4321", "Arábica"),
        FornecedoraCafe("Grãos Especiais Ltda", "23.456.789/0001-01",
                       "Av. Principal, 456, Minas Gerais - MG",
                       "(31) 91234-5678", "Robusta"),
        FornecedoraCafe("Café Gourmet Express", "34.567.890/0001-12",
                       "Rua Central, 789, Espírito Santo - ES",
                       "(27) 92345-6789", "Arábica"),
        FornecedoraCafe("Torrefação Artesanal", "45.678.901/0001-23",
                       "Estrada Rural, Km 5, Bahia - BA",
                       "(71) 93456-7890", "Arábica"),
        FornecedoraCafe("Café Orgânico Natural", "56.789.012/0001-34",
                       "Rodovia 101, 1000, Paraná - PR",
                       "(41) 94567-8901", "Arábica")
    ]
    
    for fornecedor in fornecedores_cafe:
        fornecedor_cafe_dao.add(fornecedor)
        print(f"[OK] Fornecedor de cafe criado: {fornecedor.nome} (CNPJ: {fornecedor.cnpj})")
    
    # Fornecedores de Máquinas
    fornecedores_maquina = [
        FornecedoraMaquina("Máquinas Expresso S.A.", "98.765.432/0001-10",
                          "Av. Industrial, 500, São Paulo - SP",
                          "(11) 97654-3210", "Brasil"),
        FornecedoraMaquina("CoffeeTech Internacional", "87.654.321/0001-21",
                          "Rua Tecnológica, 200, Campinas - SP",
                          "(19) 96543-2109", "Itália"),
        FornecedoraMaquina("Equipamentos Premium", "76.543.210/0001-32",
                          "Distrito Industrial, 300, Curitiba - PR",
                          "(41) 95432-1098", "Alemanha"),
        FornecedoraMaquina("Máquinas Profissionais", "65.432.109/0001-43",
                          "Parque Tecnológico, 150, Belo Horizonte - MG",
                          "(31) 94321-0987", "Suíça")
    ]
    
    for fornecedor in fornecedores_maquina:
        fornecedor_maquina_dao.add(fornecedor)
        print(f"[OK] Fornecedor de maquina criado: {fornecedor.nome} (CNPJ: {fornecedor.cnpj})")
    
    print(f"\nTotal: {len(fornecedores_cafe)} fornecedores de café e {len(fornecedores_maquina)} fornecedores de máquinas criados.")


def criar_clientes():
    """Cria clientes para o sistema."""
    print("\n" + "="*60)
    print("CRIANDO CLIENTES")
    print("="*60)
    
    cliente_dao = ClienteDAO()
    
    clientes = [
        Cliente(1, "João Silva", "joao.silva@email.com", cifrar_senha("senha123"), 
               5000.00, "Doce e Suave"),
        Cliente(2, "Maria Santos", "maria.santos@email.com", cifrar_senha("senha456"),
               6000.00, "Ácido e Frutado"),
        Cliente(3, "Pedro Oliveira", "pedro.oliveira@email.com", cifrar_senha("senha789"),
               4000.00, "Intenso e Encorpado"),
        Cliente(4, "Ana Costa", "ana.costa@email.com", cifrar_senha("senha012"),
               8000.00, "Doce e Suave"),
        Cliente(5, "Carlos Pereira", "carlos.pereira@email.com", cifrar_senha("senha345"),
               4500.00, "Ácido e Frutado"),
        Cliente(6, "Julia Ferreira", "julia.ferreira@email.com", cifrar_senha("senha678"),
               3500.00, "Intenso e Encorpado"),
        Cliente(7, "Roberto Alves", "roberto.alves@email.com", cifrar_senha("senha901"),
               5500.00, "Doce e Suave"),
        Cliente(8, "Fernanda Lima", "fernanda.lima@email.com", cifrar_senha("senha234"),
               7000.00, "Ácido e Frutado"),
        Cliente(9, "Lucas Martins", "lucas.martins@email.com", cifrar_senha("senha567"),
               6500.00, "Intenso e Encorpado"),
        Cliente(10, "Beatriz Souza", "beatriz.souza@email.com", cifrar_senha("senha890"),
                3000.00, "Doce e Suave")
    ]
    
    for cliente in clientes:
        cliente_dao.add(cliente)
        print(f"[OK] Cliente criado: {cliente.nome} (ID: {cliente.id}, Saldo: R$ {cliente.saldo:.2f})")
    
    print(f"\nTotal: {len(clientes)} clientes criados.")


def criar_produtos():
    """Cria cafés e máquinas de café para o sistema."""
    print("\n" + "="*60)
    print("CRIANDO PRODUTOS (CAFÉS E MÁQUINAS)")
    print("="*60)
    
    cafe_dao = CafeDAO()
    maquina_dao = MaquinaDeCafeDAO()
    fornecedor_cafe_dao = FornecedoraCafeDAO()
    fornecedor_maquina_dao = FornecedoraMaquinaDAO()
    
    # Buscar fornecedores
    fornecedor1 = fornecedor_cafe_dao.get("12.345.678/0001-90")
    fornecedor2 = fornecedor_cafe_dao.get("23.456.789/0001-01")
    fornecedor3 = fornecedor_cafe_dao.get("34.567.890/0001-12")
    fornecedor4 = fornecedor_cafe_dao.get("45.678.901/0001-23")
    fornecedor5 = fornecedor_cafe_dao.get("56.789.012/0001-34")
    
    fornecedor_maq1 = fornecedor_maquina_dao.get("98.765.432/0001-10")
    fornecedor_maq2 = fornecedor_maquina_dao.get("87.654.321/0001-21")
    fornecedor_maq3 = fornecedor_maquina_dao.get("76.543.210/0001-32")
    fornecedor_maq4 = fornecedor_maquina_dao.get("65.432.109/0001-43")
    
    # Cafés
    cafes = [
        Cafe("Café Especial Gourmet", 25.00, 45.00, 101, "01/01/2024",
             "Minas Gerais", "Arábica", 1200, "Média", 
             "Notas de chocolate e caramelo, corpo encorpado",
             "Doce e Suave", fornecedor1),
        Cafe("Café Premium Orgânico", 30.00, 55.00, 102, "15/01/2024",
             "Espírito Santo", "Arábica", 800, "Fina",
             "Acidez cítrica, notas frutadas",
             "Ácido e Frutado", fornecedor2),
        Cafe("Café Extra Forte", 20.00, 38.00, 103, "20/01/2024",
             "Bahia", "Robusta", 600, "Grossa",
             "Sabor intenso, corpo robusto",
                "Intenso e Encorpado", fornecedor3),
        Cafe("Café Suave Delícia", 22.00, 42.00, 104, "05/02/2024",
             "Paraná", "Arábica", 1000, "Média",
             "Doce e suave, finalização longa",
             "Doce e Suave", fornecedor4),
        Cafe("Café Frutado Especial", 28.00, 52.00, 105, "10/02/2024",
             "Minas Gerais", "Arábica", 1100, "Fina",
             "Notas de frutas vermelhas, acidez brilhante",
             "Ácido e Frutado", fornecedor5),
        Cafe("Café Chocolate Premium", 26.00, 48.00, 106, "18/02/2024",
             "Espírito Santo", "Arábica", 950, "Média",
             "Sabor achocolatado intenso, corpo cremoso",
                "Intenso e Encorpado", fornecedor1),
        Cafe("Café Doce Natural", 24.00, 44.00, 107, "25/02/2024",
             "Bahia", "Arábica", 850, "Fina",
             "Doçura natural, notas de mel",
             "Doce e Suave", fornecedor2),
        Cafe("Café Cítrico Premium", 29.00, 54.00, 108, "01/03/2024",
             "Paraná", "Arábica", 1050, "Fina",
             "Acidez vibrante, notas cítricas",
             "Ácido e Frutado", fornecedor3),
        Cafe("Café Encorpado Forte", 27.00, 50.00, 109, "08/03/2024",
             "Minas Gerais", "Robusta", 700, "Grossa",
             "Corpo encorpado, sabor intenso",
                "Intenso e Encorpado", fornecedor4),
        Cafe("Café Suave Premium", 23.00, 43.00, 110, "15/03/2024",
             "Espírito Santo", "Arábica", 900, "Média",
             "Equilibrado, suave e aromático",
             "Doce e Suave", fornecedor5)
    ]
    
    for cafe in cafes:
        cafe_dao.add(cafe)
        print(f"[OK] Cafe criado: {cafe.nome} (ID: {cafe.id}, Preco: R$ {cafe.preco_venda:.2f})")
    
    # Máquinas de Café
    maquinas = [
        MaquinaDeCafe("Máquina Expresso Profissional", 1500.00, 2500.00, 201,
                      "01/01/2024", fornecedor_maq1),
        MaquinaDeCafe("Cafeteira Automática Premium", 800.00, 1400.00, 202,
                      "10/01/2024", fornecedor_maq2),
        MaquinaDeCafe("Máquina de Cápsulas Deluxe", 600.00, 1100.00, 203,
                      "15/01/2024", fornecedor_maq3),
        MaquinaDeCafe("Expresso Compacta", 1200.00, 2000.00, 204,
                      "20/01/2024", fornecedor_maq4),
        MaquinaDeCafe("Super Automática Premium", 2000.00, 3500.00, 205,
                      "25/01/2024", fornecedor_maq1),
        MaquinaDeCafe("Máquina Doméstica Pro", 700.00, 1300.00, 206,
                      "01/02/2024", fornecedor_maq2),
        MaquinaDeCafe("Expresso Industrial", 3000.00, 5000.00, 207,
                      "05/02/2024", fornecedor_maq3),
        MaquinaDeCafe("Cafeteira Gourmet", 900.00, 1600.00, 208,
                      "10/02/2024", fornecedor_maq4),
        MaquinaDeCafe("Máquina Portátil", 400.00, 750.00, 209,
                      "15/02/2024", fornecedor_maq1),
        MaquinaDeCafe("Expresso Dupla", 1800.00, 3000.00, 210,
                      "20/02/2024", fornecedor_maq2)
    ]
    
    for maquina in maquinas:
        maquina_dao.add(maquina)
        print(f"[OK] Maquina criada: {maquina.nome} (ID: {maquina.id}, Preco: R$ {maquina.preco_venda:.2f})")
    
    print(f"\nTotal: {len(cafes)} cafés e {len(maquinas)} máquinas criados.")


def criar_estoque():
    """Adiciona produtos ao estoque."""
    print("\n" + "="*60)
    print("CRIANDO ESTOQUE")
    print("="*60)
    
    estoque_dao = EstoqueDAO()
    estoque = Estoque()
    cafe_dao = CafeDAO()
    maquina_dao = MaquinaDeCafeDAO()
    
    # Adicionar cafés ao estoque
    quantidades_cafes = {
        101: 50,  102: 30,  103: 40,  104: 35,  105: 25,
        106: 45,  107: 20,  108: 30,  109: 40,  110: 35
    }
    
    for cafe_id, quantidade in quantidades_cafes.items():
        cafe = cafe_dao.get(cafe_id)
        if cafe:
            estoque.cadastrar_novo_produto(cafe, quantidade)
            print(f"[OK] Estoque: {cafe.nome} - {quantidade} unidades")
    
    # Adicionar máquinas ao estoque
    quantidades_maquinas = {
        201: 5,  202: 8,  203: 12,  204: 6,  205: 3,
        206: 10, 207: 2,  208: 7,   209: 15, 210: 4
    }
    
    for maquina_id, quantidade in quantidades_maquinas.items():
        maquina = maquina_dao.get(maquina_id)
        if maquina:
            estoque.cadastrar_novo_produto(maquina, quantidade)
            print(f"[OK] Estoque: {maquina.nome} - {quantidade} unidades")
    
    # Persistir estoque
    produtos_por_id = {produto.id: quantidade for produto, quantidade in estoque.produtos_em_estoque.items()}
    estoque_dao.salvar(produtos_por_id)
    
    total_produtos = sum(quantidades_cafes.values()) + sum(quantidades_maquinas.values())
    print(f"\nTotal: {len(quantidades_cafes) + len(quantidades_maquinas)} tipos de produtos no estoque.")
    print(f"Total de unidades: {total_produtos} itens.")


def criar_e_finalizar_vendas():
    """Cria vendas, adiciona produtos e finaliza algumas delas."""
    print("\n" + "="*60)
    print("CRIANDO E FINALIZANDO VENDAS")
    print("="*60)
    
    venda_dao = VendaDAO()
    cliente_dao = ClienteDAO()
    cafe_dao = CafeDAO()
    maquina_dao = MaquinaDeCafeDAO()
    estoque_dao = EstoqueDAO()
    
    # Carregar estoque
    estoque = Estoque()
    dados_estoque = estoque_dao.carregar()
    for produto_id, quantidade in dados_estoque.items():
        try:
            cafe = cafe_dao.get(produto_id)
            if cafe:
                estoque.cadastrar_novo_produto(cafe, quantidade)
            else:
                maquina = maquina_dao.get(produto_id)
                if maquina:
                    estoque.cadastrar_novo_produto(maquina, quantidade)
        except:
            pass
    
    # Venda 1: Cliente compra apenas cafés
    print("\n--- Venda 1 ---")
    cliente1 = cliente_dao.get(1)
    venda1 = Venda(1001, cliente1)
    cafe1 = cafe_dao.get(101)
    cafe2 = cafe_dao.get(102)
    venda1.adicionar_produto(cafe1, 2)
    venda1.adicionar_produto(cafe2, 1)
    venda1.finalizar_venda(estoque)
    venda_dao.add(venda1)
    print(f"[OK] Venda {venda1.id_venda} finalizada - Cliente: {cliente1.nome}")
    print(f"  Produtos: {cafe1.nome} (2x), {cafe2.nome} (1x)")
    print(f"  Total: R$ {venda1.valor_total:.2f}")
    
    # Venda 2: Cliente compra máquina e cafés
    print("\n--- Venda 2 ---")
    cliente2 = cliente_dao.get(2)
    venda2 = Venda(1002, cliente2)
    maquina1 = maquina_dao.get(201)
    cafe3 = cafe_dao.get(103)
    venda2.adicionar_produto(maquina1, 1)
    venda2.adicionar_produto(cafe3, 5)
    venda2.finalizar_venda(estoque)
    venda_dao.add(venda2)
    print(f"[OK] Venda {venda2.id_venda} finalizada - Cliente: {cliente2.nome}")
    print(f"  Produtos: {maquina1.nome} (1x), {cafe3.nome} (5x)")
    print(f"  Total: R$ {venda2.valor_total:.2f}")
    
    # Venda 3: Cliente compra vários cafés
    print("\n--- Venda 3 ---")
    cliente3 = cliente_dao.get(3)
    venda3 = Venda(1003, cliente3)
    cafe4 = cafe_dao.get(104)
    cafe5 = cafe_dao.get(105)
    cafe6 = cafe_dao.get(106)
    venda3.adicionar_produto(cafe4, 3)
    venda3.adicionar_produto(cafe5, 2)
    venda3.adicionar_produto(cafe6, 4)
    venda3.finalizar_venda(estoque)
    venda_dao.add(venda3)
    print(f"[OK] Venda {venda3.id_venda} finalizada - Cliente: {cliente3.nome}")
    print(f"  Produtos: {cafe4.nome} (3x), {cafe5.nome} (2x), {cafe6.nome} (4x)")
    print(f"  Total: R$ {venda3.valor_total:.2f}")
    
    # Venda 4: Cliente compra máquina premium
    print("\n--- Venda 4 ---")
    cliente4 = cliente_dao.get(4)
    venda4 = Venda(1004, cliente4)
    maquina2 = maquina_dao.get(205)
    cafe7 = cafe_dao.get(107)
    venda4.adicionar_produto(maquina2, 1)
    venda4.adicionar_produto(cafe7, 10)
    venda4.finalizar_venda(estoque)
    venda_dao.add(venda4)
    print(f"[OK] Venda {venda4.id_venda} finalizada - Cliente: {cliente4.nome}")
    print(f"  Produtos: {maquina2.nome} (1x), {cafe7.nome} (10x)")
    print(f"  Total: R$ {venda4.valor_total:.2f}")
    
    # Venda 5: Cliente compra múltiplos produtos
    print("\n--- Venda 5 ---")
    cliente5 = cliente_dao.get(5)
    venda5 = Venda(1005, cliente5)
    maquina3 = maquina_dao.get(202)
    cafe8 = cafe_dao.get(108)
    cafe9 = cafe_dao.get(109)
    venda5.adicionar_produto(maquina3, 1)
    venda5.adicionar_produto(cafe8, 2)
    venda5.adicionar_produto(cafe9, 3)
    venda5.finalizar_venda(estoque)
    venda_dao.add(venda5)
    print(f"[OK] Venda {venda5.id_venda} finalizada - Cliente: {cliente5.nome}")
    print(f"  Produtos: {maquina3.nome} (1x), {cafe8.nome} (2x), {cafe9.nome} (3x)")
    print(f"  Total: R$ {venda5.valor_total:.2f}")
    
    # Venda 6: Venda em andamento (não finalizada)
    print("\n--- Venda 6 (Em Andamento) ---")
    cliente6 = cliente_dao.get(6)
    venda6 = Venda(1006, cliente6)
    cafe10 = cafe_dao.get(110)
    maquina4 = maquina_dao.get(203)
    venda6.adicionar_produto(cafe10, 4)
    venda6.adicionar_produto(maquina4, 1)
    venda_dao.add(venda6)
    print(f"[OK] Venda {venda6.id_venda} criada (em andamento) - Cliente: {cliente6.nome}")
    print(f"  Produtos: {cafe10.nome} (4x), {maquina4.nome} (1x)")
    print(f"  Total: R$ {venda6.valor_total:.2f} (não finalizada)")
    
    # Venda 7: Mais uma venda finalizada
    print("\n--- Venda 7 ---")
    cliente7 = cliente_dao.get(7)
    venda7 = Venda(1007, cliente7)
    cafe1_again = cafe_dao.get(101)
    cafe4_again = cafe_dao.get(104)
    maquina5 = maquina_dao.get(206)
    venda7.adicionar_produto(cafe1_again, 5)
    venda7.adicionar_produto(cafe4_again, 3)
    venda7.adicionar_produto(maquina5, 1)
    venda7.finalizar_venda(estoque)
    venda_dao.add(venda7)
    print(f"[OK] Venda {venda7.id_venda} finalizada - Cliente: {cliente7.nome}")
    print(f"  Produtos: {cafe1_again.nome} (5x), {cafe4_again.nome} (3x), {maquina5.nome} (1x)")
    print(f"  Total: R$ {venda7.valor_total:.2f}")
    
    # Venda 8: Venda grande com múltiplos itens
    print("\n--- Venda 8 ---")
    cliente8 = cliente_dao.get(8)
    venda8 = Venda(1008, cliente8)
    maquina6 = maquina_dao.get(207)
    cafe2_again = cafe_dao.get(102)
    cafe5_again = cafe_dao.get(105)
    cafe8_again = cafe_dao.get(108)
    venda8.adicionar_produto(maquina6, 1)
    venda8.adicionar_produto(cafe2_again, 6)
    venda8.adicionar_produto(cafe5_again, 4)
    venda8.adicionar_produto(cafe8_again, 3)
    venda8.finalizar_venda(estoque)
    venda_dao.add(venda8)
    print(f"[OK] Venda {venda8.id_venda} finalizada - Cliente: {cliente8.nome}")
    print(f"  Produtos: {maquina6.nome} (1x), {cafe2_again.nome} (6x), {cafe5_again.nome} (4x), {cafe8_again.nome} (3x)")
    print(f"  Total: R$ {venda8.valor_total:.2f}")
    
    # Venda 9: Venda simples de café
    print("\n--- Venda 9 ---")
    cliente9 = cliente_dao.get(9)
    venda9 = Venda(1009, cliente9)
    cafe3_again = cafe_dao.get(103)
    cafe6_again = cafe_dao.get(106)
    cafe9_again = cafe_dao.get(109)
    venda9.adicionar_produto(cafe3_again, 7)
    venda9.adicionar_produto(cafe6_again, 5)
    venda9.adicionar_produto(cafe9_again, 6)
    venda9.finalizar_venda(estoque)
    venda_dao.add(venda9)
    print(f"[OK] Venda {venda9.id_venda} finalizada - Cliente: {cliente9.nome}")
    print(f"  Produtos: {cafe3_again.nome} (7x), {cafe6_again.nome} (5x), {cafe9_again.nome} (6x)")
    print(f"  Total: R$ {venda9.valor_total:.2f}")
    
    # Venda 10: Venda em andamento
    print("\n--- Venda 10 (Em Andamento) ---")
    cliente10 = cliente_dao.get(10)
    venda10 = Venda(1010, cliente10)
    maquina7 = maquina_dao.get(208)
    cafe7_again = cafe_dao.get(107)
    venda10.adicionar_produto(maquina7, 1)
    venda10.adicionar_produto(cafe7_again, 2)
    venda_dao.add(venda10)
    print(f"[OK] Venda {venda10.id_venda} criada (em andamento) - Cliente: {cliente10.nome}")
    print(f"  Produtos: {maquina7.nome} (1x), {cafe7_again.nome} (2x)")
    print(f"  Total: R$ {venda10.valor_total:.2f} (não finalizada)")
    
    # Persistir estoque atualizado
    produtos_por_id = {produto.id: quantidade for produto, quantidade in estoque.produtos_em_estoque.items()}
    estoque_dao.salvar(produtos_por_id)
    
    vendas_finalizadas = [v for v in venda_dao.get_all() if v.status_venda == "Finalizada"]
    vendas_andamento = [v for v in venda_dao.get_all() if v.status_venda == "Em andamento"]
    
    total_arrecadado = sum(v.valor_total for v in vendas_finalizadas)
    
    print(f"\nTotal: {len(vendas_finalizadas)} vendas finalizadas e {len(vendas_andamento)} vendas em andamento.")
    print(f"Total arrecadado: R$ {total_arrecadado:.2f}")


def exibir_resumo():
    """Exibe um resumo completo do sistema após os testes."""
    print("\n" + "="*60)
    print("RESUMO DO SISTEMA")
    print("="*60)
    
    fornecedor_cafe_dao = FornecedoraCafeDAO()
    fornecedor_maquina_dao = FornecedoraMaquinaDAO()
    cliente_dao = ClienteDAO()
    cafe_dao = CafeDAO()
    maquina_dao = MaquinaDeCafeDAO()
    venda_dao = VendaDAO()
    estoque_dao = EstoqueDAO()
    
    fornecedores_cafe = list(fornecedor_cafe_dao.get_all())
    fornecedores_maquina = list(fornecedor_maquina_dao.get_all())
    clientes = list(cliente_dao.get_all())
    cafes = list(cafe_dao.get_all())
    maquinas = list(maquina_dao.get_all())
    vendas = list(venda_dao.get_all())
    dados_estoque = estoque_dao.carregar()
    
    print(f"\nFornecedores de Café: {len(fornecedores_cafe)}")
    print(f"Fornecedores de Máquinas: {len(fornecedores_maquina)}")
    print(f"Clientes: {len(clientes)}")
    print(f"Cafés: {len(cafes)}")
    print(f"Máquinas: {len(maquinas)}")
    print(f"Tipos de Produtos no Estoque: {len(dados_estoque)}")
    print(f"Vendas: {len(vendas)}")
    
    vendas_finalizadas = [v for v in vendas if v.status_venda == "Finalizada"]
    vendas_andamento = [v for v in vendas if v.status_venda == "Em andamento"]
    
    print(f"\nVendas Finalizadas: {len(vendas_finalizadas)}")
    print(f"Vendas em Andamento: {len(vendas_andamento)}")
    
    if vendas_finalizadas:
        total_arrecadado = sum(v.valor_total for v in vendas_finalizadas)
        print(f"Total Arrecadado: R$ {total_arrecadado:.2f}")
        
        # Cliente que mais gastou
        gastos_por_cliente = {}
        for venda in vendas_finalizadas:
            cliente_id = venda.cliente.id
            gastos_por_cliente[cliente_id] = gastos_por_cliente.get(cliente_id, 0) + venda.valor_total
        
        if gastos_por_cliente:
            cliente_maior_gasto = max(gastos_por_cliente.items(), key=lambda x: x[1])
            cliente = cliente_dao.get(cliente_maior_gasto[0])
            print(f"Cliente que mais gastou: {cliente.nome} - R$ {cliente_maior_gasto[1]:.2f}")
    
    # Produtos mais vendidos
    produtos_vendidos = {}
    for venda in vendas_finalizadas:
        for produto, quantidade in venda.carrinho.items():
            produtos_vendidos[produto.id] = produtos_vendidos.get(produto.id, 0) + quantidade
    
    if produtos_vendidos:
        top_produtos = sorted(produtos_vendidos.items(), key=lambda x: x[1], reverse=True)[:5]
        print(f"\nTop 5 Produtos Mais Vendidos:")
        for produto_id, quantidade in top_produtos:
            cafe = cafe_dao.get(produto_id)
            if cafe:
                print(f"  - {cafe.nome}: {quantidade} unidades")
            else:
                maquina = maquina_dao.get(produto_id)
                if maquina:
                    print(f"  - {maquina.nome}: {quantidade} unidades")
    
    print("\n" + "="*60)
    print("TESTE COMPLETO FINALIZADO COM SUCESSO!")
    print("="*60)


def main():
    """Função principal que executa todos os testes."""
    print("\n" + "="*60)
    print("INICIANDO TESTE COMPLETO DO SISTEMA CAFERRI")
    print("="*60)
    
    try:
        # Executar todas as operações
        criar_fornecedores()
        criar_clientes()
        criar_produtos()
        criar_estoque()
        criar_e_finalizar_vendas()
        exibir_resumo()
        
    except Exception as e:
        print(f"\n[ERRO] ERRO durante execucao: {e}")
        import traceback
        traceback.print_exc()
        return
    
    print("\n[OK] Todos os testes foram executados com sucesso!")
    print("O sistema está populado e pronto para uso.")


if __name__ == "__main__":
    main()

