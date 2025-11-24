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
from Excecoes.vendaNaoEmAndamentoException import VendaNaoEmAndamentoException
from Excecoes.saldoInsuficienteException import SaldoInsuficienteException
from Excecoes.produtoNaoEmEstoqueException import ProdutoNaoEmEstoqueException
from Excecoes.estoqueInsuficienteException import EstoqueInsuficienteException
from DAOs.venda_dao import VendaDAO


class ControladorVenda(BuscaProdutoMixin):
    def __init__(self, controlador_sistema) -> None:
        self._controlador_sistema = controlador_sistema
        self.__venda_dao = VendaDAO()
        self.__tela_venda = TelaVenda()

    @property
    def vendas(self) -> list:
        return list(self.__venda_dao.get_all())

    def pega_venda_por_id(self, id_venda: int) -> Venda:
        """
        Recupera uma venda específica pelo ID. Lança exceção se não encontrada.
        Usado internamente e por outros módulos que precisam acessar vendas
        específicas para operações de gerenciamento ou relatórios.
        """
        venda = self.__venda_dao.get(id_venda)
        if venda is None:
            raise VendaNaoEncontradaException()
        return venda

    def iniciar_venda(self) -> None:
        """
        Cria uma nova venda no sistema. Coleta ID da venda e ID do cliente,
        valida que não existe venda com mesmo ID, recupera cliente e cria
        instância de Venda com status "Em andamento". Após criação, redireciona
        automaticamente para o gerenciamento da venda recém-criada.
        """
        dados_venda = self.__tela_venda.pega_dados_iniciar_venda()
        if dados_venda is None:
            return

        if self.__venda_dao.get(dados_venda["id_venda"]):
            raise IDJaExistenteException("Venda")

        cliente = self._controlador_sistema.controlador_cliente.pega_cliente_por_id(
            dados_venda["id_cliente"])
        nova_venda = Venda(dados_venda["id_venda"], cliente)
        self.__venda_dao.add(nova_venda)
        self.__tela_venda.mostra_mensagem(
            "Venda iniciada com sucesso! Adicione produtos ao carrinho.")
        self.gerenciar_venda(nova_venda)

    def gerenciar_venda(self, venda: Venda) -> None:
        """
        Controla o loop de gerenciamento de uma venda em andamento. Exibe
        detalhes da venda, oferece opções para modificar carrinho (adicionar,
        diminuir, remover produtos) e finalizar. Persiste alterações após
        cada operação e continua até venda ser finalizada ou usuário salvar
        e sair. Validações de estoque e saldo são feitas pela entidade Venda.
        """
        mapa_opcoes = {
            1: self.adicionar_produto,
            2: self.diminuir_quantidade_produto,
            3: self.remover_produto,
            4: self.listar_produtos_venda,
            5: self.finalizar_venda
        }
        while venda.status_venda == "Em andamento":
            try:
                self.mostrar_detalhes_venda(venda)
                opcao = self.__tela_venda.tela_opcoes_gerenciar_venda()
                if opcao == 0:
                    self.__tela_venda.mostra_mensagem(
                        "Venda salva para continuar depois.")
                    break
                if opcao in mapa_opcoes:
                    mapa_opcoes[opcao](venda)
                else:
                    self.__tela_venda.mostra_mensagem(
                        "Opção inválida! Por favor, digite um número do menu.")
            except (ProdutoNaoEncontradoException,
                    VendaNaoEmAndamentoException, SaldoInsuficienteException,
                    ProdutoNaoEmEstoqueException, EstoqueInsuficienteException) as e:
                self.__tela_venda.mostra_mensagem(f"ERRO: {e}")

    def adicionar_produto(self, venda: Venda) -> None:
        """
        Adiciona produto ao carrinho da venda. Busca produto pelo ID usando
        mixin, adiciona à venda (que recalcula total automaticamente) e
        persiste estado atualizado. Exibe confirmação com nome do produto.
        """
        dados_produto = self.__tela_venda.pega_dados_produto()
        if dados_produto:
            produto = self.pega_produto_por_id(dados_produto["id_produto"])
            venda.adicionar_produto(produto, dados_produto["quantidade"])
            self.__salvar_venda(venda)
            self.__tela_venda.mostra_mensagem(
                f"'{produto.nome}' adicionado ao carrinho.")

    def diminuir_quantidade_produto(self, venda: Venda) -> None:
        """
        Reduz quantidade de um produto no carrinho. Se quantidade a remover
        for maior ou igual à quantidade no carrinho, remove produto completamente.
        Retorna mensagem descritiva da operação realizada e persiste alterações.
        """
        dados_produto = self.__tela_venda.pega_dados_produto()
        if dados_produto:
            produto = self.pega_produto_por_id(dados_produto["id_produto"])
            resultado = venda.diminuir_quantidade_produto(
                produto, dados_produto["quantidade"])
            self.__salvar_venda(venda)
            self.__tela_venda.mostra_mensagem(resultado)

    def remover_produto(self, venda: Venda) -> None:
        """
        Remove completamente um produto do carrinho, independente da quantidade.
        Recalcula valor total da venda e persiste estado atualizado. Exibe
        confirmação com nome do produto removido.
        """
        dados_produto = self.__tela_venda.pega_dados_produto()
        if dados_produto:
            produto = self.pega_produto_por_id(dados_produto["id_produto"])
            venda.remover_produto(produto)
            self.__salvar_venda(venda)
            self.__tela_venda.mostra_mensagem(
                f"'{produto.nome}' removido do carrinho.")

    def listar_produtos_venda(self, venda: Venda) -> None:
        """
        Exibe detalhes completos da venda, incluindo todos os produtos no
        carrinho com quantidades e subtotais. Usado para visualização durante
        o gerenciamento da venda.
        """
        self.mostrar_detalhes_venda(venda)

    def finalizar_venda(self, venda: Venda) -> None:
        """
        Finaliza uma venda em andamento. Delega validações e operações
        transacionais para a entidade Venda, que verifica saldo do cliente,
        disponibilidade no estoque, debita valores e atualiza estoque.
        Persiste venda com status "Finalizada" e data de conclusão.
        """
        estoque = self._controlador_sistema.controlador_estoque.estoque
        venda.finalizar_venda(estoque)
        self.__salvar_venda(venda)
        self.__tela_venda.mostra_mensagem("Venda finalizada com sucesso!")

    def listar_vendas(self) -> None:
        """
        Exibe lista formatada de todas as vendas registradas no sistema.
        Extrai informações resumidas (ID, cliente, status, valor total) e
        delega a exibição para a tela. Usado para visualização geral e como
        passo intermediário em operações de gerenciamento e exclusão.
        """
        if not self.vendas:
            self.__tela_venda.mostra_mensagem("Nenhuma venda registrada.")
            return

        dados_vendas = []
        for venda in self.vendas:
            dados_vendas.append({
                "id_venda": venda.id_venda,
                "cliente_nome": venda.cliente.nome,
                "status": venda.status_venda,
                "valor_total": venda.valor_total
            })
        self.__tela_venda.mostra_lista_vendas(dados_vendas)

    def mostrar_detalhes_venda(self, venda: Venda) -> None:
        """
        Exibe detalhes completos de uma venda específica, incluindo todos
        os produtos no carrinho com quantidades e subtotais formatados.
        Usado durante gerenciamento de venda para visualização em tempo real
        do estado atual do carrinho.
        """
        produtos_formatados = venda.listar_produtos_formatado()
        self.__tela_venda.mostra_venda({
            "id_venda": venda.id_venda,
            "cliente_nome": venda.cliente.nome,
            "valor_total": venda.valor_total,
            "status": venda.status_venda,
            "produtos": produtos_formatados
        })

    def excluir_venda(self) -> None:
        """
        Processa o cancelamento de uma venda em andamento. Lista vendas,
        permite seleção, valida que venda não está finalizada (não permite
        exclusão de vendas concluídas) e remove do repositório. Exibe
        confirmação de cancelamento.
        """
        self.listar_vendas()
        if not self.vendas:
            return

        id_venda = self.__tela_venda.seleciona_venda()
        if id_venda is None:
            return
        venda = self.pega_venda_por_id(id_venda)
        if venda.status_venda == "Finalizada":
            self.__tela_venda.mostra_mensagem(
                "Não é possível excluir uma venda já finalizada.")
            return

        self.__venda_dao.remove(venda.id_venda)
        self.__tela_venda.mostra_mensagem("Venda cancelada com sucesso.")

    def retornar(self) -> None:
        """
        Retorna ao menu principal do sistema, delegando navegação para o
        controlador sistema.
        """
        self._controlador_sistema.abre_tela()

    def abre_tela(self) -> None:
        """
        Controla o loop principal do menu de vendas. Exibe opções, captura
        escolha do usuário e delega execução para método correspondente.
        Trata exceções de negócio e exibe mensagens de erro apropriadas.
        Continua em loop até usuário escolher retornar (opção 0). Opção
        especial (4) permite gerenciar venda existente em andamento.
        """
        mapa_opcoes = {
            1: self.iniciar_venda,
            2: self.listar_vendas,
            3: self.excluir_venda,
            4: self.gerenciar_venda,
            0: self.retornar
        }
        while True:
            try:
                opcao = self.__tela_venda.tela_opcoes()
                if opcao == 0:
                    mapa_opcoes[0]()
                    break
                if opcao == 4:
                    self.listar_vendas()
                    if not self.vendas:
                        continue
                    id_venda = self.__tela_venda.seleciona_venda()
                    if id_venda is None:
                        continue
                    venda = self.pega_venda_por_id(id_venda)
                    if venda.status_venda == "Finalizada":
                        self.__tela_venda.mostra_mensagem(
                            "Não é possível gerenciar uma venda já finalizada.")
                        continue
                    self.gerenciar_venda(venda)
                elif opcao in mapa_opcoes:
                    mapa_opcoes[opcao]()
                else:
                    self.__tela_venda.mostra_mensagem(
                        "Opção inválida! Por favor, digite um número do menu.")
            except (ClienteNaoEncontradoException, ProdutoNaoEncontradoException,
                    VendaNaoEncontradaException, IDJaExistenteException,
                    VendaNaoEmAndamentoException, SaldoInsuficienteException,
                    ProdutoNaoEmEstoqueException, EstoqueInsuficienteException) as e:
                self.__tela_venda.mostra_mensagem(f"ERRO: {e}")

    def __salvar_venda(self, venda: Venda) -> None:
        """
        Persiste estado atualizado da venda no repositório. Chamado após
        cada modificação no carrinho para garantir que alterações não sejam
        perdidas. Método privado usado internamente após operações de
        adicionar, remover ou modificar produtos.
        """
        self.__venda_dao.update(venda)
