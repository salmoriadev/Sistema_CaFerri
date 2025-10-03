class IDJaExistenteException(Exception):
    def __init__(self, tipo_objeto: str):
        super().__init__(f"ERRO: Já existe um(a) {tipo_objeto} com este ID.")