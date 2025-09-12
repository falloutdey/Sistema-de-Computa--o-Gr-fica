# Sistemas/circulo.py
class Circulo:
    """
    Gera os pontos de um círculo usando o Algoritmo do Ponto Médio.
    Este algoritmo calcula os pontos para um octante e depois espelha
    esses pontos para os outros sete octantes.
    """
    def __init__(self, centro, raio):
        """
        Inicializa a geração dos pontos do círculo.

        Args:
            centro (tuple): As coordenadas (x, y) do centro do círculo.
            raio (float or int): O raio do círculo.
        """
        self.saida = []
        raio = round(raio)
        self._rasterizar_circulo(centro, raio)

    def _rasterizar_circulo(self, centro, raio):
        """
        Executa o Algoritmo do Ponto Médio para calcular os pontos do círculo.
        
        Args:
            centro (tuple): O centro (cx, cy) do círculo.
            raio (int): O raio do círculo.
        """
        x = 0
        y = raio
        erro = 1 - raio  # Parâmetro de decisão inicial
        cx, cy = centro

        while x <= y:
            # Adiciona os pontos simétricos em todos os 8 octantes.
            self._adicionar_octantes(cx, cy, x, y)
            
            x += 1
            if erro < 0:
                erro += 2 * x + 1
            else:
                y -= 1
                erro += 2 * (x - y) + 1

    def _adicionar_octantes(self, cx, cy, x, y):
        """
        Adiciona os pontos para todos os 8 octantes, aproveitando a simetria do círculo.

        Args:
            cx (int): Coordenada x do centro.
            cy (int): Coordenada y do centro.
            x (int): Deslocamento horizontal a partir do centro.
            y (int): Deslocamento vertical a partir do centro.
        """
        self.saida.append([cx + x, cy + y])
        self.saida.append([cx + y, cy + x])
        self.saida.append([cx - y, cy + x])
        self.saida.append([cx - x, cy + y])
        self.saida.append([cx - x, cy - y])
        self.saida.append([cx - y, cy - x])
        self.saida.append([cx + y, cy - x])
        self.saida.append([cx + x, cy - y])