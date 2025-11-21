"""
    Representa a entidade 'Café', detalhando suas características específicas.

    Como uma classe filha de `Produto`, `Cafe` herda todas as propriedades
    comerciais básicas, como ID, nome e preços. No entanto, ela expande
    significativamente essa base com atributos que descrevem as qualidades
    únicas do grão, incluindo `origem`, `variedade`, `altitude`, `moagem` e
    `notas_sensoriais`.
    """
from entidade.fornecedora_cafe import FornecedoraCafe
from entidade.produto import Produto
from entidade.perfil_consumidor import PerfilConsumidor


class Cafe(Produto):
    def __init__(self, nome: str, preco_compra: float, preco_venda: float,
                 id: int, data_fabricacao: str, origem: str, variedade: str,
                 altitude: int, moagem: str, notas_sensoriais: str,
                 perfil_recomendado: str, empresa_fornecedora: FornecedoraCafe) -> None:
        """
        Inicializa um café com dados comerciais básicos (herdados de Produto)
        e características específicas de café (origem, variedade, altitude,
        moagem, notas sensoriais). Cria instância de PerfilConsumidor para
        perfil recomendado e associa fornecedor de café.
        """
        if altitude < 0:
            raise ValueError("A altitude não pode ser negativa.")
        super().__init__(nome, preco_compra, preco_venda, id, data_fabricacao)
        self.__origem = origem
        self.__variedade = variedade
        self.__altitude = altitude
        self.__moagem = moagem
        self.__notas_sensoriais = notas_sensoriais
        self.__perfil_recomendado = PerfilConsumidor(perfil_recomendado)
        self.__empresa_fornecedora = empresa_fornecedora

    @property
    def origem(self) -> str:
        return self.__origem

    @property
    def variedade(self) -> str:
        return self.__variedade

    @property
    def altitude(self) -> int:
        return self.__altitude

    @property
    def moagem(self) -> str:
        return self.__moagem

    @property
    def notas_sensoriais(self) -> str:
        return self.__notas_sensoriais

    @property
    def perfil_recomendado(self) -> PerfilConsumidor:
        return self.__perfil_recomendado

    @property
    def empresa_fornecedora(self) -> FornecedoraCafe:
        return self.__empresa_fornecedora

    @perfil_recomendado.setter
    def perfil_recomendado(self, perfil: str) -> None:
        self.__perfil_recomendado = PerfilConsumidor(perfil)

    @moagem.setter
    def moagem(self, tipo_moagem: str) -> None:
        self.__moagem = tipo_moagem

    @notas_sensoriais.setter
    def notas_sensoriais(self, notas: str) -> None:
        self.__notas_sensoriais = notas

    @altitude.setter
    def altitude(self, nova_altitude: int) -> None:
        if nova_altitude < 0:
            raise ValueError("A altitude não pode ser negativa.")
        self.__altitude = nova_altitude

    @variedade.setter
    def variedade(self, nova_variedade: str) -> None:
        self.__variedade = nova_variedade

    @origem.setter
    def origem(self, nova_origem: str) -> None:
        self.__origem = nova_origem

    @empresa_fornecedora.setter
    def empresa_fornecedora(self, nova_empresa: FornecedoraCafe) -> None:
        self.__empresa_fornecedora = nova_empresa
