# main.py
import tkinter as tk
from tkinter import ttk, messagebox
import math
from grid import Grid
from bresenham import Bresenham
from polilinha import Polilinha
from circulo import Circulo
from elipse import Elipse
from curvas import Curvas
from preenchimentoRecursivo import PreenchimentoRecursivo
from varredura import Varredura
from recorteLinha import RecorteLinha

# --- Variáveis Globais de Estado ---
pontos_selecionados = []
poligono_para_preencher = []
janela_de_recorte = {}
estado_preenchimento = "desenhando_poligono"
estado_recorte = "definindo_janela"

# --- Funções de Lógica ---
def handle_grid_click(event):
    global pontos_selecionados
    grid_x, grid_y = tela.converter_para_coordenadas_grid(event.x, event.y)
    modo = current_mode.get()
    
    if not pontos_selecionados and modo not in ["preenchimento", "recorte"]:
        tela.limpar_tela()

    max_points = {"linha": 2, "circulo": 2, "elipse": 3}
    if modo in max_points and len(pontos_selecionados) >= max_points[modo]:
        limpar_tudo(manter_desenho=False)

    if modo == "recorte":
        if estado_recorte == "definindo_janela":
            if len(pontos_selecionados) >= 2: limpar_tudo(manter_desenho=False)
            pontos_selecionados.append((grid_x, grid_y))
            tela.desenhar_pixel(grid_x, grid_y, "red")
            if len(pontos_selecionados) == 1:
                entry_xmin.delete(0, tk.END); entry_xmin.insert(0, str(grid_x))
                entry_ymin.delete(0, tk.END); entry_ymin.insert(0, str(grid_y))
            elif len(pontos_selecionados) == 2:
                entry_xmax.delete(0, tk.END); entry_xmax.insert(0, str(grid_x))
                entry_ymax.delete(0, tk.END); entry_ymax.insert(0, str(grid_y))
        elif estado_recorte == "definindo_linha":
            if len(pontos_selecionados) >= 2:
                limpar_tudo(manter_desenho=True, limpar_apenas_pontos=True)
                tela.destacar_janela(**janela_de_recorte)
            pontos_selecionados.append((grid_x, grid_y))
            tela.desenhar_pixel(grid_x, grid_y, "blue")
            if len(pontos_selecionados) == 1:
                entry_x0_recorte.delete(0, tk.END); entry_x0_recorte.insert(0, str(grid_x))
                entry_y0_recorte.delete(0, tk.END); entry_y0_recorte.insert(0, str(grid_y))
            elif len(pontos_selecionados) == 2:
                entry_x1_recorte.delete(0, tk.END); entry_x1_recorte.insert(0, str(grid_x))
                entry_y1_recorte.delete(0, tk.END); entry_y1_recorte.insert(0, str(grid_y))
                desenhar_linha_original_para_recorte()
    elif modo == "preenchimento":
        if estado_preenchimento == "escolhendo_semente":
            if not ponto_esta_dentro((grid_x, grid_y), poligono_para_preencher): messagebox.showwarning("Ponto Inválido", "O ponto de semente deve estar DENTRO do polígono."); return
            if tela.checar_matriz(grid_x, grid_y) == '#000000': messagebox.showwarning("Ponto Inválido", "O ponto de semente não pode estar sobre uma borda."); return
            tela.limpar_marcadores(); pontos_selecionados = [(grid_x, grid_y)]; tela.desenhar_marcador_temporario(grid_x, grid_y, "cyan") 
            entry_p_x_fill.delete(0, tk.END); entry_p_x_fill.insert(0, str(grid_x)); entry_p_y_fill.delete(0, tk.END); entry_p_y_fill.insert(0, str(grid_y))
        else: pontos_selecionados.append((grid_x, grid_y)); tela.desenhar_pixel(grid_x, grid_y, "blue"); atualizar_texto_pontos()
    elif modo in ["polilinha", "varredura", "curva"]:
        pontos_selecionados.append((grid_x, grid_y)); cor = "blue"
        if modo == "varredura": cor = "magenta"
        elif modo == "curva":
            if len(pontos_selecionados) == 1: cor = "green"
            else:
                if len(pontos_selecionados) > 2: tela.desenhar_pixel(pontos_selecionados[-2][0], pontos_selecionados[-2][1], "orange")
                cor = "red"
        tela.desenhar_pixel(grid_x, grid_y, cor); atualizar_texto_pontos()
    elif modo in ["linha", "circulo", "elipse"]:
        pontos_selecionados.append((grid_x, grid_y))
        cor_ponto = {"linha": "blue", "circulo": "green", "elipse": "purple"}
        tela.desenhar_pixel(grid_x, grid_y, cor_ponto[modo])
        if modo == "linha":
            if len(pontos_selecionados) == 1: entry_x0.delete(0, tk.END); entry_x0.insert(0, str(grid_x)); entry_y0.delete(0, tk.END); entry_y0.insert(0, str(grid_y))
            elif len(pontos_selecionados) == 2: entry_x1.delete(0, tk.END); entry_x1.insert(0, str(grid_x)); entry_y1.delete(0, tk.END); entry_y1.insert(0, str(grid_y))
        elif modo == "circulo":
            if len(pontos_selecionados) == 1: entry_cx.delete(0, tk.END); entry_cx.insert(0, str(grid_x)); entry_cy.delete(0, tk.END); entry_cy.insert(0, str(grid_y))
            elif len(pontos_selecionados) == 2: p1,p2=pontos_selecionados; raio=math.sqrt((p2[0]-p1[0])**2+(p2[1]-p1[1])**2); entry_raio.delete(0,tk.END); entry_raio.insert(0,f"{raio:.2f}"); desenhar_circulo()
        elif modo == "elipse":
            if len(pontos_selecionados) == 1: entry_ex.delete(0, tk.END); entry_ex.insert(0, str(grid_x)); entry_ey.delete(0, tk.END); entry_ey.insert(0, str(grid_y))
            elif len(pontos_selecionados) == 2: raio_x=abs(pontos_selecionados[1][0]-pontos_selecionados[0][0]); entry_rx.delete(0,tk.END); entry_rx.insert(0,str(raio_x))
            elif len(pontos_selecionados) == 3: raio_y=abs(pontos_selecionados[2][1]-pontos_selecionados[0][1]); entry_ry.delete(0,tk.END); entry_ry.insert(0,str(raio_y)); desenhar_elipse()

