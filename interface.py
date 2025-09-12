# interface.py
import tkinter as tk
from tkinter import ttk

def create_linha_frame(parent, app_callbacks):
    """
    Cria e retorna o frame de controles para o desenho de linhas.

    Args:
        parent (tk.Widget): O widget pai onde o frame será inserido.
        app_callbacks (App): A instância da classe principal da aplicação, 
                             usada para conectar os callbacks dos botões.

    Returns:
        tuple: Uma tupla contendo o frame criado e um dicionário com os widgets 
               de entrada (Entries) para acesso posterior.
    """
    frame = ttk.LabelFrame(parent, text="Controles da Linha")
    tk.Label(frame, text="P1 (x0, y0)").pack()
    entry_x0 = tk.Entry(frame, width=10)
    entry_x0.pack()
    entry_y0 = tk.Entry(frame, width=10)
    entry_y0.pack()
    tk.Label(frame, text="P2 (x1, y1)").pack(pady=(10, 0))
    entry_x1 = tk.Entry(frame, width=10)
    entry_x1.pack()
    entry_y1 = tk.Entry(frame, width=10)
    entry_y1.pack()
    ttk.Button(frame, text="Desenhar Linha", command=app_callbacks.desenhar_linha).pack(pady=10, fill="x")
    return frame, {'entry_x0': entry_x0, 'entry_y0': entry_y0, 'entry_x1': entry_x1, 'entry_y1': entry_y1}


def create_polilinha_frame(parent, app_callbacks):
    """
    Cria e retorna o frame de controles para o desenho de polilinhas.

    Args:
        parent (tk.Widget): O widget pai.
        app_callbacks (App): A instância da classe principal para os callbacks.

    Returns:
        tuple: O frame criado e um dicionário de widgets.
    """
    frame = ttk.LabelFrame(parent, text="Controles da Polilinha")
    tk.Label(frame, text="Adicionar Ponto (x, y)").pack()
    entry_p_x_pv = tk.Entry(frame, width=10)
    entry_p_x_pv.pack()
    entry_p_y_pv = tk.Entry(frame, width=10)
    entry_p_y_pv.pack()
    ttk.Button(frame, text="Adicionar Ponto", command=app_callbacks.add_point_from_entry).pack(pady=5, fill="x")
    tk.Label(frame, text="Pontos:").pack(pady=(10, 0))
    texto_pontos_polilinha = tk.Text(frame, height=5, width=20)
    texto_pontos_polilinha.pack(pady=5)
    texto_pontos_polilinha.config(state=tk.DISABLED)
    ttk.Button(frame, text="Desenhar Polilinha", command=app_callbacks.desenhar_polilinha).pack(pady=5, fill="x")
    return frame, {'entry_p_x_pv': entry_p_x_pv, 'entry_p_y_pv': entry_p_y_pv, 'texto_pontos_polilinha': texto_pontos_polilinha}


def create_circulo_frame(parent, app_callbacks):
    """
    Cria e retorna o frame de controles para o desenho de círculos.

    Args:
        parent (tk.Widget): O widget pai.
        app_callbacks (App): A instância da classe principal para os callbacks.

    Returns:
        tuple: O frame criado e um dicionário de widgets.
    """
    frame = ttk.LabelFrame(parent, text="Controles do Círculo")
    tk.Label(frame, text="Centro (cx, cy)").pack()
    entry_cx = tk.Entry(frame, width=10)
    entry_cx.pack()
    entry_cy = tk.Entry(frame, width=10)
    entry_cy.pack()
    tk.Label(frame, text="Raio").pack(pady=(10, 0))
    entry_raio = tk.Entry(frame, width=10)
    entry_raio.pack()
    ttk.Button(frame, text="Desenhar Círculo", command=app_callbacks.desenhar_circulo).pack(pady=10, fill="x")
    return frame, {'entry_cx': entry_cx, 'entry_cy': entry_cy, 'entry_raio': entry_raio}


