# transformacao.py
import math
import numpy as np

class Transformacao:
    """
    Aplica transformações geométricas a um conjunto de vértices de um polígono.
    """
    def __init__(self, vertices_poligono):
        # Armazena os vértices como uma lista de listas
        self.vertices = [list(p) for p in vertices_poligono]

    def transladar(self, dx, dy):
        """Aplica uma translação."""
        matriz_translacao = np.array([
            [1, 0, dx],
            [0, 1, dy],
            [0, 0, 1]
        ])
        self._aplicar_matriz(matriz_translacao)

    def escalonar(self, sx, sy, ponto_fixo):
        """Aplica uma escala em relação a um ponto fixo."""
        px, py = ponto_fixo
        matriz_escala = (
            np.array([[1, 0, px], [0, 1, py], [0, 0, 1]]) @
            np.array([[sx, 0, 0], [0, sy, 0], [0, 0, 1]]) @
            np.array([[1, 0, -px], [0, 1, -py], [0, 0, 1]])
        )
        self._aplicar_matriz(matriz_escala)

    def rotacionar(self, angulo_graus, pivo):
        """Aplica uma rotação em relação a um ponto de pivô."""
        px, py = pivo
        angulo_rad = math.radians(angulo_graus)
        cos_a = math.cos(angulo_rad)
        sin_a = math.sin(angulo_rad)
        
        matriz_rotacao = (
            np.array([[1, 0, px], [0, 1, py], [0, 0, 1]]) @
            np.array([[cos_a, -sin_a, 0], [sin_a, cos_a, 0], [0, 0, 1]]) @
            np.array([[1, 0, -px], [0, 1, -py], [0, 0, 1]])
        )
        self._aplicar_matriz(matriz_rotacao)

    def _aplicar_matriz(self, matriz):
        """Aplica uma matriz de transformação a todos os vértices do polígono."""
        novos_vertices = []
        for vertice in self.vertices:
            ponto_homogeneo = np.array([vertice[0], vertice[1], 1])
            ponto_transformado = matriz @ ponto_homogeneo
            novos_vertices.append([round(ponto_transformado[0]), round(ponto_transformado[1])])
        self.vertices = novos_vertices