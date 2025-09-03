# curvas.py
import math
from bresenham import Bresenham

class Curvas:
    """
    Gera os pontos para uma Curva de Bézier usando o algoritmo de De Casteljau
    e rasteriza a curva usando o algoritmo de Bresenham.
    """
    def __init__(self, pontos_controle: list):
        self.saida = []
        if len(pontos_controle) < 2:
            return
            
        self.pontos = []
        # Usa a distância entre o primeiro e o último ponto como uma estimativa
        # para determinar quantos segmentos desenhar, melhorando a suavidade.
        distancia = math.sqrt((pontos_controle[-1][0] - pontos_controle[0][0])**2 + (pontos_controle[-1][1] - pontos_controle[0][1])**2)
        
        # Garante um número mínimo de passos para curvas curtas
        n_pontos = max(100, round(distancia * 2))
        passo = 1.0 / n_pontos
        t = 0.0

        for _ in range(n_pontos + 1):
            self.pontos.append(self._casteljau(t, pontos_controle))
            t += passo

        self._rasterizar_curva()

    def _casteljau(self, t, pontos_controle):
        """Calcula um ponto na curva para um dado valor de 't'."""
        pts = [list(p) for p in pontos_controle]

        for i in range(1, len(pts)):
            for j in range(len(pts) - i):
                pts[j][0] = (1 - t) * pts[j][0] + t * pts[j + 1][0]
                pts[j][1] = (1 - t) * pts[j][1] + t * pts[j + 1][1]

        return [round(pts[0][0]), round(pts[0][1])]

    def _rasterizar_curva(self):
        """Conecta os pontos calculados da curva usando o algoritmo de Bresenham."""
        for i in range(len(self.pontos) - 1):
            # Evita desenhar segmentos de comprimento zero
            if self.pontos[i] != self.pontos[i+1]:
                linha = Bresenham(self.pontos[i], self.pontos[i + 1])
                self.saida.extend(linha.saida)