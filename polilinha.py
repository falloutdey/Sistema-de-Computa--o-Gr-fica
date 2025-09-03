# polilinha.py
from bresenham import Bresenham

class Polilinha:
    """
    Cria uma lista de pixels que representam uma polilinha (uma série de
    linhas conectadas).
    """
    def __init__(self, pontos: list, fechar=False):
        self.saida = []
        
        # Cria uma cópia da lista de pontos para não modificar a original
        pontos_a_desenhar = list(pontos)

        # Se a opção 'fechar' for verdadeira, adiciona o primeiro ponto ao final
        # da lista para criar a linha de fechamento.
        if fechar and len(pontos_a_desenhar) > 1:
            pontos_a_desenhar.append(pontos_a_desenhar[0])

        # Se houver pelo menos dois pontos, desenha as linhas
        if len(pontos_a_desenhar) > 1:
            for i in range(len(pontos_a_desenhar) - 1):
                ponto_inicial = pontos_a_desenhar[i]
                ponto_final = pontos_a_desenhar[i+1]
                
                # Usa o algoritmo de Bresenham para cada segmento
                linha = Bresenham(ponto_inicial, ponto_final)
                self.saida.extend(linha.saida)