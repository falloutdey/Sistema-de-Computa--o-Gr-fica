# Sistemas/bresenham.py
import math

class Bresenham:
    """
    Implementa o Algoritmo de Bresenham para rasterização de linhas.
    O algoritmo é otimizado para funcionar em todos os octantes através de reflexões.
    """
    def __init__(self, ponto1, ponto2):
        """
        Inicializa o algoritmo de Bresenham.

        Args:
            ponto1 (tuple): As coordenadas (x, y) do ponto inicial da linha.
            ponto2 (tuple): As coordenadas (x, y) do ponto final da linha.
        """
        self.saida = []
        self.x_inicial, self.y_inicial = ponto1
        self.x_final, self.y_final = ponto2

        self.pontosFinais = []
        self.troca_x = self.troca_y = self.troca_xy = False

        # Se os pontos são iguais, a linha é um único ponto.
        if ponto1 == ponto2:
            self.saida = [list(ponto1)]
            return

        # Prepara as coordenadas para o algoritmo base (primeiro octante).
        self.calcular_octante()

        # Calcula os deltas e o erro inicial.
        delta_x = self.x_final - self.x_inicial
        delta_y = self.y_final - self.y_inicial
        m = delta_y / delta_x if delta_x != 0 else float('inf')
        erro = m - 0.5

        # Gera os pontos da linha no primeiro octante.
        aux_x, aux_y = self.x_inicial, self.y_inicial
        self.pontosFinais.append([aux_x, aux_y])

        while aux_x < self.x_final:
            if erro >= 0:
                aux_y += 1
                erro -= 1
            aux_x += 1
            erro += m
            self.pontosFinais.append([aux_x, aux_y])

        # Aplica a reflexão inversa para trazer os pontos para o octante original.
        self.aplicar_reflexao(self.pontosFinais)
        self.saida = self.pontosFinais

    def calcular_octante(self):
        """
        Transforma as coordenadas da linha para que ela possa ser processada
        como se estivesse no primeiro octante, guardando as transformações
        realizadas para revertê-las posteriormente.
        """
        delta_x = self.x_final - self.x_inicial
        delta_y = self.y_final - self.y_inicial

        # Se a inclinação for maior que 1, troca os eixos x e y.
        if abs(delta_y) > abs(delta_x):
            self.x_inicial, self.y_inicial = self.y_inicial, self.x_inicial
            self.x_final, self.y_final = self.y_final, self.x_final
            self.troca_xy = True

        # Se a linha for desenhada da direita para a esquerda, inverte o eixo x.
        if self.x_inicial > self.x_final:
            self.x_inicial, self.x_final = -self.x_inicial, -self.x_final
            self.troca_x = True

        # Se a linha for desenhada de cima para baixo, inverte o eixo y.
        if self.y_inicial > self.y_final:
            self.y_inicial, self.y_final = -self.y_inicial, -self.y_final
            self.troca_y = True

    def aplicar_reflexao(self, pontos: list):
        """
        Aplica as reflexões inversas aos pontos calculados para retorná-los
        às suas posições originais no octante correto.

        Args:
            pontos (list): A lista de pontos [x, y] calculados no primeiro octante.
        """
        for ponto in pontos:
            if self.troca_y:
                ponto[1] = -ponto[1]
            if self.troca_x:
                ponto[0] = -ponto[0]
            if self.troca_xy:
                ponto[0], ponto[1] = ponto[1], ponto[0]