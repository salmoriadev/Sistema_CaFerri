"""
Representa uma empresa fornecedora de café no sistema.

Esta classe especializa EmpresaFornecedora, adicionando o atributo específico
tipo_cafe que identifica o tipo de café fornecido pela empresa. Herda dados
básicos de empresa (nome, CNPJ, endereço, telefone) e estabelece vínculo com
cafés cadastrados no sistema.

Utilizada para manter integridade referencial entre cafés e seus fornecedores,
permitindo validações antes de cadastrar novos cafés e análises de fornecedores
mais ativos em relatórios de negócio.
"""

from entidade.empresa_fornecedora import EmpresaFornecedora


class FornecedoraCafe(EmpresaFornecedora):
    def __init__(self, nome: str,
                 cnpj: str, endereco: str,
                 telefone: str, tipo_cafe: str) -> None:
        """
        Inicializa fornecedor de café com dados básicos de empresa (herdados
        de EmpresaFornecedora) e tipo específico de café fornecido. CNPJ é usado
        como chave única para identificação e validação de unicidade.
        """
        super().__init__(nome, cnpj, endereco, telefone)
        self.__tipo_cafe = tipo_cafe

    @property
    def tipo_cafe(self) -> str:
        return self.__tipo_cafe

    @tipo_cafe.setter
    def tipo_cafe(self, novo_tipo: str) -> None:
        self.__tipo_cafe = novo_tipo
