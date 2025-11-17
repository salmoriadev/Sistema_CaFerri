class EstoqueInsuficienteException(Exception):
    def __init__(self, nome_produto: str, quantidade_necessaria: int, quantidade_disponivel: int):
        super().__init__(
            f"Estoque insuficiente para '{nome_produto}'. Necessário: {quantidade_necessaria}, Disponível: {quantidade_disponivel}.")
