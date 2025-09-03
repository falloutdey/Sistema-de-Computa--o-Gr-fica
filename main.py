# main.py
import tkinter as tk
from tkinter import ttk
from grid import Grid
from bresenham import Bresenham
from polilinha import Polilinha

# --- Variáveis Globais de Estado ---
pontos_selecionados = []
# A variável 'current_mode' será inicializada APÓS a criação da janela principal.

# --- Funções de Lógica ---
def handle_grid_click(event):
    """Função central que lida com cliques na malha, agindo de acordo com o modo."""
    grid_x, grid_y = tela.converter_para_coordenadas_grid(event.x, event.y)

    if current_mode.get() == "linha":
        if len(pontos_selecionados) >= 2:
            limpar_tudo()
        
        pontos_selecionados.append((grid_x, grid_y))
        tela.desenhar_pixel(grid_x, grid_y, "blue")

        if len(pontos_selecionados) == 1:
            entry_x0.delete(0, tk.END); entry_x0.insert(0, str(grid_x))
            entry_y0.delete(0, tk.END); entry_y0.insert(0, str(grid_y))
        elif len(pontos_selecionados) == 2:
            entry_x1.delete(0, tk.END); entry_x1.insert(0, str(grid_x))
            entry_y1.delete(0, tk.END); entry_y1.insert(0, str(grid_y))
            desenhar_linha()

    elif current_mode.get() == "polilinha":
        pontos_selecionados.append((grid_x, grid_y))
        tela.desenhar_pixel(grid_x, grid_y, "blue")
        atualizar_texto_pontos()

def add_point_from_entry():
    """Adiciona um ponto à lista da polilinha a partir dos campos de texto."""
    try:
        x = int(entry_px.get())
        y = int(entry_py.get())
    except ValueError:
        print("Coordenadas inválidas.")
        return
    
    pontos_selecionados.append((x, y))
    tela.desenhar_pixel(x, y, "blue")
    atualizar_texto_pontos()
    entry_px.delete(0, tk.END)
    entry_py.delete(0, tk.END)

# --- Funções de Desenho ---
def desenhar_linha():
    """Desenha uma única linha baseada nos campos de entrada do Modo Linha."""
    try:
        p1 = (int(entry_x0.get()), int(entry_y0.get()))
        p2 = (int(entry_x1.get()), int(entry_y1.get()))
    except ValueError:
        print("Preencha as coordenadas da linha.")
        return
    
    tela.limpar_tela()
    linha = Bresenham(p1, p2)
    tela.desenhar(linha.saida, '#000000')
    tela.desenhar_pixel(p1[0], p1[1], "blue")
    tela.desenhar_pixel(p2[0], p2[1], "blue")

def desenhar_polilinha(fechar=False):
    """Desenha a polilinha baseada na lista de pontos selecionados."""
    if len(pontos_selecionados) < 2:
        print("Selecione pelo menos dois pontos.")
        return

    tela.limpar_tela()
    polilinha = Polilinha(pontos_selecionados, fechar=fechar)
    tela.desenhar(polilinha.saida, '#000000')
    for ponto in pontos_selecionados:
        tela.desenhar_pixel(ponto[0], ponto[1], "blue")

# --- Funções de UI e Limpeza ---
def limpar_tudo():
    """Reseta o estado da aplicação, limpando a tela e todos os campos."""
    global pontos_selecionados
    pontos_selecionados = []
    tela.limpar_tela()
    entry_x0.delete(0, tk.END); entry_y0.delete(0, tk.END)
    entry_x1.delete(0, tk.END); entry_y1.delete(0, tk.END)
    entry_px.delete(0, tk.END); entry_py.delete(0, tk.END)
    texto_pontos.config(state=tk.NORMAL)
    texto_pontos.delete('1.0', tk.END)
    texto_pontos.config(state=tk.DISABLED)

