""" Esta classe é uma implementação concreta da classe base abstrata
    `EmpresaFornecedora`. Ela herda todas as características fundamentais de
    um fornecedor, como `nome`, `cnpj`, `endereco` e `telefone`, garantindo
    uma estrutura de dados consistente para todos os tipos de parceiros
    comerciais."""

from entidade.empresa_fornecedora import EmpresaFornecedora
class FornecedoraCafe(EmpresaFornecedora):
    def __init__(self, nome: str, cnpj: str, endereco: str, telefone: str, tipo_cafe: str) -> None:
        super().__init__(nome, cnpj, endereco, telefone)
        self.__tipo_cafe = tipo_cafe

    @property
    def tipo_cafe(self) -> str:
        return self.__tipo_cafe
    
    @tipo_cafe.setter
    def tipo_cafe(self, novo_tipo: str) -> None:
        self.__tipo_cafe = novo_tipo