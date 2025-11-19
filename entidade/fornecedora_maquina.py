"""
Representa uma empresa fornecedora de máquinas de café no sistema.

Esta classe especializa EmpresaFornecedora, adicionando o atributo específico
pais_de_origem que identifica a origem geográfica das máquinas fornecidas.
Herda dados básicos de empresa (nome, CNPJ, endereço, telefone) e estabelece
vínculo com máquinas cadastradas no sistema.

Utilizada para manter integridade referencial entre máquinas e seus fornecedores,
permitindo validações antes de cadastrar novas máquinas e análises de fornecedores
mais ativos em relatórios de negócio.
"""


from entidade.empresa_fornecedora import EmpresaFornecedora


class FornecedoraMaquina(EmpresaFornecedora):
    def __init__(self, nome: str, cnpj: str,
                 endereco: str, telefone: str,
                 pais_de_origem: str) -> None:
        """
        Inicializa fornecedor de máquinas com dados básicos de empresa (herdados
        de EmpresaFornecedora) e país de origem das máquinas fornecidas. CNPJ é
        usado como chave única para identificação e validação de unicidade.
        """
        super().__init__(nome, cnpj, endereco, telefone)
        self.__pais_de_origem = pais_de_origem

    @property
    def pais_de_origem(self) -> str:
        return self.__pais_de_origem

    @pais_de_origem.setter
    def pais_de_origem(self, novo_pais: str) -> None:
        self.__pais_de_origem = novo_pais
