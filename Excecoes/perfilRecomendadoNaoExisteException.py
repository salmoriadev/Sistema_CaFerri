class PerfilRecomendadoNaoExisteException(Exception):
    def __init__(self, perfil: str):
        self.mensagem = "Perfil recomendado '{}' não existe.".format(perfil)
        super().__init__(self.mensagem)
