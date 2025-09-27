class PerfilConsumidor:
    def __init__(self, perfil: str):
        self.__perfil = perfil
        self.__cafes_recomendados = self.recomendar_cafes()
        self.__possiveis_perfis = ["Doce e Suave", "Ácido e Frutado", "Intenso e Encorpado", "Equilibrado e Completo"]

    @property
    def perfil(self):
        return self.__perfil

    @property
    def cafes_recomendados(self):
        return self.__cafes_recomendados

    @property
    def possiveis_perfis(self):
        return self.__possiveis_perfis

    @cafes_recomendados.setter
    def cafes_recomendados(self, novas_recomendacoes: list):
        self.__cafes_recomendados = novas_recomendacoes

    def recomendar_cafes(self):
        recomendacoes = {
            "Doce e Suave": ["Café com Notas de Caramelo", "Café de Processo Natural"],
            "Ácido e Frutado": ["Café com Acidez Cítrica", "Café de Processo Lavado", "Cafés Florais"],
            "Intenso e Encorpado": ["Café de Torra Média Escura", "Café com Notas de Cacau"],
            "Equilibrado e Completo": ["Cafés com Notas de Baunilha", "Café de Processo Honey"]
            }
        return recomendacoes.get(self.__perfil, ["Café Arábica de Torra Média"])
