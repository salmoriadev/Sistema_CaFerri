from limite.telaVenda import TelaVenda
from entidade.venda import Venda
from Excecoes.clienteNaoEncontradoException import ClienteNaoEncontradoException
from Excecoes.produtoNaoEncontradoException import ProdutoNaoEncontradoException
from Excecoes.vendaNaoEncontradaException import VendaNaoEncontradaException
from Excecoes.IDJaExistenteException import IDJaExistenteException

class ControladorVenda:
    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__vendas = []
        self.__tela_venda = TelaVenda()

    def pega_venda_por_id(self, id_venda: int):
        for venda in self.__vendas:
            if venda.id_venda == id_venda:
                return venda
        raise VendaNaoEncontradaException()

    def __pega_produto_por_id(self, id_produto: int):
        try:
            return self.__controlador_sistema.controlador_cafe.pega_cafe_por_id(id_produto)
        except:
            try:
                return self.__controlador_sistema.controlador_maquina_de_cafe.pega_maquina_por_id(id_produto)
            except:
                raise ProdutoNaoEncontradoException()

    def iniciar_venda(self):
        dados_iniciais = self.__tela_venda.pega_dados_iniciar_venda()
        if dados_iniciais is None: return

        for v in self.__vendas:
            if v.id_venda == dados_iniciais["id_venda"]:
                raise IDJaExistenteException("Venda")
        
        cliente = self.__controlador_sistema.controlador_cliente.pega_cliente_por_id(dados_iniciais["id_cliente"])
        produto_inicial = self.__pega_produto_por_id(dados_iniciais["id_produto"])

        nova_venda = Venda(dados_iniciais["id_venda"], cliente, produto_inicial)
        self.__vendas.append(nova_venda)
        self.__tela_venda.mostra_mensagem("Venda iniciada com sucesso!")
        self.gerenciar_venda(nova_venda)

    def gerenciar_venda(self, venda: Venda):
        mapa_opcoes = {
            1: self.adicionar_produto, 2: self.remover_produto,
            3: self.listar_produtos_venda, 4: self.finalizar_venda
        }
        while venda.status_venda == "Em andamento":
            self.mostrar_detalhes_venda(venda)
            opcao = self.__tela_venda.tela_opcoes_gerenciar_venda()
            if opcao == 0:
                self.__tela_venda.mostra_mensagem("Venda salva para continuar depois.")
                break
            if opcao in mapa_opcoes:
                mapa_opcoes[opcao](venda)
            else:
                self.__tela_venda.mostra_mensagem("Opção inválida.")

    def adicionar_produto(self, venda: Venda):
        dados = self.__tela_venda.pega_dados_produto()
        if dados:
            produto = self.__pega_produto_por_id(dados["id_produto"])
            venda.adicionar_produto(produto, dados["quantidade"])
            self.__tela_venda.mostra_mensagem(f"'{produto.nome}' adicionado ao carrinho.")

    def remover_produto(self, venda: Venda):
        dados = self.__tela_venda.pega_dados_produto()
        if dados:
            produto = self.__pega_produto_por_id(dados["id_produto"])
            venda.remover_produto(produto)
            self.__tela_venda.mostra_mensagem(f"'{produto.nome}' removido do carrinho.")

    def listar_produtos_venda(self, venda: Venda):
        self.mostrar_detalhes_venda(venda)

    def finalizar_venda(self, venda: Venda):
        estoque = self.__controlador_sistema.controlador_estoque.estoque
        resultado = venda.finalizar_venda(estoque)
        self.__tela_venda.mostra_mensagem(resultado)

    def listar_vendas(self):
        if not self.__vendas:
            self.__tela_venda.mostra_mensagem("Nenhuma venda registrada.")
            return
        for venda in self.__vendas:
            self.mostrar_detalhes_venda(venda)

    def mostrar_detalhes_venda(self, venda: Venda):
        self.__tela_venda.mostra_venda({
            "id_venda": venda.id_venda,
            "cliente_nome": venda.cliente.nome,
            "valor_total": venda.valor_total,
            "status": venda.status_venda,
            "produtos": venda.listar_produtos()
        })

    def excluir_venda(self):
        self.listar_vendas()
        if not self.__vendas: return
        
        id_venda = self.__tela_venda.seleciona_venda()
        venda = self.pega_venda_por_id(id_venda)
        if venda.status_venda == "Finalizada":
            self.__tela_venda.mostra_mensagem("Não é possível excluir uma venda já finalizada.")
            return
            
        self.__vendas.remove(venda)
        self.__tela_venda.mostra_mensagem("Venda cancelada com sucesso.")

    def retornar(self):
        self.__controlador_sistema.abre_tela()

    def abre_tela(self):
        mapa_opcoes = {
            1: self.iniciar_venda, 2: self.listar_vendas, 3: self.excluir_venda, 0: self.retornar
        }
        while True:
            try:
                opcao = self.__tela_venda.tela_opcoes()
                if opcao == 0:
                    mapa_opcoes[0]()
                    break
                
                if opcao in mapa_opcoes:
                    mapa_opcoes[opcao]()
                else:
                    self.__tela_venda.mostra_mensagem("Opção inválida.")
            except (ClienteNaoEncontradoException, ProdutoNaoEncontradoException, 
                    VendaNaoEncontradaException, IDJaExistenteException) as e:
                self.__tela_venda.mostra_mensagem(f"ERRO: {e}")