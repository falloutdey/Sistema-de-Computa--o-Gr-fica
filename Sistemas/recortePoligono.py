# recortePoligono.py
from Sistemas.polilinha import Polilinha

class RecortePoligono:
    def __init__(self, pts_poligono: list, xmin, ymin, xmax, ymax):
        self.saida = []
        self.xmin = float(xmin)
        self.xmax = float(xmax)
        self.ymin = float(ymin)
        self.ymax = float(ymax)

        # Converte os pontos de entrada para float para garantir a precisão
        vertices_float = [[float(p[0]), float(p[1])] for p in pts_poligono]

        # Aplica o recorte para cada uma das 4 arestas da janela
        vertices_recortados = self._recortar(vertices_float, 'esquerda')
        vertices_recortados = self._recortar(vertices_recortados, 'direita')
        vertices_recortados = self._recortar(vertices_recortados, 'baixo')
        vertices_recortados = self._recortar(vertices_recortados, 'cima')

        # Se o recorte resultar num polígono válido, prepara-o para ser desenhado
        if len(vertices_recortados) > 1:
            poligono_final = Polilinha(vertices_recortados, fechar=True)
            # Limita os valores finais dentro da janela
            self.saida = [[self._limitar_valor(v[0], self.xmin, self.xmax),
                           self._limitar_valor(v[1], self.ymin, self.ymax)] for v in poligono_final.saida]

    def _esta_dentro(self, ponto, aresta):
        if aresta == 'esquerda': return ponto[0] >= self.xmin
        if aresta == 'direita': return ponto[0] <= self.xmax - 1
        if aresta == 'baixo': return ponto[1] >= self.ymin
        if aresta == 'cima': return ponto[1] <= self.ymax - 1
        return False

    def _limitar_valor(self, valor, min_val, max_val):
        """Garante que o valor fique dentro do intervalo [min_val, max_val-1]."""
        return max(min_val, min(valor, max_val - 1))

    def _calcular_interseccao(self, p1, p2, aresta):
        x1, y1 = p1
        x2, y2 = p2
        dx, dy = x2 - x1, y2 - y1

        if aresta == 'esquerda':
            y = y1 + dy * (self.xmin - x1) / dx if dx != 0 else y1
            return [self.xmin, self._limitar_valor(y, self.ymin, self.ymax)]
        if aresta == 'direita':
            y = y1 + dy * (self.xmax - 1 - x1) / dx if dx != 0 else y1
            return [self.xmax - 1, self._limitar_valor(y, self.ymin, self.ymax)]
        if aresta == 'baixo':
            x = x1 + dx * (self.ymin - y1) / dy if dy != 0 else x1
            return [self._limitar_valor(x, self.xmin, self.xmax), self.ymin]
        if aresta == 'cima':
            x = x1 + dx * (self.ymax - 1 - y1) / dy if dy != 0 else x1
            return [self._limitar_valor(x, self.xmin, self.xmax), self.ymax - 1]
        return [0.0, 0.0]

    def _recortar(self, pontos, aresta):
        novo_poligono = []
        num_pontos = len(pontos)
        for i in range(num_pontos):
            p1 = pontos[i]
            p2 = pontos[(i + 1) % num_pontos]

            p1_dentro = self._esta_dentro(p1, aresta)
            p2_dentro = self._esta_dentro(p2, aresta)

            if p1_dentro and p2_dentro:  # Ambos dentro
                novo_poligono.append(p2)
            elif p1_dentro and not p2_dentro:  # P1 dentro, P2 fora
                novo_poligono.append(self._calcular_interseccao(p1, p2, aresta))
            elif not p1_dentro and p2_dentro:  # P1 fora, P2 dentro
                novo_poligono.append(self._calcular_interseccao(p1, p2, aresta))
                novo_poligono.append(p2)
            # Ambos fora -> não faz nada

        return novo_poligono
