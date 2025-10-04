from entidade.empresa_fornecedora import EmpresaFornecedora
class FornecedoraCafe(EmpresaFornecedora):
    def __init__(self, nome: str, cnpj: str, endereco: str, telefone: str, tipo_cafe: str) -> None:
        super().__init__(nome, cnpj, endereco, telefone)
        self.__tipo_cafe = tipo_cafe

    @property
    def tipo_cafe(self) -> str:
        return self.__tipo_cafe