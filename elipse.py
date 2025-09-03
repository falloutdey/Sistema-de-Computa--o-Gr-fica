# elipse.py
class Elipse:
    """
    Gera os pontos de uma elipse usando o Algoritmo do Ponto Médio.
    """
    def __init__(self, centro, raio_x, raio_y):
        self.saida = []
        rx = round(raio_x)
        ry = round(raio_y)
        self._algoritmo_midpoint_elipse(centro, rx, ry)

    def _plot_elipse_points(self, cx, cy, x, y):
        self.saida.append([cx + x, cy + y])
        self.saida.append([cx - x, cy + y])
        self.saida.append([cx + x, cy - y])
        self.saida.append([cx - x, cy - y])

    def _algoritmo_midpoint_elipse(self, centro, rx, ry):
        if rx <= 0 or ry <= 0:
            return

        cx, cy = centro
        ry2 = ry * ry
        rx2 = rx * rx
        
        # Região 1
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
        
        # Região 2
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