def ponto_esta_dentro(ponto, poligono):
    x, y = ponto; n = len(poligono); dentro = False; p1x, p1y = poligono[0]
    for i in range(n + 1):
        p2x, p2y = poligono[i % n]
        if y > min(p1y, p2y) and y <= max(p1y, p2y) and x <= max(p1x, p2x):
            if p1y != p2y: xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
            if p1x == p2x or x <= xinters: dentro = not dentro
        p1x, p1y = p2x, p2y
    return dentro

def add_point_from_entry():
    global pontos_selecionados; modo=current_mode.get(); entry_map={"polilinha":(entry_p_x_pv,entry_p_y_pv),"varredura":(entry_p_x_varredura,entry_p_y_varredura),"curva":(entry_p_x_curva,entry_p_y_curva),"preenchimento":(entry_p_x_preenchimento,entry_p_y_preenchimento)}
    if modo not in entry_map: return
    entry_x, entry_y = entry_map[modo]
    try: x=int(entry_x.get()); y=int(entry_y.get())
    except ValueError: messagebox.showerror("Entrada Inválida", "As coordenadas do ponto devem ser números inteiros."); return
    if not pontos_selecionados: tela.limpar_tela()
    pontos_selecionados.append((x, y)); cor="blue"
    if modo=="varredura": cor="magenta"
    elif modo=="curva":
        if len(pontos_selecionados)==1: cor="green"
        else: cor="red"
    tela.desenhar_pixel(x,y,cor)
    if modo=="curva" and len(pontos_selecionados)>2: p_anterior=pontos_selecionados[-2]; tela.desenhar_pixel(p_anterior[0],p_anterior[1],"orange")
    atualizar_texto_pontos(); entry_x.delete(0,tk.END); entry_y.delete(0,tk.END)