def create_elipse_frame(parent, app_callbacks):
    """
    Cria e retorna o frame de controles para o desenho de elipses.

    Args:
        parent (tk.Widget): O widget pai.
        app_callbacks (App): A instância da classe principal para os callbacks.

    Returns:
        tuple: O frame criado e um dicionário de widgets.
    """
    frame = ttk.LabelFrame(parent, text="Controles da Elipse")
    tk.Label(frame, text="Centro (cx, cy)").pack()
    entry_ex = tk.Entry(frame, width=10)
    entry_ex.pack()
    entry_ey = tk.Entry(frame, width=10)
    entry_ey.pack()
    tk.Label(frame, text="Raio X (rx)").pack(pady=(10, 0))
    entry_rx = tk.Entry(frame, width=10)
    entry_rx.pack()
    tk.Label(frame, text="Raio Y (ry)").pack(pady=(10, 0))
    entry_ry = tk.Entry(frame, width=10)
    entry_ry.pack()
    ttk.Button(frame, text="Desenhar Elipse", command=app_callbacks.desenhar_elipse).pack(pady=10, fill="x")
    return frame, {'entry_ex': entry_ex, 'entry_ey': entry_ey, 'entry_rx': entry_rx, 'entry_ry': entry_ry}


def create_curva_frame(parent, app_callbacks):
    """
    Cria e retorna o frame de controles para o desenho de curvas de Bézier.

    Args:
        parent (tk.Widget): O widget pai.
        app_callbacks (App): A instância da classe principal para os callbacks.

    Returns:
        tuple: O frame criado e um dicionário de widgets.
    """
    frame = ttk.LabelFrame(parent, text="Controles da Curva")
    tk.Label(frame, text="Adicionar Ponto (x, y)").pack()
    entry_p_x_curva = tk.Entry(frame, width=10)
    entry_p_x_curva.pack()
    entry_p_y_curva = tk.Entry(frame, width=10)
    entry_p_y_curva.pack()
    ttk.Button(frame, text="Adicionar Ponto", command=app_callbacks.add_point_from_entry).pack(pady=5, fill="x")
    tk.Label(frame, text="Pontos de Controle:").pack(pady=5)
    texto_pontos_curva = tk.Text(frame, height=8, width=20)
    texto_pontos_curva.pack(pady=5)
    texto_pontos_curva.config(state=tk.DISABLED)
    ttk.Button(frame, text="Desenhar Curva", command=app_callbacks.desenhar_curva).pack(pady=10, fill="x")
    return frame, {'entry_p_x_curva': entry_p_x_curva, 'entry_p_y_curva': entry_p_y_curva, 'texto_pontos_curva': texto_pontos_curva}


