# Sistemas/recorteLinha.py
from Sistemas.bresenham import Bresenham

class RecorteLinha:
    """
    Implementa o algoritmo de recorte de linha de Cohen-Sutherland.
    Este algoritmo determina eficientemente quais segmentos de linha estão
    dentro de uma janela de recorte retangular.
    """
    def __init__(self, ponto_1, ponto_2, xmin, ymin, xmax, ymax):
        """
        Inicializa o processo de recorte de linha.

        Args:
            ponto_1 (tuple): O ponto inicial (x, y) da linha.
            ponto_2 (tuple): O ponto final (x, y) da linha.
            xmin (float/int): A coordenada x mínima da janela de recorte.
            ymin (float/int): A coordenada y mínima da janela de recorte.
            xmax (float/int): A coordenada x máxima da janela de recorte.
            ymax (float/int): A coordenada y máxima da janela de recorte.
        """
        self.saida = []
        self.xmin = float(xmin)
        self.xmax = float(xmax)
        self.ymin = float(ymin)
        self.ymax = float(ymax)

        # Códigos de região (bit flags)
        self.ACIMA = 8   # 1000
        self.ABAIXO = 4  # 0100
        self.DIREITA = 2 # 0010
        self.ESQUERDA = 1# 0001
        
        # Converte os pontos para float para manter a precisão nos cálculos de interseção.
        p1_float = [float(ponto_1[0]), float(ponto_1[1])]
        p2_float = [float(ponto_2[0]), float(ponto_2[1])]
        
        self.cohen_sutherland(p1_float, p2_float)

    def _calcular_codigo(self, ponto):
        """
        Calcula o código de região de 4 bits para um ponto, indicando sua
        posição em relação à janela de recorte.

        Args:
            ponto (list/tuple): O ponto [x, y].

        Returns:
            int: O código de região.
        """
        x, y = ponto
        codigo = 0
        if x < self.xmin: codigo |= self.ESQUERDA
        elif x >= self.xmax: codigo |= self.DIREITA
        if y < self.ymin: codigo |= self.ABAIXO
        elif y >= self.ymax: codigo |= self.ACIMA
        return codigo

    def _limitar_valor(self, valor, min_val, max_val):
        """Garante que um valor fique dentro do intervalo [min_val, max_val]."""
        return max(min_val, min(valor, max_val))


    def cohen_sutherland(self, ponto_1, ponto_2):
        """
        Executa o algoritmo de Cohen-Sutherland.

        Args:
            ponto_1 (list): O ponto inicial [x, y] da linha.
            ponto_2 (list): O ponto final [x, y] da linha.
        """
        codigo1 = self._calcular_codigo(ponto_1)
        codigo2 = self._calcular_codigo(ponto_2)
        aceite = False

        while True:
            # Caso 1: Ambos os pontos estão dentro da janela (aceite trivial).
            if codigo1 == 0 and codigo2 == 0:
                aceite = True
                break
            # Caso 2: Ambos os pontos estão fora da janela, na mesma região (rejeição trivial).
            elif (codigo1 & codigo2) != 0:
                break
            # Caso 3: Recorte necessário.
            else:
                x, y = 0.0, 0.0
                # Escolhe um ponto que está fora.
                codigo_fora = codigo1 if codigo1 != 0 else codigo2
                x1, y1 = ponto_1
                x2, y2 = ponto_2
                
                # Calcula o ponto de interseção com a borda da janela.
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
                
                # Atualiza o ponto que estava fora com a nova interseção.
                if codigo_fora == codigo1:
                    ponto_1[0], ponto_1[1] = x, y
                    codigo1 = self._calcular_codigo(ponto_1)
                else:
                    ponto_2[0], ponto_2[1] = x, y
                    codigo2 = self._calcular_codigo(ponto_2)

        if aceite:
            # Se a linha foi aceita, arredonda para inteiros e rasteriza.
            p1_int = [self._limitar_valor(round(ponto_1[0]), self.xmin, self.xmax),
                      self._limitar_valor(round(ponto_1[1]), self.ymin, self.ymax)]
            p2_int = [self._limitar_valor(round(ponto_2[0]), self.xmin, self.xmax),
                      self._limitar_valor(round(ponto_2[1]), self.ymin, self.ymax)]
            linha_recortada = Bresenham(p1_int, p2_int)
            self.saida = linha_recortada.saida