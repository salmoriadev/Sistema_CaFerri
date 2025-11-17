""" Esta classe é uma implementação concreta da classe base abstrata
    `EmpresaFornecedora`. Ela herda todas as características fundamentais de
    um fornecedor, como `nome`, `cnpj`, `endereco` e `telefone`, garantindo
    uma estrutura de dados consistente para todos os tipos de parceiros
    comerciais."""


from entidade.empresa_fornecedora import EmpresaFornecedora


class FornecedoraMaquina(EmpresaFornecedora):
    def __init__(self, nome: str, cnpj: str,
                 endereco: str, telefone: str,
                 pais_de_origem: str) -> None:
        super().__init__(nome, cnpj, endereco, telefone)
        self.__pais_de_origem = pais_de_origem

    @property
    def pais_de_origem(self) -> str:
        return self.__pais_de_origem

    @pais_de_origem.setter
    def pais_de_origem(self, novo_pais: str) -> None:
        self.__pais_de_origem = novo_pais
