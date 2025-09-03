# main.py
import tkinter as tk
from tkinter import ttk
import math
from grid import Grid
from bresenham import Bresenham
from polilinha import Polilinha
from circulo import Circulo
from elipse import Elipse
from curvas import Curvas

# --- Variáveis Globais de Estado ---
pontos_selecionados = []
# A variável 'current_mode' será inicializada APÓS a criação da janela principal.

# --- Funções de Lógica ---
def handle_grid_click(event):
    """Função central que lida com cliques na malha, agindo de acordo com o modo."""
    grid_x, grid_y = tela.converter_para_coordenadas_grid(event.x, event.y)
    
    modo = current_mode.get()
    
    if modo == "linha":
        if len(pontos_selecionados) >= 2: limpar_tudo()
        pontos_selecionados.append((grid_x, grid_y))
        tela.desenhar_pixel(grid_x, grid_y, "blue")
        if len(pontos_selecionados) == 1:
            entry_x0.delete(0, tk.END); entry_x0.insert(0, str(grid_x))
            entry_y0.delete(0, tk.END); entry_y0.insert(0, str(grid_y))
        elif len(pontos_selecionados) == 2:
            entry_x1.delete(0, tk.END); entry_x1.insert(0, str(grid_x))
            entry_y1.delete(0, tk.END); entry_y1.insert(0, str(grid_y))
            desenhar_linha()
            
    elif modo in ["polilinha", "curva"]:
        pontos_selecionados.append((grid_x, grid_y))
        tela.desenhar_pixel(grid_x, grid_y, "orange" if modo == "curva" else "blue")
        atualizar_texto_pontos()

    elif modo == "circulo":
        if len(pontos_selecionados) >= 2: limpar_tudo()
        pontos_selecionados.append((grid_x, grid_y))
        tela.desenhar_pixel(grid_x, grid_y, "green")
        if len(pontos_selecionados) == 1: # Ponto central
            entry_cx.delete(0, tk.END); entry_cx.insert(0, str(grid_x))
            entry_cy.delete(0, tk.END); entry_cy.insert(0, str(grid_y))
        elif len(pontos_selecionados) == 2: # Ponto da borda
            p1 = pontos_selecionados[0]; p2 = pontos_selecionados[1]
            raio = math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
            entry_raio.delete(0, tk.END); entry_raio.insert(0, f"{raio:.2f}")
            desenhar_circulo()

    elif modo == "elipse":
        if len(pontos_selecionados) >= 3: limpar_tudo()
        pontos_selecionados.append((grid_x, grid_y))
        tela.desenhar_pixel(grid_x, grid_y, "purple")
        if len(pontos_selecionados) == 1: # Centro
            entry_ex.delete(0, tk.END); entry_ex.insert(0, str(grid_x))
            entry_ey.delete(0, tk.END); entry_ey.insert(0, str(grid_y))
        elif len(pontos_selecionados) == 2: # Ponto do raio X
            raio_x = abs(pontos_selecionados[1][0] - pontos_selecionados[0][0])
            entry_rx.delete(0, tk.END); entry_rx.insert(0, str(raio_x))
        elif len(pontos_selecionados) == 3: # Ponto do raio Y
            raio_y = abs(pontos_selecionados[2][1] - pontos_selecionados[0][1])
            entry_ry.delete(0, tk.END); entry_ry.insert(0, str(raio_y))
            desenhar_elipse()

# --- Funções de Desenho ---
def desenhar_linha():
    try: p1=(int(entry_x0.get()),int(entry_y0.get())); p2=(int(entry_x1.get()),int(entry_y1.get()))
    except ValueError: return
    tela.limpar_tela(); linha=Bresenham(p1, p2); tela.desenhar(linha.saida,'#000000')
    tela.desenhar_pixel(p1[0],p1[1],"blue"); tela.desenhar_pixel(p2[0],p2[1],"blue")

def desenhar_polilinha(fechar=False):
    if len(pontos_selecionados)<2: return
    tela.limpar_tela(); polilinha=Polilinha(pontos_selecionados, fechar=fechar); tela.desenhar(polilinha.saida,'#000000')
    for ponto in pontos_selecionados: tela.desenhar_pixel(ponto[0],ponto[1],"blue")

