# Sistemas/recortePoligono.py
from Sistemas.polilinha import Polilinha

class RecortePoligono:
    """
    Implementa o algoritmo de recorte de polígono de Sutherland-Hodgman.
    Este algoritmo recorta um polígono contra cada uma das quatro arestas
    de uma janela de recorte retangular.
    """
    def __init__(self, pts_poligono: list, xmin, ymin, xmax, ymax):
        """
        Inicializa o processo de recorte de polígono.

        Args:
            pts_poligono (list): Uma lista de vértices (x, y) do polígono.
            xmin, ymin, xmax, ymax (float/int): As coordenadas da janela de recorte.
        """
        self.saida = []
        self.xmin = float(xmin)
        self.xmax = float(xmax)
        self.ymin = float(ymin)
        self.ymax = float(ymax)

        vertices_float = [[float(p[0]), float(p[1])] for p in pts_poligono]

        # Aplica o recorte sequencialmente para cada aresta da janela.
        vertices_recortados = self._recortar(vertices_float, 'esquerda')
        vertices_recortados = self._recortar(vertices_recortados, 'direita')
        vertices_recortados = self._recortar(vertices_recortados, 'baixo')
        vertices_recortados = self._recortar(vertices_recortados, 'cima')

        # Se o recorte resultar num polígono válido, prepara-o para ser desenhado.
        if len(vertices_recortados) > 1:
            poligono_final = Polilinha(vertices_recortados, fechar=True)
            self.saida = [[self._limitar_valor(v[0], self.xmin, self.xmax),
                           self._limitar_valor(v[1], self.ymin, self.ymax)] for v in poligono_final.saida]

    def _esta_dentro(self, ponto, aresta):
        """
        Verifica se um ponto está 'dentro' de uma aresta da janela de recorte.

        Args:
            ponto (list): O ponto [x, y].
            aresta (str): O nome da aresta ('esquerda', 'direita', 'baixo', 'cima').

        Returns:
            bool: True se o ponto está do lado visível da aresta.
        """
        if aresta == 'esquerda': return ponto[0] >= self.xmin
        if aresta == 'direita': return ponto[0] < self.xmax
        if aresta == 'baixo': return ponto[1] >= self.ymin
        if aresta == 'cima': return ponto[1] < self.ymax
        return False

    def _limitar_valor(self, valor, min_val, max_val):
        """Garante que um valor fique dentro do intervalo [min_val, max_val-1]."""
        return max(min_val, min(valor, max_val - 1))

    def _calcular_interseccao(self, p1, p2, aresta):
        """
        Calcula o ponto de interseção entre um segmento de linha (p1, p2) e uma aresta da janela.

        Args:
            p1, p2 (list): Os pontos inicial e final do segmento de linha.
            aresta (str): O nome da aresta da janela.

        Returns:
            list: As coordenadas [x, y] do ponto de interseção.
        """
        x1, y1 = p1
        x2, y2 = p2
        dx, dy = x2 - x1, y2 - y1

        if aresta == 'esquerda':
            y = y1 + dy * (self.xmin - x1) / dx if dx != 0 else y1
            return [self.xmin, y]
        if aresta == 'direita':
            y = y1 + dy * (self.xmax - 1 - x1) / dx if dx != 0 else y1
            return [self.xmax - 1, y]
        if aresta == 'baixo':
            x = x1 + dx * (self.ymin - y1) / dy if dy != 0 else x1
            return [x, self.ymin]
        if aresta == 'cima':
            x = x1 + dx * (self.ymax - 1 - y1) / dy if dy != 0 else x1
            return [x, self.ymax - 1]
        return [0.0, 0.0]

    def _recortar(self, pontos, aresta):
        """
        Recorta uma lista de vértices contra uma única aresta da janela.

        Args:
            pontos (list): A lista de vértices do polígono.
            aresta (str): A aresta contra a qual recortar.

        Returns:
            list: A nova lista de vértices do polígono recortado.
        """
        novo_poligono = []
        num_pontos = len(pontos)
        for i in range(num_pontos):
            p1 = pontos[i]
            p2 = pontos[(i + 1) % num_pontos]

            p1_dentro = self._esta_dentro(p1, aresta)
            p2_dentro = self._esta_dentro(p2, aresta)

            # Caso 1: Ambos os pontos dentro -> adiciona o segundo ponto.
            if p1_dentro and p2_dentro:
                novo_poligono.append(p2)
            # Caso 2: P1 dentro, P2 fora -> adiciona a interseção.
            elif p1_dentro and not p2_dentro:
                novo_poligono.append(self._calcular_interseccao(p1, p2, aresta))
            # Caso 3: P1 fora, P2 dentro -> adiciona a interseção e o segundo ponto.
            elif not p1_dentro and p2_dentro:
                novo_poligono.append(self._calcular_interseccao(p1, p2, aresta))
                novo_poligono.append(p2)
            # Caso 4: Ambos fora -> não faz nada.

        return novo_poligono