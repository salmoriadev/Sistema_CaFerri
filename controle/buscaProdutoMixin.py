from Excecoes.produtoNaoEncontradoException import ProdutoNaoEncontradoException
from Excecoes.cafeNaoEncontradoException import CafeNaoEncontradoException
from Excecoes.maquinaNaoEncontradaException import MaquinaNaoEncontradaException
from entidade.produto import Produto

"""
    Mixin que fornece métodos para buscar produtos (Café ou Máquina)
    em todo o sistema.
    """
class BuscaProdutoMixin:

    def existe_produto(self) -> bool:
        return bool(self._controlador_sistema.controlador_cafe.cafes or
                    self._controlador_sistema.controlador_maquina_de_cafe.maquinas)

    def pega_produto_por_id(self, id_produto: int) -> Produto:
        try:
            return self._controlador_sistema.controlador_cafe.pega_cafe_por_id(id_produto)
        except CafeNaoEncontradoException:
            try:
                return self._controlador_sistema.controlador_maquina_de_cafe.pega_maquina_por_id(id_produto)
            except MaquinaNaoEncontradaException:
                raise ProdutoNaoEncontradoException()

    def id_produto_ja_existe(self, id_produto: int) -> bool:
        try:
            self.pega_produto_por_id(id_produto)
            return True
        except ProdutoNaoEncontradoException:
            return False