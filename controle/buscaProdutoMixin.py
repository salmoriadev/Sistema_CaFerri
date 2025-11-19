"""
Mixin para busca unificada de produtos e validação de identificadores.

Este módulo implementa um mixin que fornece funcionalidade de busca de produtos
(cafés e máquinas) sem acoplamento direto aos controladores específicos. A
classe que herda este mixin deve ter acesso a `_controlador_sistema` para
delegar as buscas aos controladores apropriados.

Funcionalidades principais:
- Busca produtos por ID em todos os repositórios (cafés e máquinas)
- Verifica existência de IDs de produtos para garantir unicidade
- Verifica existência de CNPJs de fornecedores em ambos os tipos de empresa
- Abstrai a complexidade de múltiplos repositórios de produtos

Este mixin é usado por controladores que precisam trabalhar com produtos de
forma genérica, como ControladorVenda e ControladorEstoque, permitindo que
eles não precisem conhecer se um produto é um café ou uma máquina.
"""

from Excecoes.fornecedorNaoEncontradoException import FornecedorNaoEncontradoException
from Excecoes.produtoNaoEncontradoException import ProdutoNaoEncontradoException
from Excecoes.cafeNaoEncontradoException import CafeNaoEncontradoException
from Excecoes.maquinaNaoEncontradaException import MaquinaNaoEncontradaException
from entidade.produto import Produto


class BuscaProdutoMixin:

    def existe_fornecedor_com_cnpj(self, cnpj: str) -> bool:
        """
        Verifica se existe um fornecedor (de café ou máquina) com o CNPJ
        fornecido. Busca primeiro em fornecedores de café, depois em
        fornecedores de máquinas. Retorna True se encontrar em qualquer um.
        """
        try:
            self._controlador_sistema.controlador_empresa_cafe.pega_fornecedor_por_cnpj(
                cnpj)
            return True
        except FornecedorNaoEncontradoException:
            pass
        try:
            self._controlador_sistema.controlador_empresa_maquina.pega_fornecedor_por_cnpj(
                cnpj)
            return True
        except FornecedorNaoEncontradoException:
            return False

    def existe_produto(self) -> bool:
        """
        Verifica se existe pelo menos um produto (café ou máquina) cadastrado
        no sistema. Usado para validações de pré-condição em operações que
        requerem produtos existentes.
        """
        return bool(self._controlador_sistema.controlador_cafe.cafes or
                    self._controlador_sistema.controlador_maquina_de_cafe.maquinas)

    def pega_produto_por_id(self, id_produto: int) -> Produto:
        """
        Busca um produto pelo ID em todos os repositórios. Tenta primeiro
        encontrar como café, depois como máquina. Lança ProdutoNaoEncontradoException
        se não encontrar em nenhum repositório.
        """
        try:
            return self._controlador_sistema.controlador_cafe.pega_cafe_por_id(id_produto)
        except CafeNaoEncontradoException:
            try:
                return self._controlador_sistema.controlador_maquina_de_cafe.pega_maquina_por_id(
                    id_produto)
            except MaquinaNaoEncontradaException:
                raise ProdutoNaoEncontradoException()

    def id_produto_ja_existe(self, id_produto: int) -> bool:
        """
        Verifica se já existe um produto (café ou máquina) com o ID fornecido.
        Usado para garantir unicidade de IDs antes de criar novos produtos.
        """
        try:
            self.pega_produto_por_id(id_produto)
            return True
        except ProdutoNaoEncontradoException:
            return False
