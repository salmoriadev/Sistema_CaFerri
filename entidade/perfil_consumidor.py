"""
    Representa e gerencia o perfil de sabor de um consumidor de café.

    Esta classe funciona como um objeto de valor que encapsula as preferências
    de um cliente. Ao ser instanciada, ela valida se o perfil fornecido
    existe em uma lista predefinida de perfis válidos (ex: "Doce e Suave",
    "Ácido e Frutado"). Se o perfil for inválido, uma exceção
    `PerfilRecomendadoNaoExisteException` é lançada para garantir a
    integridade dos dados.
    """

from Excecoes.perfilRecomendadoNaoExisteException import PerfilRecomendadoNaoExisteException

class PerfilConsumidor:
    def __init__(self, perfil: str) -> None:
        self.__possiveis_perfis = ["Doce e Suave", "Ácido e Frutado", "Intenso e Encorpado", "Equilibrado e Completo"]
        if perfil not in self.__possiveis_perfis:
            raise PerfilRecomendadoNaoExisteException(perfil)
        self.__perfil = perfil

    @property
    def perfil(self) -> str:
        return self.__perfil

    @property
    def possiveis_perfis(self) -> list[str]:
        return self.__possiveis_perfis

    def recomendar_cafes(self) -> list[str]:
        recomendacoes = {
            "Doce e Suave": ["Café com Notas de Caramelo", "Café de Processo Natural"],
            "Ácido e Frutado": ["Café com Acidez Cítrica", "Café de Processo Lavado", "Cafés Florais"],
            "Intenso e Encorpado": ["Café de Torra Média Escura", "Café com Notas de Cacau"],
            "Equilibrado e Completo": ["Cafés com Notas de Baunilha", "Café de Processo Honey"]
        }
        return recomendacoes.get(self.__perfil, [])