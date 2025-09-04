# varredura.py
from pontoCrítico import PontoCritico

class Varredura:
    """
    Implementa o algoritmo de preenchimento por Varredura (Scanline)
    usando uma Tabela de Arestas (Edge Table).
    """
    def __init__(self, poligono):
        self.saida = []
        if len(poligono) < 3:
            return

        self.ymin, self.ymax = self._definir_limites_y(poligono)
        self.tabela_arestas = self._criar_tabela_arestas(poligono)
        self._preencher_poligono()

    def _definir_limites_y(self, poligono):
        ymin = min(p[1] for p in poligono)
        ymax = max(p[1] for p in poligono)
        return ymin, ymax

    def _criar_tabela_arestas(self, poligono):
        tabela = {}
        num_vertices = len(poligono)
        for i in range(num_vertices):
            p1 = poligono[i]
            p2 = poligono[(i + 1) % num_vertices]

            # Ignora arestas horizontais
            if p1[1] == p2[1]:
                continue

            # Garante que p1 é o ponto com menor y
            if p1[1] > p2[1]:
                p1, p2 = p2, p1
            
            ymin_aresta = p1[1]
            ymax_aresta = p2[1]
            x_inicial = p1[0]
            inv_slope = (p2[0] - p1[0]) / (p2[1] - p1[1])
            
            if ymin_aresta not in tabela:
                tabela[ymin_aresta] = []
            
            aresta = PontoCritico(ymax_aresta, x_inicial, inv_slope)
            tabela[ymin_aresta].append(aresta)
        
        return tabela

    def _preencher_poligono(self):
        arestas_ativas = []
        for y in range(self.ymin, self.ymax):
            # Adiciona novas arestas que começam na linha de varredura atual
            if y in self.tabela_arestas:
                arestas_ativas.extend(self.tabela_arestas[y])

            # Remove arestas que terminam nesta linha de varredura
            arestas_ativas = [aresta for aresta in arestas_ativas if aresta.ymax > y]

            # Ordena as arestas ativas pela coordenada x
            arestas_ativas.sort()

            # Preenche os pixels entre pares de interseções
            for i in range(0, len(arestas_ativas), 2):
                if i + 1 < len(arestas_ativas):
                    xmin = round(arestas_ativas[i].x_interseccao)
                    xmax = round(arestas_ativas[i+1].x_interseccao)
                    for x in range(xmin, xmax):
                        self.saida.append([x, y])

            # Atualiza a intersecção x para a próxima linha de varredura
            for aresta in arestas_ativas:
                aresta.x_interseccao += aresta.inv_slope