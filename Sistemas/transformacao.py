# Sistemas/transformacao.py
import math
import numpy as np
from Sistemas.polilinha import Polilinha

class Transformacao:
    """
    Aplica transformações geométricas 2D (translação, escalonamento, rotação)
    a uma lista de pontos usando coordenadas homogêneas e matrizes de transformação.
    """
    def __init__(self, pontos: list):
        """
        Inicializa a classe de transformação com uma lista de pontos.

        Args:
            pontos (list): Uma lista de vértices [x, y] do objeto.
        """
        self.entrada = [list(p) for p in pontos]
        self.saida = [list(p) for p in pontos]

    def translacao(self, dx, dy):
        """
        Move o objeto somando dx e dy às suas coordenadas.

        Args:
            dx (int/float): O deslocamento no eixo x.
            dy (int/float): O deslocamento no eixo y.

        Returns:
            list: A nova lista de pontos transformados.
        """
        matriz_translacao = np.array([
            [1, 0, dx],
            [0, 1, dy],
            [0, 0, 1]
        ])
        # Converte os pontos para coordenadas homogêneas [x, y, 1].
        pontos_homogeneos = [np.array([p[0], p[1], 1]) for p in self.entrada]
        
        pontos_transformados = []
        for ponto in pontos_homogeneos:
            novo_ponto = matriz_translacao @ ponto
            pontos_transformados.append([novo_ponto[0], novo_ponto[1]])
        
        # Atualiza o estado interno do objeto.
        self.saida = pontos_transformados
        self.entrada = self.saida
        
        return self.saida

    def escalonamento(self, sx, sy, pivo=None):
        """
        Redimensiona o objeto em relação a um ponto pivô usando matrizes combinadas.

        Args:
            sx (float): O fator de escala no eixo x.
            sy (float): O fator de escala no eixo y.
            pivo (list, optional): O ponto [x, y] em torno do qual o escalonamento 
                                   ocorre. Se None, a origem (0,0) é usada.

        Returns:
            list: A lista de pixels rasterizados do polígono escalonado.
        """
        if pivo is None:
            pivo = [0, 0]
        
        # Matrizes de transformação:
        # 1. Transladar para a origem
        T_para_origem = np.array([[1, 0, -pivo[0]], [0, 1, -pivo[1]], [0, 0, 1]])
        # 2. Aplicar escalonamento
        S = np.array([[sx, 0, 0], [0, sy, 0], [0, 0, 1]])
        # 3. Transladar de volta para a posição original
        T_de_volta = np.array([[1, 0, pivo[0]], [0, 1, pivo[1]], [0, 0, 1]])
        
        matriz_combinada = T_de_volta @ S @ T_para_origem
        
        pontos_homogeneos = [np.array([p[0], p[1], 1]) for p in self.entrada]
        
        pontos_transformados = []
        for ponto in pontos_homogeneos:
            novo_ponto = matriz_combinada @ ponto
            pontos_transformados.append([round(novo_ponto[0]), round(novo_ponto[1])])
        
        self.entrada = pontos_transformados
        self.saida = pontos_transformados
        
        # Rasteriza o resultado para exibição.
        polilinha_resultante = Polilinha(self.saida, fechar=True)
        return polilinha_resultante.saida

    def rotacao(self, angulo, pivo=None):
        """
        Gira o objeto em torno de um ponto pivô.

        Args:
            angulo (float): O ângulo de rotação em graus.
            pivo (list, optional): O ponto [x, y] em torno do qual a rotação 
                                   ocorre. Se None, a origem (0,0) é usada.

        Returns:
            list: A lista de pixels rasterizados do polígono rotacionado.
        """
        if pivo is None:
            pivo = [0, 0]
        
        rad = math.radians(angulo)
        cos_theta = math.cos(rad)
        sin_theta = math.sin(rad)
        
        # Matrizes de transformação:
        # 1. Transladar para a origem
        T_para_origem = np.array([[1, 0, -pivo[0]], [0, 1, -pivo[1]], [0, 0, 1]])
        # 2. Aplicar rotação
        R = np.array([[cos_theta, -sin_theta, 0], [sin_theta,  cos_theta, 0], [0, 0, 1]])
        # 3. Transladar de volta
        T_de_volta = np.array([[1, 0, pivo[0]], [0, 1, pivo[1]], [0, 0, 1]])
        
        matriz_combinada = T_de_volta @ R @ T_para_origem
        
        pontos_homogeneos = [np.array([p[0], p[1], 1]) for p in self.entrada]
        
        pontos_rotacionados = []
        for ponto in pontos_homogeneos:
            novo_ponto = matriz_combinada @ ponto
            pontos_rotacionados.append([round(novo_ponto[0]), round(novo_ponto[1])])
            
        self.entrada = pontos_rotacionados
        self.saida = pontos_rotacionados
        
        polilinha_resultante = Polilinha(self.saida, fechar=True)
        return polilinha_resultante.saida