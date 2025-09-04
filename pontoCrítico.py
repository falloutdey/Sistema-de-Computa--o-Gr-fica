# ponto_critico.py
class PontoCritico:
    """
    Representa uma aresta na Tabela de Arestas para o algoritmo de varredura.
    """
    def __init__(self, ymax, x_inicial, inv_slope):
        self.ymax = ymax
        self.x_interseccao = x_inicial
        self.inv_slope = inv_slope

    def __lt__(self, other):
        # Permite que a lista de arestas seja ordenada pela coordenada x.
        return self.x_interseccao < other.x_interseccao