def create_preenchimento_frame(parent, app_callbacks):
    """
    Cria e retorna o frame de controles para o preenchimento de polígonos.
    Este frame contém dois sub-frames para as diferentes etapas do processo.

    Args:
        parent (tk.Widget): O widget pai.
        app_callbacks (App): A instância da classe principal para os callbacks.

    Returns:
        tuple: O frame principal e um dicionário com todos os seus widgets internos.
    """
    frame = ttk.LabelFrame(parent, text="Controles de Preenchimento")

    # Sub-frame para adicionar vértices do polígono
    frame_desenho_poligono = tk.Frame(frame)
    tk.Label(frame_desenho_poligono, text="1. Adicionar Vértice (x, y)").pack()
    entry_p_x_preenchimento = tk.Entry(frame_desenho_poligono, width=10)
    entry_p_x_preenchimento.pack()
    entry_p_y_preenchimento = tk.Entry(frame_desenho_poligono, width=10)
    entry_p_y_preenchimento.pack()
    ttk.Button(frame_desenho_poligono, text="Adicionar Vértice", command=app_callbacks.add_point_from_entry).pack(pady=5)
    tk.Label(frame_desenho_poligono, text="Vértices:").pack()
    texto_pontos_preenchimento = tk.Text(frame_desenho_poligono, height=5, width=20)
    texto_pontos_preenchimento.pack(pady=5)
    texto_pontos_preenchimento.config(state=tk.DISABLED)
    ttk.Button(frame_desenho_poligono, text="Finalizar Polígono", command=app_callbacks.finalizar_poligono_para_preenchimento).pack(pady=5, fill="x")

    # Sub-frame para escolher o ponto de semente e a cor
    frame_escolha_semente = tk.Frame(frame)
    tk.Label(frame_escolha_semente, text="2. Ponto de Semente (x, y)").pack()
    entry_p_x_fill = tk.Entry(frame_escolha_semente, width=10)
    entry_p_x_fill.pack()
    entry_p_y_fill = tk.Entry(frame_escolha_semente, width=10)
    entry_p_y_fill.pack()
    tk.Label(frame_escolha_semente, text="Cor:").pack(pady=(10, 0))
    entry_cor_preenchimento = tk.Entry(frame_escolha_semente, width=10)
    entry_cor_preenchimento.pack()
    entry_cor_preenchimento.insert(0, "#FF0000")
    ttk.Button(frame_escolha_semente, text="Preencher", command=app_callbacks.executar_preenchimento).pack(pady=10, fill="x")

    return frame, {
        'frame_desenho_poligono': frame_desenho_poligono,
        'entry_p_x_preenchimento': entry_p_x_preenchimento,
        'entry_p_y_preenchimento': entry_p_y_preenchimento,
        'texto_pontos_preenchimento': texto_pontos_preenchimento,
        'frame_escolha_semente': frame_escolha_semente,
        'entry_p_x_fill': entry_p_x_fill,
        'entry_p_y_fill': entry_p_y_fill,
        'entry_cor_preenchimento': entry_cor_preenchimento
    }


def create_varredura_frame(parent, app_callbacks):
    """
    Cria e retorna o frame para o preenchimento por varredura (Scanline).

    Args:
        parent (tk.Widget): O widget pai.
        app_callbacks (App): A instância da classe principal para os callbacks.

    Returns:
        tuple: O frame criado e um dicionário de widgets.
    """
    frame = ttk.LabelFrame(parent, text="Controles de Varredura")
    tk.Label(frame, text="Adicionar Vértice (x, y)").pack()
    entry_p_x_varredura = tk.Entry(frame, width=10)
    entry_p_x_varredura.pack()
    entry_p_y_varredura = tk.Entry(frame, width=10)
    entry_p_y_varredura.pack()
    ttk.Button(frame, text="Adicionar Vértice", command=app_callbacks.add_point_from_entry).pack(pady=5, fill="x")
    tk.Label(frame, text="Vértices do Polígono:").pack(pady=5)
    texto_pontos_varredura = tk.Text(frame, height=8, width=20)
    texto_pontos_varredura.pack(pady=5)
    texto_pontos_varredura.config(state=tk.DISABLED)
    ttk.Button(frame, text="Preencher com Varredura", command=app_callbacks.executar_varredura).pack(pady=10, fill="x")
    return frame, {'entry_p_x_varredura': entry_p_x_varredura, 'entry_p_y_varredura': entry_p_y_varredura, 'texto_pontos_varredura': texto_pontos_varredura}