def atualizar_texto_pontos():
    """Atualiza a caixa de texto com a lista de pontos da polilinha."""
    texto_pontos.config(state=tk.NORMAL)
    texto_pontos.delete('1.0', tk.END)
    for ponto in pontos_selecionados:
        texto_pontos.insert(tk.END, f"({ponto[0]}, {ponto[1]})\n")
    texto_pontos.config(state=tk.DISABLED)

def switch_mode():
    """Alterna a visibilidade dos frames de controle com base no modo selecionado."""
    limpar_tudo()
    if current_mode.get() == "linha":
        frame_linha.pack(pady=10, padx=10, fill="x", expand=True)
        frame_polilinha.pack_forget()
    else:
        frame_linha.pack_forget()
        frame_polilinha.pack(pady=10, padx=10, fill="x", expand=True)

# --- Configuração da Interface Gráfica ---
tela = Grid(550)

# Inicializa a variável 'current_mode' APÓS a criação da janela 'tela.master'
current_mode = tk.StringVar(master=tela.master, value="linha")

tela.tela.bind("<Button-1>", handle_grid_click)
tela.tela.pack(side=tk.LEFT, padx=10, pady=10)

# --- Frame Principal de Controles (Lateral Direita) ---
controls_frame = tk.Frame(tela.master)
controls_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.Y)

# --- Seletor de Modo ---
mode_frame = ttk.LabelFrame(controls_frame, text="Modo de Desenho")
mode_frame.pack(pady=10, padx=10, fill="x")
ttk.Radiobutton(mode_frame, text="Linha", variable=current_mode, value="linha", command=switch_mode).pack(anchor="w")
ttk.Radiobutton(mode_frame, text="Polilinha", variable=current_mode, value="polilinha", command=switch_mode).pack(anchor="w")

# --- Frame para Controles do Modo Linha ---
frame_linha = ttk.LabelFrame(controls_frame, text="Controles da Linha")
tk.Label(frame_linha, text="Ponto Inicial (x0, y0)").pack()
entry_x0 = tk.Entry(frame_linha, width=10); entry_x0.pack()
entry_y0 = tk.Entry(frame_linha, width=10); entry_y0.pack()
tk.Label(frame_linha, text="Ponto Final (x1, y1)").pack(pady=(10,0))
entry_x1 = tk.Entry(frame_linha, width=10); entry_x1.pack()
entry_y1 = tk.Entry(frame_linha, width=10); entry_y1.pack()
ttk.Button(frame_linha, text="Desenhar Linha", command=desenhar_linha).pack(pady=10, fill="x")

# --- Frame para Controles do Modo Polilinha ---
frame_polilinha = ttk.LabelFrame(controls_frame, text="Controles da Polilinha")
tk.Label(frame_polilinha, text="Adicionar Ponto (x, y)").pack()
entry_px = tk.Entry(frame_polilinha, width=10); entry_px.pack()
entry_py = tk.Entry(frame_polilinha, width=10); entry_py.pack()
ttk.Button(frame_polilinha, text="Adicionar Ponto", command=add_point_from_entry).pack(pady=5, fill="x")
tk.Label(frame_polilinha, text="Pontos Adicionados:").pack(pady=(10,0))
texto_pontos = tk.Text(frame_polilinha, height=8, width=20)
texto_pontos.pack(pady=5)
texto_pontos.config(state=tk.DISABLED)
ttk.Button(frame_polilinha, text="Desenhar Polilinha", command=lambda: desenhar_polilinha(False)).pack(pady=5, fill="x")
ttk.Button(frame_polilinha, text="Fechar Polilinha", command=lambda: desenhar_polilinha(True)).pack(pady=5, fill="x")

# --- Botão de Limpar Global ---
ttk.Button(controls_frame, text="Limpar Tudo", command=limpar_tudo).pack(pady=20, fill="x", side="bottom")

# --- Início da Aplicação ---
switch_mode()
tela.iniciar()