class PerfilConsumidor:
    def __init__(self, perfil: str):
        self.__perfil = perfil
        self.__cafes_recomendados = []

    @property
    def perfil(self):
        return self.__perfil

    @property
    def preferencias(self):
        return self.__preferencias
    
    @preferencias.setter
    def preferencias(self, novas_preferencias: list):
        self.__preferencias = novas_preferencias

    def recomendar_cafes(self):
        recomendacoes = {
            "Doce e Suave": ["Café com Notas de Caramelo", "Café de Processo Natural"],
            "Ácido e Frutado": ["Café com Acidez Cítrica", "Café de Processo Lavado", "Cafés Florais"],
            "Intenso e Encorpado": ["Café de Torra Média Escura", "Café com Notas de Cacau"],
            "Equilibrado e Completo": ["Cafés com Notas de Baunilha", "Café de Processo Honey"]
            }
        return recomendacoes.get(self.__perfil, ["Café Arábica de Torra Média"])
    