def create_recorte_linha_frame(parent, app_callbacks):
    """
    Cria e retorna o frame de controles para o recorte de linha.

    Args:
        parent (tk.Widget): O widget pai.
        app_callbacks (App): A instância da classe principal para os callbacks.

    Returns:
        tuple: O frame principal e um dicionário com todos os seus widgets internos.
    """
    frame = ttk.LabelFrame(parent, text="Controles de Recorte de Linha")

    # Sub-frame para definir a janela de recorte
    frame_definir_janela = tk.Frame(frame)
    tk.Label(frame_definir_janela, text="1. Defina a Janela de Recorte:").pack()
    tk.Label(frame_definir_janela, text="Ponto 1 (xmin, ymin)").pack()
    entry_xmin = tk.Entry(frame_definir_janela, width=10)
    entry_xmin.pack()
    entry_ymin = tk.Entry(frame_definir_janela, width=10)
    entry_ymin.pack()
    tk.Label(frame_definir_janela, text="Ponto 2 (xmax, ymax)").pack(pady=(5, 0))
    entry_xmax = tk.Entry(frame_definir_janela, width=10)
    entry_xmax.pack()
    entry_ymax = tk.Entry(frame_definir_janela, width=10)
    entry_ymax.pack()
    ttk.Button(frame_definir_janela, text="Finalizar Janela", command=app_callbacks.finalizar_janela_de_recorte).pack(pady=10, fill="x")

    # Sub-frame para definir a linha a ser recortada
    frame_definir_linha = tk.Frame(frame)
    tk.Label(frame_definir_linha, text="2. Defina a Linha a ser Recortada:").pack()
    tk.Label(frame_definir_linha, text="Ponto 1 (x0, y0)").pack()
    entry_x0_recorte = tk.Entry(frame_definir_linha, width=10)
    entry_x0_recorte.pack()
    entry_y0_recorte = tk.Entry(frame_definir_linha, width=10)
    entry_y0_recorte.pack()
    tk.Label(frame_definir_linha, text="Ponto 2 (x1, y1)").pack(pady=(5, 0))
    entry_x1_recorte = tk.Entry(frame_definir_linha, width=10)
    entry_x1_recorte.pack()
    entry_y1_recorte = tk.Entry(frame_definir_linha, width=10)
    entry_y1_recorte.pack()
    ttk.Button(frame_definir_linha, text="Recortar Linha", command=app_callbacks.executar_recorte_linha).pack(pady=10, fill="x")

    return frame, {
        'frame_definir_janela': frame_definir_janela,
        'entry_xmin': entry_xmin,
        'entry_ymin': entry_ymin,
        'entry_xmax': entry_xmax,
        'entry_ymax': entry_ymax,
        'frame_definir_linha': frame_definir_linha,
        'entry_x0_recorte': entry_x0_recorte,
        'entry_y0_recorte': entry_y0_recorte,
        'entry_x1_recorte': entry_x1_recorte,
        'entry_y1_recorte': entry_y1_recorte
    }


