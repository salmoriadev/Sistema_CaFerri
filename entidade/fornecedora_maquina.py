from empresa_fornecedora import EmpresaFornecedora

class FornecedoraMaquina(EmpresaFornecedora):
    def __init__(self, nome: str, cnpj: str, endereco: str, telefone: str, pais_de_origem: str):
        super().__init__(nome, cnpj, endereco, telefone)
        self.__pais_de_origem = pais_de_origem

    @property
    def pais_de_origem(self):
        return self.__pais_de_origem
    
    @pais_de_origem.setter
    def pais_de_origem(self, novo_pais: str):
        self.__pais_de_origem = novo_pais