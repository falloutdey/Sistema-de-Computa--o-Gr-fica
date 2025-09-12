# Sistemas/curvas.py
import math
from Sistemas.bresenham import Bresenham

class Curvas:
    """
    Gera os pontos para uma Curva de Bézier usando o algoritmo de De Casteljau
    e rasteriza a curva conectando os pontos gerados com o algoritmo de Bresenham.
    """
    def __init__(self, pontos_controle: list):
        """
        Inicializa a geração da curva.

        Args:
            pontos_controle (list): Uma lista de tuplas (x, y) representando 
                                    os pontos de controle da curva.
        """
        self.saida = []
        if len(pontos_controle) < 2:
            return
            
        self.pontos = []
        # Usa a distância entre o primeiro e o último ponto de controle como uma 
        # estimativa para determinar o número de segmentos, melhorando a suavidade.
        distancia = math.sqrt((pontos_controle[-1][0] - pontos_controle[0][0])**2 + (pontos_controle[-1][1] - pontos_controle[0][1])**2)
        
        # Garante um número mínimo de passos para curvas curtas, evitando serrilhados.
        n_pontos = max(100, round(distancia * 2))
        passo = 1.0 / n_pontos
        t = 0.0

        # Calcula os pontos ao longo da curva usando o algoritmo de De Casteljau.
        for _ in range(n_pontos + 1):
            self.pontos.append(self._casteljau(t, pontos_controle))
            t += passo

        # Conecta os pontos calculados para formar a curva visível.
        self._rasterizar_curva()

    def _casteljau(self, t, pontos_controle):
        """
        Calcula um ponto na curva de Bézier para um dado valor de 't'
        usando interpolação linear recursiva.

        Args:
            t (float): O parâmetro da curva, variando de 0.0 a 1.0.
            pontos_controle (list): A lista de pontos de controle.

        Returns:
            list: As coordenadas [x, y] do ponto calculado na curva.
        """
        pts = [list(p) for p in pontos_controle]

        for i in range(1, len(pts)):
            for j in range(len(pts) - i):
                pts[j][0] = (1 - t) * pts[j][0] + t * pts[j + 1][0]
                pts[j][1] = (1 - t) * pts[j][1] + t * pts[j + 1][1]

        return [round(pts[0][0]), round(pts[0][1])]

    def _rasterizar_curva(self):
        """
        Conecta os pontos calculados da curva usando o algoritmo de Bresenham
        para formar uma linha contínua.
        """
        for i in range(len(self.pontos) - 1):
            # Evita desenhar segmentos de comprimento zero se pontos consecutivos forem iguais.
            if self.pontos[i] != self.pontos[i+1]:
                linha = Bresenham(self.pontos[i], self.pontos[i + 1])
                self.saida.extend(linha.saida)