def create_recorte_poligono_frame(parent, app_callbacks):
    """
    Cria e retorna o frame de controles para o recorte de polígono.

    Args:
        parent (tk.Widget): O widget pai.
        app_callbacks (App): A instância da classe principal para os callbacks.

    Returns:
        tuple: O frame principal e um dicionário com todos os seus widgets internos.
    """
    frame = ttk.LabelFrame(parent, text="Controles de Recorte de Polígono")

    # Sub-frame para definir a janela de recorte
    frame_definir_janela_p = tk.Frame(frame)
    tk.Label(frame_definir_janela_p, text="1. Defina a Janela de Recorte:").pack()
    tk.Label(frame_definir_janela_p, text="Ponto 1 (xmin, ymin)").pack()
    entry_xmin_p = tk.Entry(frame_definir_janela_p, width=10)
    entry_xmin_p.pack()
    entry_ymin_p = tk.Entry(frame_definir_janela_p, width=10)
    entry_ymin_p.pack()
    tk.Label(frame_definir_janela_p, text="Ponto 2 (xmax, ymax)").pack(pady=(5, 0))
    entry_xmax_p = tk.Entry(frame_definir_janela_p, width=10)
    entry_xmax_p.pack()
    entry_ymax_p = tk.Entry(frame_definir_janela_p, width=10)
    entry_ymax_p.pack()
    ttk.Button(frame_definir_janela_p, text="Finalizar Janela", command=app_callbacks.finalizar_janela_para_recorte_poligono).pack(pady=10, fill="x")

    # Sub-frame para definir o polígono a ser recortado
    frame_definir_poligono = tk.Frame(frame)
    tk.Label(frame_definir_poligono, text="2. Defina os Vértices do Polígono:").pack()
    tk.Label(frame_definir_poligono, text="Adicionar Ponto (x, y)").pack()
    entry_p_x_recorte_p = tk.Entry(frame_definir_poligono, width=10)
    entry_p_x_recorte_p.pack()
    entry_p_y_recorte_p = tk.Entry(frame_definir_poligono, width=10)
    entry_p_y_recorte_p.pack()
    ttk.Button(frame_definir_poligono, text="Adicionar Vértice", command=app_callbacks.add_point_from_entry).pack(pady=5)
    tk.Label(frame_definir_poligono, text="Vértices:").pack()
    texto_pontos_recorte_p = tk.Text(frame_definir_poligono, height=5, width=20)
    texto_pontos_recorte_p.pack(pady=5)
    texto_pontos_recorte_p.config(state=tk.DISABLED)
    ttk.Button(frame_definir_poligono, text="Recortar Polígono", command=app_callbacks.executar_recorte_poligono).pack(pady=10, fill="x")

    return frame, {
        'frame_definir_janela_p': frame_definir_janela_p,
        'entry_xmin_p': entry_xmin_p,
        'entry_ymin_p': entry_ymin_p,
        'entry_xmax_p': entry_xmax_p,
        'entry_ymax_p': entry_ymax_p,
        'frame_definir_poligono': frame_definir_poligono,
        'entry_p_x_recorte_p': entry_p_x_recorte_p,
        'entry_p_y_recorte_p': entry_p_y_recorte_p,
        'texto_pontos_recorte_p': texto_pontos_recorte_p
    }