def desenhar_linha():
    try: p1=(int(entry_x0.get()),int(entry_y0.get())); p2=(int(entry_x1.get()),int(entry_y1.get()))
    except ValueError: messagebox.showerror("Entrada Inválida", "As coordenadas devem ser números inteiros."); limpar_tudo(manter_desenho=True); return
    tela.limpar_tela(); linha=Bresenham(p1, p2); tela.desenhar(linha.saida,'#000000'); tela.desenhar_pixel(p1[0],p1[1],"blue"); tela.desenhar_pixel(p2[0],p2[1],"blue")

def desenhar_polilinha():
    if len(pontos_selecionados)<2: messagebox.showwarning("Pontos Insuficientes", "São necessários pelo menos 2 pontos para desenhar uma polilinha."); return
    pontos_para_desenhar = list(pontos_selecionados); tela.limpar_tela() 
    polilinha=Polilinha(pontos_para_desenhar, fechar=False); tela.desenhar(polilinha.saida,'#000000')
    for ponto in pontos_para_desenhar: tela.desenhar_pixel(ponto[0],ponto[1],"blue")

def desenhar_circulo():
    try: centro=(int(entry_cx.get()),int(entry_cy.get())); raio=float(entry_raio.get())
    except ValueError: messagebox.showerror("Entrada Inválida", "O centro deve ter coordenadas inteiras e o raio um número."); limpar_tudo(manter_desenho=True); return
    if raio <= 0: messagebox.showwarning("Raio Inválido", "O raio do círculo deve ser maior que zero."); limpar_tudo(manter_desenho=True); return
    tela.limpar_tela(); circulo=Circulo(centro, raio); tela.desenhar(circulo.saida,'#000000'); tela.desenhar_pixel(centro[0],centro[1],"green")

def desenhar_elipse():
    try: centro=(int(entry_ex.get()),int(entry_ey.get())); rx=float(entry_rx.get()); ry=float(entry_ry.get())
    except ValueError: messagebox.showerror("Entrada Inválida", "O centro deve ter coordenadas inteiras e os raios números."); limpar_tudo(manter_desenho=True); return
    if rx <= 0 or ry <= 0: messagebox.showwarning("Raios Inválidos", "Os raios X e Y devem ser maiores que zero."); limpar_tudo(manter_desenho=True); return
    tela.limpar_tela(); elipse=Elipse(centro, rx, ry); tela.desenhar(elipse.saida,'#000000'); tela.desenhar_pixel(centro[0],centro[1],"purple")

def desenhar_curva():
    if len(pontos_selecionados) < 3: messagebox.showwarning("Pontos Insuficientes", "São necessários pelo menos 3 pontos de controle para uma curva."); return
    pontos_para_desenhar = list(pontos_selecionados); tela.limpar_tela()
    curva = Curvas(pontos_para_desenhar); tela.desenhar(curva.saida, '#000000')
    for i, ponto in enumerate(pontos_para_desenhar):
        if i == 0: cor = "green"
        elif i == len(pontos_para_desenhar) - 1: cor = "red"
        else: cor = "orange"
        tela.desenhar_pixel(ponto[0], ponto[1], cor)

def finalizar_poligono_para_preenchimento():
    global estado_preenchimento, poligono_para_preencher
    if len(pontos_selecionados) < 3: messagebox.showerror("Polígono Inválido", "São necessários pelo menos 3 pontos para formar um polígono."); return
    tela.limpar_tela(); poligono_para_preencher = list(pontos_selecionados)
    poligono_fechado = Polilinha(poligono_para_preencher, fechar=True); tela.desenhar(poligono_fechado.saida, '#000000')
    estado_preenchimento = "escolhendo_semente"; pontos_selecionados.clear(); atualizar_texto_pontos(); switch_fill_state()

