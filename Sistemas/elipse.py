# Sistemas/elipse.py
class Elipse:
    """
    Gera os pontos de uma elipse usando o Algoritmo do Ponto Médio.
    O algoritmo é dividido em duas regiões para otimizar o cálculo.
    """
    def __init__(self, centro, raio_x, raio_y):
        """
        Inicializa a geração dos pontos da elipse.

        Args:
            centro (tuple): As coordenadas (x, y) do centro.
            raio_x (float or int): O raio no eixo x.
            raio_y (float or int): O raio no eixo y.
        """
        self.saida = []
        rx = round(raio_x)
        ry = round(raio_y)
        self._algoritmo_midpoint_elipse(centro, rx, ry)

    def _plot_elipse_points(self, cx, cy, x, y):
        """
        Adiciona os pontos simétricos nos quatro quadrantes da elipse.

        Args:
            cx (int): Coordenada x do centro.
            cy (int): Coordenada y do centro.
            x (int): Deslocamento horizontal a partir do centro.
            y (int): Deslocamento vertical a partir do centro.
        """
        self.saida.append([cx + x, cy + y])
        self.saida.append([cx - x, cy + y])
        self.saida.append([cx + x, cy - y])
        self.saida.append([cx - x, cy - y])

    def _algoritmo_midpoint_elipse(self, centro, rx, ry):
        """
        Executa o Algoritmo do Ponto Médio para elipses.

        Args:
            centro (tuple): O centro (cx, cy) da elipse.
            rx (int): O raio no eixo x.
            ry (int): O raio no eixo y.
        """
        if rx <= 0 or ry <= 0:
            return

        cx, cy = centro
        ry2 = ry * ry
        rx2 = rx * rx
        
        # --- Região 1 ---
        # Nesta região, a inclinação da curva é < -1.
        x = 0
        y = ry
        p1 = ry2 - (rx2 * ry) + (0.25 * rx2)
        dx = 2 * ry2 * x
        dy = 2 * rx2 * y

        while dx < dy:
            self._plot_elipse_points(cx, cy, x, y)
            x += 1
            dx += (2 * ry2)
            if p1 < 0:
                p1 += dx + ry2
            else:
                y -= 1
                dy -= (2 * rx2)
                p1 += dx - dy + ry2
        
        # --- Região 2 ---
        # Nesta região, a inclinação da curva é >= -1.
        p2 = (ry2 * (x + 0.5)**2) + (rx2 * (y - 1)**2) - (rx2 * ry2)
        
        while y >= 0:
            self._plot_elipse_points(cx, cy, x, y)
            y -= 1
            dy -= (2 * rx2)
            if p2 > 0:
                p2 += rx2 - dy
            else:
                x += 1
                dx += (2 * ry2)
                p2 += dx - dy + rx2