def create_transformacao_frame(parent, app_callbacks):
    """
    Cria e retorna o frame de controles para transformações geométricas 2D.

    Args:
        parent (tk.Widget): O widget pai.
        app_callbacks (App): A instância da classe principal para os callbacks.

    Returns:
        tuple: O frame principal e um dicionário com todos os seus widgets internos.
    """
    frame = ttk.LabelFrame(parent, text="Controles de Transformação")

    # Sub-frame para adicionar vértices do polígono
    frame_add_ponto_transf = tk.Frame(frame)
    tk.Label(frame_add_ponto_transf, text="1. Adicionar Vértice (x, y)").pack()
    entry_p_x_transf = tk.Entry(frame_add_ponto_transf, width=10)
    entry_p_x_transf.pack()
    entry_p_y_transf = tk.Entry(frame_add_ponto_transf, width=10)
    entry_p_y_transf.pack()
    ttk.Button(frame_add_ponto_transf, text="Adicionar Vértice", command=app_callbacks.add_point_from_entry).pack(pady=5)
    tk.Label(frame_add_ponto_transf, text="Vértices:").pack()
    texto_pontos_transformacao = tk.Text(frame_add_ponto_transf, height=5, width=20)
    texto_pontos_transformacao.pack(pady=5)
    texto_pontos_transformacao.config(state=tk.DISABLED)
    ttk.Button(frame_add_ponto_transf, text="Finalizar Polígono", command=app_callbacks.finalizar_poligono_para_transformacao).pack(pady=5)

    # Sub-frame para as opções de transformação
    frame_opcoes_transf = tk.Frame(frame)
    tk.Label(frame_opcoes_transf, text="2. Aplicar Transformações").pack()
    frame_translacao = ttk.LabelFrame(frame_opcoes_transf, text="Translação")
    tk.Label(frame_translacao, text="dx:").pack(side="left")
    entry_dx_transf = tk.Entry(frame_translacao, width=5)
    entry_dx_transf.pack(side="left", padx=5)
    entry_dx_transf.insert(0, "5")
    tk.Label(frame_translacao, text="dy:").pack(side="left")
    entry_dy_transf = tk.Entry(frame_translacao, width=5)
    entry_dy_transf.pack(side="left", padx=5)
    entry_dy_transf.insert(0, "5")
    ttk.Button(frame_translacao, text="Aplicar", command=app_callbacks.aplicar_translacao).pack(side="right", padx=5)
    frame_translacao.pack(fill="x", pady=5)
    frame_escalonamento = ttk.LabelFrame(frame_opcoes_transf, text="Escalonamento")
    tk.Label(frame_escalonamento, text="sx:").pack()
    entry_sx_transf = tk.Entry(frame_escalonamento, width=10)
    entry_sx_transf.pack()
    entry_sx_transf.insert(0, "1.5")
    tk.Label(frame_escalonamento, text="sy:").pack()
    entry_sy_transf = tk.Entry(frame_escalonamento, width=10)
    entry_sy_transf.pack()
    entry_sy_transf.insert(0, "1.5")
    tk.Label(frame_escalonamento, text="Pivô:").pack()
    combo_pivo_escalonamento = ttk.Combobox(frame_escalonamento, width=15, state="readonly")
    combo_pivo_escalonamento.pack()
    ttk.Button(frame_escalonamento, text="Aplicar", command=app_callbacks.aplicar_escalonamento).pack(pady=5)
    frame_escalonamento.pack(fill="x", pady=5)
    frame_rotacao = ttk.LabelFrame(frame_opcoes_transf, text="Rotação")
    tk.Label(frame_rotacao, text="Ângulo (graus):").pack()
    entry_angulo_transf = tk.Entry(frame_rotacao, width=10)
    entry_angulo_transf.pack()
    entry_angulo_transf.insert(0, "45")
    tk.Label(frame_rotacao, text="Pivô:").pack()
    combo_pivo_rotacao = ttk.Combobox(frame_rotacao, width=15, state="readonly")
    combo_pivo_rotacao.pack()
    ttk.Button(frame_rotacao, text="Aplicar", command=app_callbacks.aplicar_rotacao).pack(pady=5)
    frame_rotacao.pack(fill="x", pady=5)
    return frame, {
        'frame_add_ponto_transf': frame_add_ponto_transf,
        'entry_p_x_transf': entry_p_x_transf,
        'entry_p_y_transf': entry_p_y_transf,
        'texto_pontos_transformacao': texto_pontos_transformacao,
        'frame_opcoes_transf': frame_opcoes_transf,
        'entry_dx_transf': entry_dx_transf,
        'entry_dy_transf': entry_dy_transf,
        'entry_sx_transf': entry_sx_transf,
        'entry_sy_transf': entry_sy_transf,
        'combo_pivo_escalonamento': combo_pivo_escalonamento,
        'entry_angulo_transf': entry_angulo_transf,
        'combo_pivo_rotacao': combo_pivo_rotacao
    }


