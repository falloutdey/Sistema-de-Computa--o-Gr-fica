# Sistemas/varredura.py
from Sistemas.pontoCrítico import PontoCritico

class Varredura:
    """
    Implementa o algoritmo de preenchimento por Varredura (Scanline)
    usando uma Tabela de Arestas Ativas (AET) e uma Tabela de Arestas (ET).
    """
    def __init__(self, poligono):
        """
        Inicializa o algoritmo de preenchimento.

        Args:
            poligono (list): Uma lista de vértices (x, y) do polígono.
        """
        self.saida = []
        if len(poligono) < 3:
            return

        self.ymin, self.ymax = self._definir_limites_y(poligono)
        self.tabela_arestas = self._criar_tabela_arestas(poligono)
        self._preencher_poligono()

    def _definir_limites_y(self, poligono):
        """
        Encontra as coordenadas y mínima e máxima do polígono para determinar
        os limites da varredura.

        Args:
            poligono (list): A lista de vértices.

        Returns:
            tuple: (ymin, ymax)
        """
        ymin = min(p[1] for p in poligono)
        ymax = max(p[1] for p in poligono)
        return ymin, ymax

    def _criar_tabela_arestas(self, poligono):
        """
        Cria a Tabela de Arestas (Edge Table), que armazena as arestas do 
        polígono, indexadas pela sua coordenada y mínima.

        Args:
            poligono (list): A lista de vértices.

        Returns:
            dict: A Tabela de Arestas.
        """
        tabela = {}
        num_vertices = len(poligono)
        for i in range(num_vertices):
            p1 = poligono[i]
            p2 = poligono[(i + 1) % num_vertices]

            # Ignora arestas horizontais, pois elas não cruzam as linhas de varredura.
            if p1[1] == p2[1]:
                continue

            # Garante que p1 seja o vértice com menor y para padronizar.
            if p1[1] > p2[1]:
                p1, p2 = p2, p1
            
            ymin_aresta = p1[1]
            ymax_aresta = p2[1]
            x_inicial = float(p1[0])
            inv_slope = (p2[0] - p1[0]) / (p2[1] - p1[1]) if (p2[1] - p1[1]) != 0 else 0
            
            if ymin_aresta not in tabela:
                tabela[ymin_aresta] = []
            
            aresta = PontoCritico(ymax_aresta, x_inicial, inv_slope)
            tabela[ymin_aresta].append(aresta)
        
        return tabela

    def _preencher_poligono(self):
        """
        Executa o algoritmo de varredura principal.
        """
        arestas_ativas = []
        for y in range(self.ymin, self.ymax):
            # Adiciona novas arestas da Tabela de Arestas para a lista de Arestas Ativas (AET)
            # se a linha de varredura atual (y) atingir o y mínimo de uma aresta.
            if y in self.tabela_arestas:
                arestas_ativas.extend(self.tabela_arestas[y])

            # Remove arestas da AET se a linha de varredura ultrapassar o y máximo da aresta.
            arestas_ativas = [aresta for aresta in arestas_ativas if aresta.ymax > y]

            # Ordena a AET pela coordenada x da interseção.
            arestas_ativas.sort()

            # Preenche os pixels entre pares de interseções na linha de varredura atual.
            for i in range(0, len(arestas_ativas), 2):
                if i + 1 < len(arestas_ativas):
                    xmin = round(arestas_ativas[i].x_interseccao)
                    xmax = round(arestas_ativas[i+1].x_interseccao)
                    for x in range(xmin, xmax):
                        self.saida.append([x, y])

            # Atualiza a coordenada x de interseção para cada aresta na AET.
            for aresta in arestas_ativas:
                aresta.x_interseccao += aresta.inv_slope