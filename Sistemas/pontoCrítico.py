# Sistemas/pontoCritico.py
class PontoCritico:
    """
    Representa uma aresta na Tabela de Arestas (Edge Table) para o 
    algoritmo de preenchimento por varredura (Scanline).
    
    Atributos:
        ymax (int): A coordenada y máxima da aresta.
        x_interseccao (float): A coordenada x onde a aresta intercepta a linha de varredura atual.
        inv_slope (float): O inverso da inclinação da aresta (dx/dy).
    """
    def __init__(self, ymax, x_inicial, inv_slope):
        """
        Inicializa um objeto PontoCritico.

        Args:
            ymax (int): A coordenada y máxima da aresta.
            x_inicial (float): A coordenada x do vértice inferior da aresta.
            inv_slope (float): O inverso da inclinação (dx/dy).
        """
        self.ymax = ymax
        self.x_interseccao = x_inicial
        self.inv_slope = inv_slope

    def __lt__(self, other):
        """
        Método de comparação "menor que" (<).
        Permite que uma lista de arestas ativas seja ordenada pela coordenada x da interseção.

        Args:
            other (PontoCritico): O outro objeto a ser comparado.

        Returns:
            bool: True se a interseção x deste objeto for menor que a do outro.
        """
        return self.x_interseccao < other.x_interseccao