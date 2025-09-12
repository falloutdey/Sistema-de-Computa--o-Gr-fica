# Sistemas/projecoes.py
import numpy as np
import math
from Sistemas.bresenham import Bresenham

class Projetor3D:
    """
    Realiza projeções 3D (ortogonal, oblíqua e perspectiva) de um conjunto de 
    vértices e arestas, e depois rasteriza o resultado 2D.
    """
    def __init__(self, vertices_3d, arestas):
        """
        Inicializa o projetor com os dados do objeto 3D.

        Args:
            vertices_3d (list): Lista de listas ou tuplas, onde cada uma representa 
                                as coordenadas [x, y, z] de um vértice.
            arestas (list): Lista de listas ou tuplas, onde cada uma contém um par 
                            de índices indicando os vértices que formam uma aresta.
        """
        self.vertices = np.array(vertices_3d, dtype=float)
        # Adiciona uma coluna de '1's para usar coordenadas homogêneas,
        # facilitando as transformações matriciais.
        self.vertices_homogeneos = np.hstack([self.vertices, np.ones((self.vertices.shape[0], 1))])
        self.arestas = arestas
        self.saida = []

    def projetar_ortogonal(self):
        """ 
        Projeta os vértices 3D em um plano 2D (visão frontal),
        simplesmente descartando a coordenada Z.
        
        Returns:
            np.array: Um array com as coordenadas 2D [x, y] dos vértices projetados.
        """
        matriz_projecao = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 0],  # Zera o eixo Z
            [0, 0, 0, 1]
        ])
        vertices_projetados = (matriz_projecao @ self.vertices_homogeneos.T).T
        return vertices_projetados[:, :2]

    def projetar_cavalier(self, angulo=45):
        """ 
        Projeta usando a projeção oblíqua Cavalier, que mantém a profundidade 
        dos objetos sem distorção.

        Args:
            angulo (float): O ângulo da projeção.

        Returns:
            np.array: As coordenadas 2D [x, y] dos vértices projetados.
        """
        rad = math.radians(angulo)
        L = 1.0  # Fator de profundidade
        matriz_projecao = np.array([
            [1, 0, L * math.cos(rad), 0],
            [0, 1, L * math.sin(rad), 0],
            [0, 0, 0, 0],
            [0, 0, 0, 1]
        ])
        vertices_projetados = (matriz_projecao @ self.vertices_homogeneos.T).T
        return vertices_projetados[:, :2]

    def projetar_cabinet(self, angulo=45):
        """ 
        Projeta usando a projeção oblíqua Cabinet, que reduz a profundidade
        pela metade para uma aparência mais realista.

        Args:
            angulo (float): O ângulo da projeção.

        Returns:
            np.array: As coordenadas 2D [x, y] dos vértices projetados.
        """
        rad = math.radians(angulo)
        L = 0.5  # A profundidade é reduzida pela metade
        matriz_projecao = np.array([
            [1, 0, L * math.cos(rad), 0],
            [0, 1, L * math.sin(rad), 0],
            [0, 0, 0, 0],
            [0, 0, 0, 1]
        ])
        vertices_projetados = (matriz_projecao @ self.vertices_homogeneos.T).T
        return vertices_projetados[:, :2]

    def projetar_perspectiva(self, distancia_camera):
        """ 
        Projeta os vértices 3D em um plano 2D usando projeção perspectiva,
        o que cria a ilusão de profundidade.

        Args:
            distancia_camera (float): A distância do observador (câmera) ao plano de projeção.

        Returns:
            np.array: As coordenadas 2D [x, y] dos vértices projetados.
        """
        d = float(distancia_camera)
        if d == 0: d = 1.0

        vertices_2d = []
        for v in self.vertices:
            x, y, z = v[0], v[1], v[2]
            
            # O fator de perspectiva 'w' aumenta com a distância, fazendo objetos
            # mais distantes parecerem menores.
            w = 1 - (z / d)
            if w <= 0: 
                # Evita divisão por zero e pontos atrás do observador.
                vertices_2d.append([float('inf'), float('inf')])
                continue

            x_p = x / w
            y_p = y / w
            vertices_2d.append([x_p, y_p])
        
        return np.array(vertices_2d)

    def rasterizar_arestas(self, vertices_2d):
        """ 
        Usa o algoritmo de Bresenham para desenhar as arestas do sólido 
        conectando os vértices 2D projetados.
        
        Args:
            vertices_2d (np.array): O array de vértices 2D a serem conectados.
        """
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

                # Ignora arestas com coordenadas infinitas (pontos que estavam atrás da câmera).
                if np.isinf(p1).any() or np.isinf(p2).any():
                    continue
                
                linha = Bresenham(tuple(p1), tuple(p2))
                pontos_rasterizados.extend(linha.saida)
            
        self.saida = pontos_rasterizados