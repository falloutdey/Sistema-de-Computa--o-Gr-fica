# projecoes.py
import numpy as np
import math
from Sistemas.bresenham import Bresenham

class Projetor3D:
    """
    Realiza projeções 3D e rasteriza o resultado.
    """
    def __init__(self, vertices_3d, arestas):
        self.vertices = np.array(vertices_3d, dtype=float)
        # Adiciona uma coluna de '1's para usar coordenadas homogêneas
        self.vertices_homogeneos = np.hstack([self.vertices, np.ones((self.vertices.shape[0], 1))])
        self.arestas = arestas
        self.saida = []

    def projetar_ortogonal(self):
        """ Projeta os vértices 3D em um plano 2D (visão frontal). """
        matriz_projecao = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 0], # Zera o eixo Z
            [0, 0, 0, 1]
        ])
        vertices_projetados = (matriz_projecao @ self.vertices_homogeneos.T).T
        return vertices_projetados[:, :2]

    def projetar_cavalier(self, angulo=45):
        """ Projeta usando a projeção oblíqua Cavalier. """
        rad = math.radians(angulo)
        L = 1.0
        matriz_projecao = np.array([
            [1, 0, L * math.cos(rad), 0],
            [0, 1, L * math.sin(rad), 0],
            [0, 0, 0, 0],
            [0, 0, 0, 1]
        ])
        vertices_projetados = (matriz_projecao @ self.vertices_homogeneos.T).T
        return vertices_projetados[:, :2]

    def projetar_cabinet(self, angulo=45):
        """ Projeta usando a projeção oblíqua Cabinet. """
        rad = math.radians(angulo)
        L = 0.5 # A profundidade é reduzida pela metade
        matriz_projecao = np.array([
            [1, 0, L * math.cos(rad), 0],
            [0, 1, L * math.sin(rad), 0],
            [0, 0, 0, 0],
            [0, 0, 0, 1]
        ])
        vertices_projetados = (matriz_projecao @ self.vertices_homogeneos.T).T
        return vertices_projetados[:, :2]

    def projetar_perspectiva(self, distancia_camera):
        """ Projeta os vértices 3D em um plano 2D usando projeção perspectiva. """
        d = float(distancia_camera)
        if d == 0: d = 1.0

        vertices_2d = []
        for v in self.vertices:
            x, y, z = v[0], v[1], v[2]
            
            # Fator de perspectiva (evita divisão por zero)
            w = 1 - (z / d)
            if w <= 0: 
                vertices_2d.append([float('inf'), float('inf')])
                continue

            x_p = x / w
            y_p = y / w
            vertices_2d.append([x_p, y_p])
        
        return np.array(vertices_2d)

    def rasterizar_arestas(self, vertices_2d):
        """ Usa o algoritmo de Bresenham para desenhar as arestas do sólido. """
        if len(vertices_2d) == 0:
            self.saida = []
            return

        pontos_rasterizados = []
        vertices_arredondados = np.round(vertices_2d).astype(int)

        for aresta in self.arestas:
            p1_idx, p2_idx = aresta
            if p1_idx < len(vertices_arredondados) and p2_idx < len(vertices_arredondados):
                p1 = vertices_arredondados[p1_idx]
                p2 = vertices_arredondados[p2_idx]

                if np.isinf(p1).any() or np.isinf(p2).any():
                    continue
                
                linha = Bresenham(tuple(p1), tuple(p2))
                pontos_rasterizados.extend(linha.saida)
            
        self.saida = pontos_rasterizados