def executar_preenchimento():
    try: ponto_semente = (int(entry_p_x_fill.get()), int(entry_p_y_fill.get())); cor = entry_cor_preenchimento.get()
    except ValueError: messagebox.showerror("Entrada Inválida", "As coordenadas do ponto de semente devem ser números inteiros."); return
    if not (cor.startswith('#') and len(cor) == 7): messagebox.showerror("Cor Inválida", "A cor deve estar no formato #RRGGBB."); return
    if not poligono_para_preencher: messagebox.showwarning("Nenhum Polígono", "Primeiro, finalize um polígono para depois o preencher."); return
    if not ponto_esta_dentro(ponto_semente, poligono_para_preencher): messagebox.showwarning("Ponto Inválido", "O ponto de semente deve estar DENTRO do polígono."); return
    tela.limpar_marcadores(); PreenchimentoRecursivo(ponto_semente, cor, tela); limpar_tudo(manter_desenho=True, limpar_apenas_pontos=True)

def executar_varredura():
    if len(pontos_selecionados) < 3: messagebox.showwarning("Pontos Insuficientes", "São necessários pelo menos 3 pontos para preencher com varredura."); return
    pontos_para_desenhar = list(pontos_selecionados); tela.limpar_tela()
    preenchimento = Varredura(pontos_para_desenhar); tela.desenhar(preenchimento.saida, "#FFA500")
    borda = Polilinha(pontos_para_desenhar, fechar=True); tela.desenhar(borda.saida, '#000000')

def finalizar_janela_de_recorte():
    global estado_recorte, janela_de_recorte
    try:
        x_coords = [int(entry_xmin.get()), int(entry_xmax.get())]; y_coords = [int(entry_ymin.get()), int(entry_ymax.get())]
    except ValueError: messagebox.showerror("Entrada Inválida", "As coordenadas da janela devem ser números inteiros."); return
    xmin, xmax = min(x_coords), max(x_coords); ymin, ymax = min(y_coords), max(y_coords)
    # --- CORREÇÃO AQUI ---
    janela_de_recorte = {'xmin': xmin, 'ymin': ymin, 'xmax': xmax, 'ymax': ymax}
    tela.limpar_tela(); tela.destacar_janela(**janela_de_recorte)
    estado_recorte = "definindo_linha"; pontos_selecionados.clear(); switch_clip_state()

def desenhar_linha_original_para_recorte():
    try: p1 = (int(entry_x0_recorte.get()), int(entry_y0_recorte.get())); p2 = (int(entry_x1_recorte.get()), int(entry_y1_recorte.get()))
    except ValueError: return
    linha_original = Bresenham(p1, p2)
    tela.desenhar(linha_original.saida, 'lightgrey')

def executar_recorte_linha():
    if not janela_de_recorte: messagebox.showwarning("Janela não Definida", "Primeiro, defina uma janela de recorte."); return
    try:
        p1 = (int(entry_x0_recorte.get()), int(entry_y0_recorte.get()))
        p2 = (int(entry_x1_recorte.get()), int(entry_y1_recorte.get()))
    except ValueError: messagebox.showerror("Entrada Inválida", "As coordenadas da linha devem ser números inteiros."); return
    
    tela.limpar_tela()
    tela.destacar_janela(**janela_de_recorte)
    recorte = RecorteLinha(p1, p2, **janela_de_recorte)
    tela.desenhar(recorte.saida, '#000000')

def limpar_tudo(manter_desenho=False, limpar_apenas_pontos=False):
    global pontos_selecionados; tela.limpar_marcadores()
    if not limpar_apenas_pontos:
        entries = [entry_x0, entry_y0, entry_x1, entry_y1, entry_cx, entry_cy, entry_raio, entry_ex, entry_ey, entry_rx, entry_ry, entry_p_x_fill, entry_p_y_fill, entry_p_x_pv, entry_p_y_pv, entry_p_x_curva, entry_p_y_curva, entry_p_x_preenchimento, entry_p_y_preenchimento, entry_p_x_varredura, entry_p_y_varredura, entry_x0_recorte, entry_y0_recorte, entry_x1_recorte, entry_y1_recorte, entry_xmin, entry_ymin, entry_xmax, entry_ymax]
        for entry in entries:
            if entry.winfo_exists(): entry.delete(0, tk.END)
        text_widgets = [texto_pontos_polilinha, texto_pontos_curva, texto_pontos_varredura, texto_pontos_preenchimento]
        for widget in text_widgets:
            if widget.winfo_exists(): widget.config(state=tk.NORMAL); widget.delete('1.0', tk.END); widget.config(state=tk.DISABLED)
    pontos_selecionados = []
    if not manter_desenho:
        tela.limpar_tela()

