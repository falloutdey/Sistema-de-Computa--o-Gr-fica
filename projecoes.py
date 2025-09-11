# projecoes.py
import numpy as np
from bresenham import Bresenham
from polilinha import Polilinha

class Projetor3D:
    """
    Realiza projeções Ortogonal e Perspectiva de um sólido 3D e rasteriza o resultado.
    """
    def __init__(self, vertices_3d, arestas):
        # Armazena os vértices como um array NumPy para facilitar os cálculos
        self.vertices = np.array(vertices_3d, dtype=float)
        # Adiciona uma coluna de '1's para usar coordenadas homogêneas
        self.vertices_homogeneos = np.hstack([self.vertices, np.ones((self.vertices.shape[0], 1))])
        self.arestas = arestas
        self.saida = []

    def projetar_ortogonal(self):
        """
        Projeta os vértices 3D em um plano 2D (visão frontal), descartando o eixo Z.
        """
        # Matriz de projeção ortogonal frontal (plano XY)
        matriz_projecao = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 0], # Zera o eixo Z
            [0, 0, 0, 1]
        ])
        
        vertices_projetados = (matriz_projecao @ self.vertices_homogeneos.T).T
        # Retorna apenas as coordenadas X e Y
        return vertices_projetados[:, :2]

    def projetar_perspectiva(self, distancia_camera):
        """
        Projeta os vértices 3D em um plano 2D usando projeção perspectiva.
        """
        d = distancia_camera
        if d == 0: d = 1 # Evita divisão por zero

        # Matriz de projeção perspectiva
        matriz_projecao = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 1/d, 1]
        ])

        vertices_projetados = (matriz_projecao @ self.vertices_homogeneos.T).T
        
        # Normalização: divide X, Y e Z por W para obter as coordenadas 2D
        vertices_2d = []
        for v in vertices_projetados:
            w = v[3]
            if w != 0:
                # Multiplicamos por 'd' para escalar o resultado e torná-lo visível
                vertices_2d.append([d * v[0]/w, d * v[1]/w])
            else:
                vertices_2d.append([v[0], v[1]])
        
        return np.array(vertices_2d)

    def rasterizar_arestas(self, vertices_2d):
        """
        Usa o algoritmo de Bresenham para desenhar as arestas do sólido
        com base nos vértices 2D projetados.
        """
        pontos_rasterizados = []
        # Arredonda todos os vértices para coordenadas de pixel inteiras
        vertices_arredondados = np.round(vertices_2d).astype(int)

        for aresta in self.arestas:
            p1_idx, p2_idx = aresta
            p1 = vertices_arredondados[p1_idx]
            p2 = vertices_arredondados[p2_idx]
            
            linha = Bresenham(tuple(p1), tuple(p2))
            pontos_rasterizados.extend(linha.saida)
            
        self.saida = pontos_rasterizados