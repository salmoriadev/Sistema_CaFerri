class PerfilRecomendadoNaoExisteException(Exception):
    def __init__(self):
        self.mensagem = "Perfil recomendado não existe."
        super().__init__(self.mensagem)
