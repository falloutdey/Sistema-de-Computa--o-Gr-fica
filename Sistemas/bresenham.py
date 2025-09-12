# bresenham.py
class Bresenham:
    def __init__(self, ponto1, ponto2):
        self.saida = []
        self.x_inicial, self.y_inicial = ponto1
        self.x_final, self.y_final = ponto2

        self.pontosFinais = []
        self.troca_x = self.troca_y = self.troca_xy = False

        if ponto1 == ponto2:
            self.saida = [ponto1]
            return

        self.calcular_octante()

        delta_x = self.x_final - self.x_inicial
        delta_y = self.y_final - self.y_inicial

        m = delta_y / delta_x if delta_x != 0 else float('inf')
        erro = m - 0.5

        aux_x, aux_y = self.x_inicial, self.y_inicial
        self.pontosFinais.append([aux_x, aux_y])

        while aux_x < self.x_final:
            if erro >= 0:
                aux_y += 1
                erro -= 1
            aux_x += 1
            erro += m
            self.pontosFinais.append([aux_x, aux_y])

        self.aplicar_reflexao(self.pontosFinais)
        self.saida = self.pontosFinais

    def calcular_octante(self):
        delta_x = self.x_final - self.x_inicial
        delta_y = self.y_final - self.y_inicial

        m = delta_y / delta_x if delta_x != 0 else 2

        if abs(m) > 1:
            self.x_inicial, self.y_inicial = self.y_inicial, self.x_inicial
            self.x_final, self.y_final = self.y_final, self.x_final
            self.troca_xy = True

        if self.x_inicial > self.x_final:
            self.x_inicial, self.x_final = -self.x_inicial, -self.x_final
            self.troca_x = True

        if self.y_inicial > self.y_final:
            self.y_inicial, self.y_final = -self.y_inicial, -self.y_final
            self.troca_y = True

    def aplicar_reflexao(self, pontos: list):
        for ponto in pontos:
            if self.troca_y:
                ponto[1] = -ponto[1]
            if self.troca_x:
                ponto[0] = -ponto[0]
            if self.troca_xy:
                ponto[0], ponto[1] = ponto[1], ponto[0]