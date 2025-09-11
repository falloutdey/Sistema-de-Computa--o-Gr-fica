# polilinha.py
from bresenham import Bresenham

class Polilinha:
    """
    Cria uma lista de pixels que representam uma polilinha (uma série de
    linhas conectadas).
    """
    def __init__(self, pontos: list, fechar=False):
        self.saida = []
        
        pontos_a_desenhar = list(pontos)

        if fechar and len(pontos_a_desenhar) > 1:
            pontos_a_desenhar.append(pontos_a_desenhar[0])

        if len(pontos_a_desenhar) > 1:
            for i in range(len(pontos_a_desenhar) - 1):
                # Arredonda as coordenadas para inteiros antes de desenhar
                ponto_inicial = [round(pontos_a_desenhar[i][0]), round(pontos_a_desenhar[i][1])]
                ponto_final = [round(pontos_a_desenhar[i+1][0]), round(pontos_a_desenhar[i+1][1])]
                
                # Desenha o segmento apenas se os pontos forem diferentes após o arredondamento
                if ponto_inicial != ponto_final:
                    linha = Bresenham(ponto_inicial, ponto_final)
                    self.saida.extend(linha.saida)