def atualizar_texto_pontos():
    modo = current_mode.get(); widgets_map = {"polilinha": texto_pontos_polilinha, "curva": texto_pontos_curva, "varredura": texto_pontos_varredura, "preenchimento": texto_pontos_preenchimento}
    if modo not in widgets_map: return
    widget = widgets_map[modo]; widget.config(state=tk.NORMAL); widget.delete('1.0', tk.END)
    for ponto in pontos_selecionados: widget.insert(tk.END, f"({ponto[0]}, {ponto[1]})\n")
    widget.config(state=tk.DISABLED)

def switch_mode():
    global estado_preenchimento, poligono_para_preencher, estado_recorte, janela_de_recorte
    estado_preenchimento="desenhando_poligono"; poligono_para_preencher=[]; estado_recorte="definindo_janela"; janela_de_recorte={}
    limpar_tudo(manter_desenho=False); modo = current_mode.get()
    for frame in [frame_linha, frame_polilinha, frame_circulo, frame_elipse, frame_curva, frame_preenchimento, frame_varredura, frame_recorte]:
        frame.pack_forget()
    frames_map = {"linha":frame_linha, "polilinha":frame_polilinha, "circulo":frame_circulo, "elipse":frame_elipse, "curva":frame_curva, "varredura":frame_varredura, "preenchimento":frame_preenchimento, "recorte":frame_recorte}
    if modo in frames_map:
        frames_map[modo].pack(pady=10, padx=10, fill="x")
        if modo == "preenchimento": switch_fill_state()
        elif modo == "recorte": switch_clip_state()

def switch_fill_state():
    if estado_preenchimento == "desenhando_poligono":
        frame_desenho_poligono.pack(fill="x"); frame_escolha_semente.pack_forget()
    else: frame_desenho_poligono.pack_forget(); frame_escolha_semente.pack(fill="x")
    
def switch_clip_state():
    if estado_recorte == "definindo_janela":
        frame_definir_janela.pack(fill="x"); frame_definir_linha.pack_forget()
    else: frame_definir_janela.pack_forget(); frame_definir_linha.pack(fill="x")

# ===================================================================
# Bloco 2: Criação da Interface Gráfica
# ===================================================================
tela = Grid(550)
current_mode = tk.StringVar(master=tela.master, value="linha")
tela.tela.bind("<Button-1>", handle_grid_click)
tela.tela.pack(side=tk.LEFT, padx=10, pady=10)
controls_frame_main = tk.Frame(tela.master); controls_frame_main.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.Y)
mode_frame = ttk.LabelFrame(controls_frame_main, text="Modo de Desenho"); mode_frame.pack(pady=10, padx=10, fill="x")
modos = ["Linha", "Polilinha", "Círculo", "Elipse", "Curva", "Preenchimento", "Varredura", "Recorte de Linha"]
valores = ["linha", "polilinha", "circulo", "elipse", "curva", "preenchimento", "varredura", "recorte"]
for i in range(len(modos)):
    ttk.Radiobutton(mode_frame, text=modos[i], variable=current_mode, value=valores[i], command=switch_mode).pack(anchor="w")
