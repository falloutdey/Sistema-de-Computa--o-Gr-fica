# circulo.py
class Circulo:
    """
    Gera os pontos de um círculo usando o Algoritmo do Ponto Médio.
    """
    def __init__(self, centro, raio):
        self.saida = []
        raio = round(raio)
        self._rasterizar_circulo(centro, raio)

    def _rasterizar_circulo(self, centro, raio):
        x = 0
        y = raio
        erro = 1 - raio  # Ponto inicial de decisão
        cx, cy = centro

        while x <= y:
            # Adiciona os pontos em todos os 8 octantes
            self._adicionar_octantes(cx, cy, x, y)
            
            x += 1
            if erro < 0:
                erro += 2 * x + 1
            else:
                y -= 1
                erro += 2 * (x - y) + 1

    def _adicionar_octantes(self, cx, cy, x, y):
        self.saida.append([cx + x, cy + y])
        self.saida.append([cx + y, cy + x])
        self.saida.append([cx - y, cy + x])
        self.saida.append([cx - x, cy + y])
        self.saida.append([cx - x, cy - y])
        self.saida.append([cx - y, cy - x])
        self.saida.append([cx + y, cy - x])
        self.saida.append([cx + x, cy - y])