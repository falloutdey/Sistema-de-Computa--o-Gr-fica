# recorte_linha.py
from bresenham import Bresenham

class RecorteLinha:
    def __init__(self, ponto_1, ponto_2, xmin, ymin, xmax, ymax):
        self.saida = []
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax

        self.ACIMA = 8
        self.ABAIXO = 4
        self.DIREITA = 2
        self.ESQUERDA = 1
        
        self.cohen_sutherland(list(ponto_1), list(ponto_2))

    def _calcular_codigo(self, ponto):
        x, y = ponto
        codigo = 0
        if x < self.xmin: codigo |= self.ESQUERDA
        elif x > self.xmax: codigo |= self.DIREITA
        if y < self.ymin: codigo |= self.ABAIXO
        elif y > self.ymax: codigo |= self.ACIMA
        return codigo

    def cohen_sutherland(self, ponto_1, ponto_2):
        codigo1 = self._calcular_codigo(ponto_1)
        codigo2 = self._calcular_codigo(ponto_2)
        aceite = False

        while True:
            if codigo1 == 0 and codigo2 == 0:
                aceite = True
                break
            elif (codigo1 & codigo2) != 0:
                break
            else:
                x, y = 0.0, 0.0
                codigo_fora = codigo1 if codigo1 != 0 else codigo2
                x1, y1 = ponto_1
                x2, y2 = ponto_2
                
                if codigo_fora & self.ACIMA:
                    x = x1 + (x2 - x1) * (self.ymax - y1) / (y2 - y1) if y1 != y2 else x1
                    y = float(self.ymax)
                elif codigo_fora & self.ABAIXO:
                    x = x1 + (x2 - x1) * (self.ymin - y1) / (y2 - y1) if y1 != y2 else x1
                    y = float(self.ymin)
                elif codigo_fora & self.DIREITA:
                    y = y1 + (y2 - y1) * (self.xmax - x1) / (x2 - x1) if x1 != x2 else y1
                    x = float(self.xmax)
                elif codigo_fora & self.ESQUERDA:
                    y = y1 + (y2 - y1) * (self.xmin - x1) / (x2 - x1) if x1 != x2 else y1
                    x = float(self.xmin)
                
                nx, ny = round(x), round(y)
                
                nx = max(self.xmin, min(self.xmax, nx))
                ny = max(self.ymin, min(self.ymax, ny))

                if codigo_fora == codigo1:
                    ponto_1[0], ponto_1[1] = nx, ny
                    codigo1 = self._calcular_codigo(ponto_1)
                else:
                    # --- CORREÇÃO DO BUG AQUI ---
                    ponto_2[0], ponto_2[1] = nx, ny # Estava 'ny, ny'
                    codigo2 = self._calcular_codigo(ponto_2)

        if aceite:
            linha_recortada = Bresenham(ponto_1, ponto_2)
            self.saida = linha_recortada.saida