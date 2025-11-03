"""
        Este Mixin foi projetado para ser herdado por controladores que precisam
    localizar um `Produto` (seja um `Cafe` ou uma `MaquinaDeCafe`) sem
    precisar conhecer os detalhes de onde esses produtos estão armazenados.

    Ele abstrai a lógica de busca em múltiplos repositórios (ControladorCafe,
    ControladorMaquinaDeCafe), centralizando o acesso e promovendo o reuso
    de código. Assume-se que a classe que herda este Mixin terá acesso a
    `controlador_sistema`.

    Além disso, fornece métodos para verificar a existência de IDs de produtos
    e CNPJs de fornecedores, garantindo a unicidade desses identificadores.
    """

from Excecoes.fornecedorNaoEncontradoException import FornecedorNaoEncontradoException
from Excecoes.produtoNaoEncontradoException import ProdutoNaoEncontradoException
from Excecoes.cafeNaoEncontradoException import CafeNaoEncontradoException
from Excecoes.maquinaNaoEncontradaException import MaquinaNaoEncontradaException
from entidade.produto import Produto

class BuscaProdutoMixin:

    def existe_fornecedor_com_cnpj(self, cnpj: str) -> bool:
        try:
            self._controlador_sistema.controlador_empresa_cafe.pega_fornecedor_por_cnpj(cnpj)
            return True
        except FornecedorNaoEncontradoException:
            pass
        try:
            self._controlador_sistema.controlador_empresa_maquina.pega_fornecedor_por_cnpj(cnpj)
            return True 
        except FornecedorNaoEncontradoException:
            return False

    def existe_produto(self) -> bool:
        return bool(self._controlador_sistema.controlador_cafe.cafes or
                    self._controlador_sistema.controlador_maquina_de_cafe.maquinas)

    def pega_produto_por_id(self, id_produto: int) -> Produto:
        try:
            return self._controlador_sistema.controlador_cafe.pega_cafe_por_id(id_produto)
        except CafeNaoEncontradoException:
            try:
                return self._controlador_sistema.controlador_maquina_de_cafe.pega_maquina_por_id(
                    id_produto)
            except MaquinaNaoEncontradaException:
                raise ProdutoNaoEncontradoException()

    def id_produto_ja_existe(self, id_produto: int) -> bool:
        try:
            self.pega_produto_por_id(id_produto)
            return True
        except ProdutoNaoEncontradoException:
            return False