def desenhar_circulo():
    try: centro=(int(entry_cx.get()),int(entry_cy.get())); raio=float(entry_raio.get())
    except ValueError: return
    tela.limpar_tela(); circulo=Circulo(centro, raio); tela.desenhar(circulo.saida,'#000000')
    tela.desenhar_pixel(centro[0],centro[1],"green")

def desenhar_elipse():
    try: centro=(int(entry_ex.get()),int(entry_ey.get())); rx=float(entry_rx.get()); ry=float(entry_ry.get())
    except ValueError: return
    tela.limpar_tela(); elipse=Elipse(centro, rx, ry); tela.desenhar(elipse.saida,'#000000')
    tela.desenhar_pixel(centro[0],centro[1],"purple")

def desenhar_curva():
    """Desenha uma Curva de Bézier, mostrando apenas a curva final."""
    if len(pontos_selecionados) < 2:
        print("Selecione pelo menos dois pontos de controle para a curva.")
        return
    tela.limpar_tela()
    curva = Curvas(pontos_selecionados)
    
    # Apenas a rasterização da curva é desenhada
    tela.desenhar(curva.saida, '#000000')

# --- Funções de UI e Limpeza ---
def limpar_tudo():
    global pontos_selecionados; pontos_selecionados = []; tela.limpar_tela()
    for entry in [entry_x0, entry_y0, entry_x1, entry_y1, entry_px, entry_py, entry_cx, entry_cy, entry_raio, entry_ex, entry_ey, entry_rx, entry_ry]:
        entry.delete(0, tk.END)
    texto_pontos.config(state=tk.NORMAL); texto_pontos.delete('1.0', tk.END); texto_pontos.config(state=tk.DISABLED)

def atualizar_texto_pontos():
    texto_pontos.config(state=tk.NORMAL); texto_pontos.delete('1.0', tk.END)
    for ponto in pontos_selecionados: texto_pontos.insert(tk.END, f"({ponto[0]}, {ponto[1]})\n")
    texto_pontos.config(state=tk.DISABLED)

def switch_mode():
    limpar_tudo()
    modo = current_mode.get()
    for frame in [frame_linha, frame_polilinha, frame_circulo, frame_elipse, frame_curva]:
        frame.pack_forget()
    if modo == "linha": frame_linha.pack(pady=10, padx=10, fill="x")
    elif modo == "polilinha": frame_polilinha.pack(pady=10, padx=10, fill="x")
    elif modo == "circulo": frame_circulo.pack(pady=10, padx=10, fill="x")
    elif modo == "elipse": frame_elipse.pack(pady=10, padx=10, fill="x")
    elif modo == "curva": frame_curva.pack(pady=10, padx=10, fill="x")

# --- Configuração da Interface Gráfica ---
tela = Grid(550)
current_mode = tk.StringVar(master=tela.master, value="linha")
tela.tela.bind("<Button-1>", handle_grid_click)
tela.tela.pack(side=tk.LEFT, padx=10, pady=10)

controls_frame = tk.Frame(tela.master); controls_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.Y)
mode_frame = ttk.LabelFrame(controls_frame, text="Modo de Desenho"); mode_frame.pack(pady=10, padx=10, fill="x")
modos = ["Linha", "Polilinha", "Círculo", "Elipse", "Curva"]
valores = ["linha", "polilinha", "circulo", "elipse", "curva"]
for i in range(len(modos)):
    ttk.Radiobutton(mode_frame, text=modos[i], variable=current_mode, value=valores[i], command=switch_mode).pack(anchor="w")

# --- Frames de Controles ---
frame_linha = ttk.LabelFrame(controls_frame, text="Controles da Linha")
frame_polilinha = ttk.LabelFrame(controls_frame, text="Controles da Polilinha")
frame_circulo = ttk.LabelFrame(controls_frame, text="Controles do Círculo")
frame_elipse = ttk.LabelFrame(controls_frame, text="Controles da Elipse")
frame_curva = ttk.LabelFrame(controls_frame, text="Controles da Curva")

