"""
Exceção lançada quando um fornecedor não é encontrado no repositório.

Esta exceção é usada pelos controladores de fornecedores (café e máquinas)
quando uma busca por CNPJ não encontra o fornecedor solicitado. Permite que
controladores validem existência de fornecedores antes de criar produtos
associados, mantendo integridade referencial.
"""

class FornecedorNaoEncontradoException(Exception):
    def __init__(self):
        super().__init__("Fornecedor não encontrado.")
