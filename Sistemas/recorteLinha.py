# recorteLinha.py
from Sistemas.bresenham import Bresenham

class RecorteLinha:
    def __init__(self, ponto_1, ponto_2, xmin, ymin, xmax, ymax):
        self.saida = []
        self.xmin = float(xmin)
        self.xmax = float(xmax)
        self.ymin = float(ymin)
        self.ymax = float(ymax)

        self.ACIMA = 8
        self.ABAIXO = 4
        self.DIREITA = 2
        self.ESQUERDA = 1
        
        # Converte os pontos de entrada para float para manter a precisão
        p1_float = [float(ponto_1[0]), float(ponto_1[1])]
        p2_float = [float(ponto_2[0]), float(ponto_2[1])]
        
        self.cohen_sutherland(p1_float, p2_float)

    def _calcular_codigo(self, ponto):
        x, y = ponto
        codigo = 0
        if x < self.xmin: codigo |= self.ESQUERDA
        elif x > self.xmax - 1: codigo |= self.DIREITA
        if y < self.ymin: codigo |= self.ABAIXO
        elif y > self.ymax - 1: codigo |= self.ACIMA
        return codigo

    def _limitar_valor(self, valor, min_val, max_val):
        """Garante que o valor fique dentro do intervalo [min_val, max_val-1]."""
        return max(min_val, min(valor, max_val - 1))

    def cohen_sutherland(self, ponto_1, ponto_2):
        codigo1 = self._calcular_codigo(ponto_1)
        codigo2 = self._calcular_codigo(ponto_2)
        aceite = False

        while True:
            if codigo1 == 0 and codigo2 == 0:  # Ambos dentro
                aceite = True
                break
            elif (codigo1 & codigo2) != 0:  # Ambos fora e na mesma região
                break
            else:  # Recorte necessário
                x, y = 0.0, 0.0
                codigo_fora = codigo1 if codigo1 != 0 else codigo2
                x1, y1 = ponto_1
                x2, y2 = ponto_2
                
                if codigo_fora & self.ACIMA:
                    x = x1 + (x2 - x1) * (self.ymax - 1 - y1) / (y2 - y1) if y1 != y2 else x1
                    y = self.ymax - 1
                elif codigo_fora & self.ABAIXO:
                    x = x1 + (x2 - x1) * (self.ymin - y1) / (y2 - y1) if y1 != y2 else x1
                    y = self.ymin
                elif codigo_fora & self.DIREITA:
                    y = y1 + (y2 - y1) * (self.xmax - 1 - x1) / (x2 - x1) if x1 != x2 else y1
                    x = self.xmax - 1
                elif codigo_fora & self.ESQUERDA:
                    y = y1 + (y2 - y1) * (self.xmin - x1) / (x2 - x1) if x1 != x2 else y1
                    x = self.xmin
                
                if codigo_fora == codigo1:
                    ponto_1[0], ponto_1[1] = x, y
                    codigo1 = self._calcular_codigo(ponto_1)
                else:
                    ponto_2[0], ponto_2[1] = x, y
                    codigo2 = self._calcular_codigo(ponto_2)

        if aceite:
            # Arredonda para inteiros apenas no final e limita dentro da janela
            p1_int = [self._limitar_valor(round(ponto_1[0]), self.xmin, self.xmax),
                      self._limitar_valor(round(ponto_1[1]), self.ymin, self.ymax)]
            p2_int = [self._limitar_valor(round(ponto_2[0]), self.xmin, self.xmax),
                      self._limitar_valor(round(ponto_2[1]), self.ymin, self.ymax)]
            linha_recortada = Bresenham(p1_int, p2_int)
            self.saida = linha_recortada.saida