# Conteúdo do Frame Curva
tk.Label(frame_curva, text="Adicione 2 ou mais pontos de controle\nclicando na malha.").pack(pady=5)
tk.Label(frame_curva, text="Pontos de Controle:").pack(pady=(10,0))
texto_pontos_curva = tk.Text(frame_curva, height=8, width=20)
texto_pontos_curva.pack(pady=5)
texto_pontos_curva.config(state=tk.DISABLED)
ttk.Button(frame_curva, text="Desenhar Curva", command=desenhar_curva).pack(pady=10, fill="x")

# --- Botão de Limpar Global ---
ttk.Button(controls_frame, text="Limpar Tudo", command=limpar_tudo).pack(pady=20, fill="x", side="bottom")

# Preenche os frames (mantém o código anterior para os outros frames)
# Frame Linha
tk.Label(frame_linha, text="P1 (x0, y0)").pack(); entry_x0 = tk.Entry(frame_linha, width=10); entry_x0.pack(); entry_y0 = tk.Entry(frame_linha, width=10); entry_y0.pack()
tk.Label(frame_linha, text="P2 (x1, y1)").pack(pady=(10,0)); entry_x1 = tk.Entry(frame_linha, width=10); entry_x1.pack(); entry_y1 = tk.Entry(frame_linha, width=10); entry_y1.pack()
ttk.Button(frame_linha, text="Desenhar Linha", command=desenhar_linha).pack(pady=10, fill="x")
# Frame Polilinha
tk.Label(frame_polilinha, text="Adicionar Ponto (x, y)").pack(); entry_px = tk.Entry(frame_polilinha, width=10); entry_px.pack(); entry_py = tk.Entry(frame_polilinha, width=10); entry_py.pack()
ttk.Button(frame_polilinha, text="Adicionar Ponto").pack(pady=5, fill="x") 
tk.Label(frame_polilinha, text="Pontos:").pack(pady=(10,0)); texto_pontos_polilinha = tk.Text(frame_polilinha, height=5, width=20); texto_pontos_polilinha.pack(pady=5); texto_pontos_polilinha.config(state=tk.DISABLED)
ttk.Button(frame_polilinha, text="Desenhar Polilinha", command=lambda: desenhar_polilinha(False)).pack(pady=5, fill="x")
ttk.Button(frame_polilinha, text="Fechar Polilinha", command=lambda: desenhar_polilinha(True)).pack(pady=5, fill="x")
# Atribui as caixas de texto à variável global 'texto_pontos' dependendo do modo
if current_mode.get() in ["polilinha", "curva"]:
    if current_mode.get() == "polilinha":
        texto_pontos = texto_pontos_polilinha
    else:
        texto_pontos = texto_pontos_curva

# Frame Círculo
tk.Label(frame_circulo, text="Centro (cx, cy)").pack(); entry_cx = tk.Entry(frame_circulo, width=10); entry_cx.pack(); entry_cy = tk.Entry(frame_circulo, width=10); entry_cy.pack()
tk.Label(frame_circulo, text="Raio").pack(pady=(10,0)); entry_raio = tk.Entry(frame_circulo, width=10); entry_raio.pack()
ttk.Button(frame_circulo, text="Desenhar Círculo", command=desenhar_circulo).pack(pady=10, fill="x")
# Frame Elipse
tk.Label(frame_elipse, text="Centro (cx, cy)").pack(); entry_ex = tk.Entry(frame_elipse, width=10); entry_ex.pack(); entry_ey = tk.Entry(frame_elipse, width=10); entry_ey.pack()
tk.Label(frame_elipse, text="Raio X (rx)").pack(pady=(10,0)); entry_rx = tk.Entry(frame_elipse, width=10); entry_rx.pack()
tk.Label(frame_elipse, text="Raio Y (ry)").pack(pady=(10,0)); entry_ry = tk.Entry(frame_elipse, width=10); entry_ry.pack()
ttk.Button(frame_elipse, text="Desenhar Elipse", command=desenhar_elipse).pack(pady=10, fill="x")

# --- Início da Aplicação ---
switch_mode()
tela.iniciar()