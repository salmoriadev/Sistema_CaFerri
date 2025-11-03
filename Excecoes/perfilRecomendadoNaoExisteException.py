class PerfilRecomendadoNaoExisteException(Exception):
    def __init__(self, perfil: str):
        super().__init__(f"Perfil recomendado '{perfil}' não existe.")
