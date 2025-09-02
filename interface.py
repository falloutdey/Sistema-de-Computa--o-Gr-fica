import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from Sistemas.bresenham import criar_malha

# Configuração inicial da malha
linhas_iniciais = 15
colunas_iniciais = 15
malha_inicial = np.ones((linhas_iniciais, colunas_iniciais))  # fundo branco

def desenhar():
    try:
        x0 = int(entry_x0.get())
        y0 = int(entry_y0.get())
        x1 = int(entry_x1.get())
        y1 = int(entry_y1.get())
        linhas = int(entry_linhas.get())
        colunas = int(entry_colunas.get())
    except ValueError:
        return

    tela = criar_malha(x0, y0, x1, y1, linhas, colunas)
    atualizar_canvas(tela)

def atualizar_canvas(tela):
    ax.clear()
    # cmap='gray_r' faz o fundo branco e pixels pretos
    ax.imshow(tela, cmap='gray_r', origin='lower')

    # Grade de pixels
    linhas, colunas = tela.shape
    for i in range(linhas + 1):
        ax.axhline(i - 0.5, color='black', linewidth=0.5)
    for j in range(colunas + 1):
        ax.axvline(j - 0.5, color='black', linewidth=0.5)

    ax.set_xticks([])
    ax.set_yticks([])
    canvas.draw()

# --- Janela Tkinter ---
root = tk.Tk()
root.title("Malha de Pixels")

# Área de desenho
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=0, column=0, rowspan=10)

# Entradas
tk.Label(root, text="x0").grid(row=0, column=1)
entry_x0 = tk.Entry(root); entry_x0.grid(row=0, column=2)

tk.Label(root, text="y0").grid(row=1, column=1)
entry_y0 = tk.Entry(root); entry_y0.grid(row=1, column=2)

tk.Label(root, text="x1").grid(row=2, column=1)
entry_x1 = tk.Entry(root); entry_x1.grid(row=2, column=2)

tk.Label(root, text="y1").grid(row=3, column=1)
entry_y1 = tk.Entry(root); entry_y1.grid(row=3, column=2)

tk.Label(root, text="Linhas").grid(row=4, column=1)
entry_linhas = tk.Entry(root); entry_linhas.grid(row=4, column=2)
entry_linhas.insert(0, str(linhas_iniciais))

tk.Label(root, text="Colunas").grid(row=5, column=1)
entry_colunas = tk.Entry(root); entry_colunas.grid(row=5, column=2)
entry_colunas.insert(0, str(colunas_iniciais))

# Botão
btn = tk.Button(root, text="Desenhar", command=desenhar)
btn.grid(row=6, column=1, columnspan=2, sticky="we")

# Malha inicial vazia já exibida
atualizar_canvas(malha_inicial)

root.mainloop()