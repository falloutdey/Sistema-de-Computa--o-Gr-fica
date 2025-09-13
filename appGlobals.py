# globals.py

"""
Este módulo centraliza as variáveis globais da aplicação para evitar o uso 
de 'global' em múltiplos arquivos e facilitar o gerenciamento de estado.
"""

def init():
    """
    Inicializa ou reinicializa todas as variáveis de estado globais da aplicação.
    
    Esta função é chamada no início do programa e sempre que a tela é limpa 
    para garantir que o estado da aplicação retorne ao seu ponto inicial, 
    evitando que dados de desenhos anteriores interfiram nos novos.
    """
    global pontos_selecionados, poligono_para_transformar, poligono_para_preencher, janela_de_recorte
    global vertices_3d_selecionados, arestas_3d_selecionadas, estado_projecao
    global estado_preenchimento, estado_recorte, estado_transformacao

    # --- Variáveis para desenho 2D ---
    pontos_selecionados = []  # Armazena os pontos clicados pelo usuário para formar um objeto.
    poligono_para_transformar = []  # Guarda os vértices do polígono que sofrerá transformações.
    poligono_para_preencher = []  # Armazena o polígono que será preenchido.
    janela_de_recorte = {}  # Dicionário com as coordenadas (xmin, ymin, xmax, ymax) da janela de recorte.

    # --- Variáveis para projeção 3D ---
    vertices_3d_selecionados = []  # Lista de vértices [x, y, z] do objeto 3D.
    arestas_3d_selecionadas = []  # Lista de arestas, representadas por pares de índices de vértices.
    estado_projecao = "definindo_vertices"  # Controla a fase da projeção ('definindo_vertices' ou 'definindo_arestas').

    # --- Variáveis de controle de estado para modos específicos ---
    estado_preenchimento = "desenhando_poligono"  # Controla a fase do preenchimento ('desenhando_poligono' ou 'escolhendo_semente').
    estado_recorte = "definindo_janela"  # Controla a fase do recorte ('definindo_janela' ou 'definindo_linha'/'definindo_poligono').
    estado_transformacao = "definindo_poligono"  # Controla a fase da transformação ('definindo_poligono' ou 'aplicando_transformacao').