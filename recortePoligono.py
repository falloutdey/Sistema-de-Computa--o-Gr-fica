# recorte_poligono.py
from polilinha import Polilinha

class RecortePoligono:
    def __init__(self, pts_poligono: list, xmin, ymin, xmax, ymax):
        self.saida = []
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax

        # Aplica o recorte para cada uma das 4 arestas da janela
        vertices_recortados = self._recortar(pts_poligono, 'esquerda')
        vertices_recortados = self._recortar(vertices_recortados, 'direita')
        vertices_recortados = self._recortar(vertices_recortados, 'baixo')
        vertices_recortados = self._recortar(vertices_recortados, 'cima')

        # Se o recorte resultar num polígono válido, prepara-o para ser desenhado
        if len(vertices_recortados) > 1:
            poligono_final = Polilinha(vertices_recortados, fechar=True)
            self.saida = poligono_final.saida

    def _esta_dentro(self, ponto, aresta):
        if aresta == 'esquerda': return ponto[0] >= self.xmin
        if aresta == 'direita': return ponto[0] <= self.xmax
        if aresta == 'baixo': return ponto[1] >= self.ymin
        if aresta == 'cima': return ponto[1] <= self.ymax
        return False

    def _calcular_interseccao(self, p1, p2, aresta):
        x1, y1 = p1
        x2, y2 = p2
        dx, dy = x2 - x1, y2 - y1

        if aresta == 'esquerda':
            y = y1 + dy * (self.xmin - x1) / dx if dx != 0 else y1
            return [self.xmin, round(y)]
        if aresta == 'direita':
            y = y1 + dy * (self.xmax - x1) / dx if dx != 0 else y1
            return [self.xmax, round(y)]
        if aresta == 'baixo':
            x = x1 + dx * (self.ymin - y1) / dy if dy != 0 else x1
            return [round(x), self.ymin]
        if aresta == 'cima':
            x = x1 + dx * (self.ymax - y1) / dy if dy != 0 else x1
            return [round(x), self.ymax]
        return [0, 0]

    def _recortar(self, pontos, aresta):
        novo_poligono = []
        num_pontos = len(pontos)
        for i in range(num_pontos):
            p1 = pontos[i]
            p2 = pontos[(i + 1) % num_pontos]

            p1_dentro = self._esta_dentro(p1, aresta)
            p2_dentro = self._esta_dentro(p2, aresta)

            if p1_dentro and p2_dentro: # Caso 1: Ambos dentro
                novo_poligono.append(p2)
            elif p1_dentro and not p2_dentro: # Caso 2: P1 dentro, P2 fora
                novo_poligono.append(self._calcular_interseccao(p1, p2, aresta))
            elif not p1_dentro and p2_dentro: # Caso 3: P1 fora, P2 dentro
                novo_poligono.append(self._calcular_interseccao(p1, p2, aresta))
                novo_poligono.append(p2)
            # Caso 4 (Ambos fora) não faz nada
        
        return novo_poligono