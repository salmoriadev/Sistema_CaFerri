from Excecoes.perfilRecomendadoNaoExisteException import PerfilRecomendadoNaoExisteException

class PerfilConsumidor:
    def __init__(self, perfil: str):
        self.__possiveis_perfis = ["Doce e Suave", "Ácido e Frutado", "Intenso e Encorpado", "Equilibrado e Completo"]
        if perfil not in self.__possiveis_perfis:
            raise PerfilRecomendadoNaoExisteException(perfil)
        self.__perfil = perfil

    @property
    def perfil(self):
        return self.__perfil

    @property
    def possiveis_perfis(self):
        return self.__possiveis_perfis

    def recomendar_cafes(self):
        recomendacoes = {
            "Doce e Suave": ["Café com Notas de Caramelo", "Café de Processo Natural"],
            "Ácido e Frutado": ["Café com Acidez Cítrica", "Café de Processo Lavado", "Cafés Florais"],
            "Intenso e Encorpado": ["Café de Torra Média Escura", "Café com Notas de Cacau"],
            "Equilibrado e Completo": ["Cafés com Notas de Baunilha", "Café de Processo Honey"]
        }
        return recomendacoes.get(self.__perfil, [])