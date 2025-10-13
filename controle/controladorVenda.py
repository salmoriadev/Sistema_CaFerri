"""
    Orquestra toda a lógica de negócio para o processo de Vendas.

    Esta classe atua como a camada de Controle (Controller) central para
    qualquer transação de venda. Ela gerencia o ciclo de vida completo de
    uma venda, desde sua criação até a finalização ou cancelamento, fazendo
    a ponte entre a interface do usuário (`TelaVenda`) e a entidade `Venda`.

    Como um hub de operações, este controlador colabora intensamente com
    outras partes do sistema:
    - Utiliza o `ControladorCliente` para associar um cliente a uma venda.
    - Herda de `BuscaProdutoMixin` para localizar produtos (cafés ou máquinas)
      a serem adicionados ao carrinho.
    - Fornece a instância de `Estoque` (do `ControladorEstoque`) para a
      entidade `Venda` no momento da finalização, permitindo que a própria
      venda valide a disponibilidade dos itens.

    Gerencia o fluxo de navegação entre o menu principal de vendas e um
    submenu de gerenciamento de uma venda específica, além de tratar um
    amplo leque de exceções para garantir a integridade dos dados e
    fornecer feedback claro ao usuário.
    """

from controle.buscaProdutoMixin import BuscaProdutoMixin
from limite.telaVenda import TelaVenda
from entidade.venda import Venda
from Excecoes.clienteNaoEncontradoException import ClienteNaoEncontradoException
from Excecoes.produtoNaoEncontradoException import ProdutoNaoEncontradoException
from Excecoes.vendaNaoEncontradaException import VendaNaoEncontradaException
from Excecoes.IDJaExistenteException import IDJaExistenteException

class ControladorVenda(BuscaProdutoMixin):
    def __init__(self, controlador_sistema) -> None:
        self._controlador_sistema = controlador_sistema
        self.__vendas = []
        self.__tela_venda = TelaVenda()

    @property
    def vendas(self) -> list:
        return self.__vendas

    def pega_venda_por_id(self, id_venda: int) -> Venda:
        for venda in self.__vendas:
            if venda.id_venda == id_venda:
                return venda
        raise VendaNaoEncontradaException()

    def iniciar_venda(self) -> None:
        dados_iniciais = self.__tela_venda.pega_dados_iniciar_venda()
        if dados_iniciais is None: return

        for v in self.__vendas:
            if v.id_venda == dados_iniciais["id_venda"]:
                raise IDJaExistenteException("Venda")
        
        cliente = self._controlador_sistema.controlador_cliente.pega_cliente_por_id(dados_iniciais["id_cliente"])
        nova_venda = Venda(dados_iniciais["id_venda"], cliente)
        self.__vendas.append(nova_venda)
        self.__tela_venda.mostra_mensagem("Venda iniciada com sucesso! Adicione produtos ao carrinho.")
        self.gerenciar_venda(nova_venda)

    def gerenciar_venda(self, venda: Venda) -> None:
        mapa_opcoes = {
            1: self.adicionar_produto,
            2: self.diminuir_quantidade_produto, 
            3: self.remover_produto,
            4: self.listar_produtos_venda,
            5: self.finalizar_venda
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

    def adicionar_produto(self, venda: Venda) -> None:
        dados = self.__tela_venda.pega_dados_produto()
        if dados:
            produto = self.pega_produto_por_id(dados["id_produto"])
            venda.adicionar_produto(produto, dados["quantidade"])
            self.__tela_venda.mostra_mensagem(f"'{produto.nome}' adicionado ao carrinho.")

    def diminuir_quantidade_produto(self, venda: Venda) -> None:
        dados = self.__tela_venda.pega_dados_produto()
        if dados:
            produto = self.pega_produto_por_id(dados["id_produto"])
            resultado = venda.diminuir_quantidade_produto(produto, dados["quantidade"])
            self.__tela_venda.mostra_mensagem(resultado)

    def remover_produto(self, venda: Venda) -> None:
        dados = self.__tela_venda.pega_dados_produto()
        if dados:
            produto = self.pega_produto_por_id(dados["id_produto"])
            venda.remover_produto(produto)
            self.__tela_venda.mostra_mensagem(f"'{produto.nome}' removido do carrinho.")

    def listar_produtos_venda(self, venda: Venda) -> None:
        self.mostrar_detalhes_venda(venda)

    def finalizar_venda(self, venda: Venda) -> None:
        estoque = self._controlador_sistema.controlador_estoque.estoque
        resultado = venda.finalizar_venda(estoque)
        self.__tela_venda.mostra_mensagem(resultado)

    def listar_vendas(self) -> None:
        if not self.__vendas:
            self.__tela_venda.mostra_mensagem("Nenhuma venda registrada.")
            return
        for venda in self.__vendas:
            self.mostrar_detalhes_venda(venda)

    def mostrar_detalhes_venda(self, venda: Venda) -> None:
        produtos_formatados = venda.listar_produtos_formatado()
        self.__tela_venda.mostra_venda({
            "id_venda": venda.id_venda,
            "cliente_nome": venda.cliente.nome,
            "valor_total": venda.valor_total,
            "status": venda.status_venda,
            "produtos": produtos_formatados
        })

    def excluir_venda(self) -> None:
        self.listar_vendas()
        if not self.__vendas: return
        
        id_venda = self.__tela_venda.seleciona_venda()
        venda = self.pega_venda_por_id(id_venda)
        if venda.status_venda == "Finalizada":
            self.__tela_venda.mostra_mensagem("Não é possível excluir uma venda já finalizada.")
            return
            
        self.__vendas.remove(venda)
        self.__tela_venda.mostra_mensagem("Venda cancelada com sucesso.")

    def retornar(self) -> None:
        self._controlador_sistema.abre_tela()

    def abre_tela(self) -> None:
        mapa_opcoes = {
            1: self.iniciar_venda, 2: self.listar_vendas, 3: self.excluir_venda, 4: self.gerenciar_venda, 0: self.retornar
        }
        while True:
            try:
                opcao = self.__tela_venda.tela_opcoes()
                if opcao == 0:
                    mapa_opcoes[0]()
                    break
                if opcao == 4:
                    self.listar_vendas()
                    if not self.__vendas: continue
                    id_venda = self.__tela_venda.seleciona_venda()
                    venda = self.pega_venda_por_id(id_venda)
                    if venda.status_venda == "Finalizada":
                        self.__tela_venda.mostra_mensagem("Não é possível gerenciar uma venda já finalizada.")
                        continue
                    self.gerenciar_venda(venda)
                elif opcao in mapa_opcoes:
                    mapa_opcoes[opcao]()
                else:
                    self.__tela_venda.mostra_mensagem("Opção inválida.")
            except (ClienteNaoEncontradoException, ProdutoNaoEncontradoException, 
                    VendaNaoEncontradaException, IDJaExistenteException) as e:
                self.__tela_venda.mostra_mensagem(f"ERRO: {e}")