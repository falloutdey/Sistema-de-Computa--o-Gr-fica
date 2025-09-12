# Sistemas/polilinha.py
from Sistemas.bresenham import Bresenham

class Polilinha:
    """
    Cria uma lista de pixels que representam uma polilinha (uma série de
    segmentos de linha conectados).
    """
    def __init__(self, pontos: list, fechar=False):
        """
        Inicializa a criação da polilinha.

        Args:
            pontos (list): Uma lista de tuplas (x, y) representando os vértices.
            fechar (bool): Se True, um segmento de linha adicional será desenhado
                           do último ao primeiro ponto para fechar a forma.
        """
        self.saida = []
        
        pontos_a_desenhar = list(pontos)

        # Se a opção 'fechar' for True, adiciona o primeiro ponto ao final da lista
        # para criar o segmento de fechamento.
        if fechar and len(pontos_a_desenhar) > 1:
            pontos_a_desenhar.append(pontos_a_desenhar[0])

        # Desenha um segmento de linha entre cada par de pontos consecutivos.
        if len(pontos_a_desenhar) > 1:
            for i in range(len(pontos_a_desenhar) - 1):
                # Arredonda as coordenadas para inteiros antes de desenhar.
                ponto_inicial = [round(pontos_a_desenhar[i][0]), round(pontos_a_desenhar[i][1])]
                ponto_final = [round(pontos_a_desenhar[i+1][0]), round(pontos_a_desenhar[i+1][1])]
                
                # Desenha o segmento apenas se os pontos forem diferentes após o arredondamento.
                if ponto_inicial != ponto_final:
                    linha = Bresenham(ponto_inicial, ponto_final)
                    self.saida.extend(linha.saida)