def create_projecao_frame(parent, app_callbacks):
    """
    Cria e retorna o frame de controles para projeções 3D.

    Args:
        parent (tk.Widget): O widget pai.
        app_callbacks (App): A instância da classe principal para os callbacks.

    Returns:
        tuple: O frame principal e um dicionário com todos os seus widgets internos.
    """
    frame = ttk.LabelFrame(parent, text="Controles de Projeção 3D")

    # Sub-frame para definir os vértices 3D
    frame_definir_vertices_3d = tk.Frame(frame)
    tk.Label(frame_definir_vertices_3d, text="1. Adicionar Vértices 3D").pack()
    frame_coords = tk.Frame(frame_definir_vertices_3d)
    tk.Label(frame_coords, text="X:").pack(side='left')
    entry_vertice_x = tk.Entry(frame_coords, width=4)
    entry_vertice_x.pack(side='left')
    tk.Label(frame_coords, text="Y:").pack(side='left')
    entry_vertice_y = tk.Entry(frame_coords, width=4)
    entry_vertice_y.pack(side='left')
    tk.Label(frame_coords, text="Z:").pack(side='left')
    entry_vertice_z = tk.Entry(frame_coords, width=4)
    entry_vertice_z.pack(side='left')
    frame_coords.pack(pady=5)
    ttk.Button(frame_definir_vertices_3d, text="Adicionar Vértice", command=app_callbacks.add_vertice_3d).pack()
    tk.Label(frame_definir_vertices_3d, text="Vértices:").pack()
    texto_vertices_3d = tk.Text(frame_definir_vertices_3d, height=5, width=25)
    texto_vertices_3d.pack(pady=5)
    texto_vertices_3d.config(state=tk.DISABLED)
    ttk.Button(frame_definir_vertices_3d, text="Finalizar Vértices", command=app_callbacks.finalizar_vertices_3d).pack(pady=5, fill='x')

    # Sub-frame para definir as arestas do objeto 3D
    frame_definir_arestas_3d = tk.Frame(frame)
    tk.Label(frame_definir_arestas_3d, text="2. Adicionar Arestas").pack()
    frame_arestas = tk.Frame(frame_definir_arestas_3d)
    tk.Label(frame_arestas, text="De:").pack()
    combo_aresta_de = ttk.Combobox(frame_arestas, width=22, state="readonly")
    combo_aresta_de.pack()
    tk.Label(frame_arestas, text="Para:").pack()
    combo_aresta_para = ttk.Combobox(frame_arestas, width=22, state="readonly")
    combo_aresta_para.pack()
    frame_arestas.pack(pady=5)
    ttk.Button(frame_definir_arestas_3d, text="Adicionar Aresta", command=app_callbacks.add_aresta_3d).pack()
    tk.Label(frame_definir_arestas_3d, text="Arestas:").pack()
    texto_arestas_3d = tk.Text(frame_definir_arestas_3d, height=4, width=25)
    texto_arestas_3d.pack(pady=5)
    texto_arestas_3d.config(state=tk.DISABLED)

    # Controles para projeção
    ttk.Separator(frame_definir_arestas_3d, orient='horizontal').pack(fill='x', pady=10)
    tk.Label(frame_definir_arestas_3d, text="3. Escolher Projeção").pack()
    tk.Label(frame_definir_arestas_3d, text="Tipo de Projeção:").pack()
    combo_tipo_projecao = ttk.Combobox(frame_definir_arestas_3d, values=["Ortogonal", "Cavalier", "Cabinet", "Perspectiva"], state="readonly", width=25)
    combo_tipo_projecao.pack(pady=5)
    combo_tipo_projecao.current(0)
    combo_tipo_projecao.bind("<<ComboboxSelected>>", app_callbacks.toggle_distancia_camera)

    label_distancia_proj = tk.Label(frame_definir_arestas_3d, text="Distância Câmera (Perspectiva):")
    entry_distancia_proj = tk.Entry(frame_definir_arestas_3d, width=27)
    entry_distancia_proj.insert(0, "20")
    btn_projetar_objeto = ttk.Button(frame_definir_arestas_3d, text="Projetar Objeto", command=app_callbacks.executar_projecao)

    return frame, {
        'frame_definir_vertices_3d': frame_definir_vertices_3d,
        'entry_vertice_x': entry_vertice_x,
        'entry_vertice_y': entry_vertice_y,
        'entry_vertice_z': entry_vertice_z,
        'texto_vertices_3d': texto_vertices_3d,
        'frame_definir_arestas_3d': frame_definir_arestas_3d,
        'combo_aresta_de': combo_aresta_de,
        'combo_aresta_para': combo_aresta_para,
        'texto_arestas_3d': texto_arestas_3d,
        'combo_tipo_projecao': combo_tipo_projecao,
        'label_distancia_proj': label_distancia_proj,
        'entry_distancia_proj': entry_distancia_proj,
        'btn_projetar_objeto': btn_projetar_objeto
    }