dynamic_controls_frame = tk.Frame(controls_frame_main); dynamic_controls_frame.pack(pady=10, padx=10, fill="both", expand=True)
frame_linha=ttk.LabelFrame(dynamic_controls_frame, text="Controles da Linha")
frame_polilinha=ttk.LabelFrame(dynamic_controls_frame, text="Controles da Polilinha")
frame_circulo=ttk.LabelFrame(dynamic_controls_frame, text="Controles do Círculo")
frame_elipse=ttk.LabelFrame(dynamic_controls_frame, text="Controles da Elipse")
frame_curva=ttk.LabelFrame(dynamic_controls_frame, text="Controles da Curva")
frame_preenchimento=ttk.LabelFrame(dynamic_controls_frame, text="Controles de Preenchimento")
frame_varredura=ttk.LabelFrame(dynamic_controls_frame, text="Controles de Varredura")
frame_recorte=ttk.LabelFrame(dynamic_controls_frame, text="Controles de Recorte de Linha")
tk.Label(frame_linha, text="P1 (x0, y0)").pack(); entry_x0=tk.Entry(frame_linha, width=10); entry_x0.pack(); entry_y0=tk.Entry(frame_linha, width=10); entry_y0.pack()
tk.Label(frame_linha, text="P2 (x1, y1)").pack(pady=(10,0)); entry_x1=tk.Entry(frame_linha, width=10); entry_x1.pack(); entry_y1=tk.Entry(frame_linha, width=10); entry_y1.pack()
ttk.Button(frame_linha, text="Desenhar Linha", command=desenhar_linha).pack(pady=10, fill="x")
tk.Label(frame_polilinha, text="Adicionar Ponto (x, y)").pack(); entry_p_x_pv=tk.Entry(frame_polilinha, width=10); entry_p_x_pv.pack(); entry_p_y_pv=tk.Entry(frame_polilinha, width=10); entry_p_y_pv.pack()
ttk.Button(frame_polilinha, text="Adicionar Ponto", command=add_point_from_entry).pack(pady=5, fill="x")
tk.Label(frame_polilinha, text="Pontos:").pack(pady=(10,0)); texto_pontos_polilinha = tk.Text(frame_polilinha, height=5, width=20); texto_pontos_polilinha.pack(pady=5); texto_pontos_polilinha.config(state=tk.DISABLED)
ttk.Button(frame_polilinha, text="Desenhar Polilinha", command=desenhar_polilinha).pack(pady=5, fill="x")
tk.Label(frame_curva, text="Adicionar Ponto (x, y)").pack(); entry_p_x_curva=tk.Entry(frame_curva, width=10); entry_p_x_curva.pack(); entry_p_y_curva=tk.Entry(frame_curva, width=10); entry_p_y_curva.pack()
ttk.Button(frame_curva, text="Adicionar Ponto", command=add_point_from_entry).pack(pady=5, fill="x")
tk.Label(frame_curva, text="Pontos de Controle:").pack(pady=5); texto_pontos_curva = tk.Text(frame_curva, height=8, width=20); texto_pontos_curva.pack(pady=5); texto_pontos_curva.config(state=tk.DISABLED)
ttk.Button(frame_curva, text="Desenhar Curva", command=desenhar_curva).pack(pady=10, fill="x")
tk.Label(frame_circulo, text="Centro (cx, cy)").pack(); entry_cx=tk.Entry(frame_circulo, width=10); entry_cx.pack(); entry_cy=tk.Entry(frame_circulo, width=10); entry_cy.pack()
tk.Label(frame_circulo, text="Raio").pack(pady=(10,0)); entry_raio=tk.Entry(frame_circulo, width=10); entry_raio.pack()
ttk.Button(frame_circulo, text="Desenhar Círculo", command=desenhar_circulo).pack(pady=10, fill="x")
tk.Label(frame_elipse, text="Centro (cx, cy)").pack(); entry_ex=tk.Entry(frame_elipse, width=10); entry_ex.pack(); entry_ey=tk.Entry(frame_elipse, width=10); entry_ey.pack()
tk.Label(frame_elipse, text="Raio X (rx)").pack(pady=(10,0)); entry_rx=tk.Entry(frame_elipse, width=10); entry_rx.pack()
tk.Label(frame_elipse, text="Raio Y (ry)").pack(pady=(10,0)); entry_ry=tk.Entry(frame_elipse, width=10); entry_ry.pack()
ttk.Button(frame_elipse, text="Desenhar Elipse", command=desenhar_elipse).pack(pady=10, fill="x")
frame_desenho_poligono = tk.Frame(frame_preenchimento)
tk.Label(frame_desenho_poligono, text="1. Adicionar Vértice (x, y)").pack(); entry_p_x_preenchimento=tk.Entry(frame_desenho_poligono, width=10); entry_p_x_preenchimento.pack(); entry_p_y_preenchimento=tk.Entry(frame_desenho_poligono, width=10); entry_p_y_preenchimento.pack()
ttk.Button(frame_desenho_poligono, text="Adicionar Vértice", command=add_point_from_entry).pack(pady=5)
tk.Label(frame_desenho_poligono, text="Vértices:").pack(); texto_pontos_preenchimento = tk.Text(frame_desenho_poligono, height=5, width=20); texto_pontos_preenchimento.pack(pady=5); texto_pontos_preenchimento.config(state=tk.DISABLED)
ttk.Button(frame_desenho_poligono, text="Finalizar Polígono", command=finalizar_poligono_para_preenchimento).pack(pady=5, fill="x")
frame_escolha_semente = tk.Frame(frame_preenchimento)
tk.Label(frame_escolha_semente, text="2. Ponto de Semente (x, y)").pack(); entry_p_x_fill=tk.Entry(frame_escolha_semente, width=10); entry_p_x_fill.pack(); entry_p_y_fill=tk.Entry(frame_escolha_semente, width=10); entry_p_y_fill.pack()
tk.Label(frame_escolha_semente, text="Cor:").pack(pady=(10,0)); entry_cor_preenchimento = tk.Entry(frame_escolha_semente, width=10); entry_cor_preenchimento.pack()
entry_cor_preenchimento.insert(0, "#FF0000"); ttk.Button(frame_escolha_semente, text="Preencher", command=executar_preenchimento).pack(pady=10, fill="x")
tk.Label(frame_varredura, text="Adicionar Vértice (x, y)").pack(); entry_p_x_varredura=tk.Entry(frame_varredura, width=10); entry_p_x_varredura.pack(); entry_p_y_varredura=tk.Entry(frame_varredura, width=10); entry_p_y_varredura.pack()
ttk.Button(frame_varredura, text="Adicionar Vértice", command=add_point_from_entry).pack(pady=5, fill="x")
tk.Label(frame_varredura, text="Vértices do Polígono:").pack(pady=5); texto_pontos_varredura = tk.Text(frame_varredura, height=8, width=20); texto_pontos_varredura.pack(pady=5); texto_pontos_varredura.config(state=tk.DISABLED)
ttk.Button(frame_varredura, text="Preencher com Varredura", command=executar_varredura).pack(pady=10, fill="x")
frame_definir_janela = tk.Frame(frame_recorte)
tk.Label(frame_definir_janela, text="1. Defina a Janela de Recorte:").pack()
tk.Label(frame_definir_janela, text="Ponto 1 (xmin, ymin)").pack(); entry_xmin=tk.Entry(frame_definir_janela, width=10); entry_xmin.pack(); entry_ymin=tk.Entry(frame_definir_janela, width=10); entry_ymin.pack()
tk.Label(frame_definir_janela, text="Ponto 2 (xmax, ymax)").pack(pady=(5,0)); entry_xmax=tk.Entry(frame_definir_janela, width=10); entry_xmax.pack(); entry_ymax=tk.Entry(frame_definir_janela, width=10); entry_ymax.pack()
ttk.Button(frame_definir_janela, text="Finalizar Janela", command=finalizar_janela_de_recorte).pack(pady=10, fill="x")
frame_definir_linha = tk.Frame(frame_recorte)
tk.Label(frame_definir_linha, text="2. Defina a Linha a ser Recortada:").pack()
tk.Label(frame_definir_linha, text="Ponto 1 (x0, y0)").pack(); entry_x0_recorte=tk.Entry(frame_definir_linha, width=10); entry_x0_recorte.pack(); entry_y0_recorte=tk.Entry(frame_definir_linha, width=10); entry_y0_recorte.pack()
tk.Label(frame_definir_linha, text="Ponto 2 (x1, y1)").pack(pady=(5,0)); entry_x1_recorte=tk.Entry(frame_definir_linha, width=10); entry_x1_recorte.pack(); entry_y1_recorte=tk.Entry(frame_definir_linha, width=10); entry_y1_recorte.pack()
ttk.Button(frame_definir_linha, text="Recortar Linha", command=executar_recorte_linha).pack(pady=10, fill="x")
ttk.Button(controls_frame_main, text="Limpar Tudo", command=lambda: limpar_tudo(manter_desenho=False)).pack(pady=10, padx=10, side="bottom", fill="x")
switch_mode()
tela.iniciar()