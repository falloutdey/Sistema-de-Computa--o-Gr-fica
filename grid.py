# grid.py
import tkinter as tk
import math

class Grid:
  # ... (O resto do código da classe Grid permanece o mesmo)
  def __init__(self, tamanho_tela, tamanho_matriz=50):
    self.tamanho_tela = tamanho_tela
    self.matriz = []
    self.tamanho_matriz = tamanho_matriz
    self.meio_matriz = tamanho_matriz / 2
    self.tamanho_pixel = int(self.tamanho_tela / self.tamanho_matriz)
    self.cor_borda = '#000000'

    for i in range(self.tamanho_matriz):
        linha = [0] * self.tamanho_matriz
        self.matriz.append(linha)

    self.master = tk.Tk()
    self.master.title("Sistema de Computação Gráfica")
    self.tela = tk.Canvas(self.master, width=self.tamanho_tela, height=self.tamanho_tela, bg="white")
    self.CriarTemplate()

  def CriarTemplate(self):
    centro = int(self.tamanho_tela / 2)
    for x in range(0, self.tamanho_tela, self.tamanho_pixel):
      self.tela.create_line(x, 0, x, self.tamanho_tela, fill='#DCDCDC')
    for y in range(0, self.tamanho_tela, self.tamanho_pixel):
      self.tela.create_line(0, y, self.tamanho_tela, y, fill='#DCDCDC')
    self.tela.create_line(0, centro, self.tamanho_tela, centro, fill="#f00")
    self.tela.create_line(centro, 0, centro, self.tamanho_tela, fill="#f00")

  def converter_coordenadas(self, x, y):
    real_x = int((self.tamanho_pixel * x) + (self.tamanho_tela / 2))
    real_y = int((self.tamanho_tela / 2) - (self.tamanho_pixel * y))
    return real_x, real_y

  def converter_para_coordenadas_grid(self, event_x, event_y):
    centro = self.tamanho_tela / 2
    grid_x = math.floor((event_x - centro + (self.tamanho_pixel / 2)) / self.tamanho_pixel)
    grid_y = math.floor((centro - event_y + (self.tamanho_pixel / 2)) / self.tamanho_pixel)
    return int(grid_x), int(grid_y)
    
  def converter_coordenadas_matriz(self, x, y):
    coluna = int(x + self.meio_matriz)
    linha = int(self.meio_matriz - y - 1)
    return linha, coluna

  def esta_dentro_dos_limites(self, x, y):
    return -self.meio_matriz <= x < self.meio_matriz and -self.meio_matriz <= y < self.meio_matriz

  def desenhar_pixel(self, x, y, cor):
    if not self.esta_dentro_dos_limites(x, y): return
    x1, y1 = self.converter_coordenadas(x, y)
    x2, y2 = x1 + self.tamanho_pixel, y1 - self.tamanho_pixel
    self.tela.create_rectangle(x1, y1, x2, y2, fill=cor, outline=cor)
    l, c = self.converter_coordenadas_matriz(x, y)
    self.matriz[l][c] = cor
    
  def checar_matriz(self, x, y):
    if not self.esta_dentro_dos_limites(x, y): return self.cor_borda
    l, c = self.converter_coordenadas_matriz(x, y)
    return self.matriz[l][c]

  def desenhar(self, objeto: list, cor):
    for p in objeto:
      self.desenhar_pixel(p[0], p[1], cor)

  def desenhar_marcador_temporario(self, x, y, cor):
      if not self.esta_dentro_dos_limites(x, y): return
      x1, y1 = self.converter_coordenadas(x, y)
      self.tela.create_oval(x1 + 2, y1 - 2, x1 + self.tamanho_pixel - 2, y1 - self.tamanho_pixel + 2, fill=cor, outline="", tags="marcador")

  def limpar_marcadores(self):
      self.tela.delete("marcador")

  # --- NOVA FUNÇÃO ---
  def destacar_janela(self, xmin, ymin, xmax, ymax):
    """Desenha um retângulo vermelho para visualizar a janela de recorte."""
    # Converte as coordenadas da malha para coordenadas de pixel na tela
    x1_tela, y1_tela = self.converter_coordenadas(xmin, ymax)
    x2_tela, y2_tela = self.converter_coordenadas(xmax, ymin)
    
    # Desenha o retângulo (outline) sem preenchimento
    self.tela.create_rectangle(x1_tela, y1_tela, x2_tela, y2_tela, outline='red', width=2)


  def limpar_tela(self):
    self.tela.delete("all")
    self.matriz = [[0 for _ in range(self.tamanho_matriz)] for _ in range(self.tamanho_matriz)]
    self.CriarTemplate()

  def iniciar(self):
    self.master.mainloop()