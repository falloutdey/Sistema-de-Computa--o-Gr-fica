# grid.py
import tkinter as tk
import math

class Grid:
  def __init__(self, master_frame, redraw_callback=None):
    self.master = master_frame
    self.redraw_callback = redraw_callback
    self.matriz = []
    self.tamanho_matriz = 50
    self.meio_matriz = self.tamanho_matriz / 2
    self.cor_borda = '#000000'

    self.tela = tk.Canvas(self.master, bg="white", highlightthickness=0)
    self.tela.pack(fill=tk.BOTH, expand=True)

    self.tela.bind("<Configure>", self.on_resize)

    self.tamanho_tela = 0
    self.tamanho_pixel = 0

  def on_resize(self, event):
      novo_tamanho = min(event.width, event.height)
      if abs(self.tamanho_tela - novo_tamanho) < 2:
          return 
      
      self.tamanho_tela = novo_tamanho
      self.tamanho_pixel = self.tamanho_tela / self.tamanho_matriz
      
      self.tela.config(width=self.tamanho_tela, height=self.tamanho_tela)
      self.limpar_tela()

      if self.redraw_callback:
          self.redraw_callback()

  def CriarTemplate(self):
    if self.tamanho_tela == 0: return
    centro = self.tamanho_tela / 2
    pixel_size = int(self.tamanho_pixel) if self.tamanho_pixel > 0 else 1
    
    for i in range(0, int(self.tamanho_tela) + 1, pixel_size):
      self.tela.create_line(i, 0, i, self.tamanho_tela, fill='#DCDCDC')
      self.tela.create_line(0, i, self.tamanho_tela, i, fill='#DCDCDC')
      
    self.tela.create_line(0, centro, self.tamanho_tela, centro, fill="#f00")
    self.tela.create_line(centro, 0, centro, self.tamanho_tela, fill="#f00")

  def converter_coordenadas(self, x, y):
    real_x = (self.tamanho_pixel * x) + (self.tamanho_tela / 2)
    real_y = (self.tamanho_tela / 2) - (self.tamanho_pixel * y)
    return real_x, real_y

  def converter_para_coordenadas_grid(self, event_x, event_y):
    if self.tamanho_pixel == 0: return 0, 0
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
    if not self.esta_dentro_dos_limites(x, y) or self.tamanho_pixel == 0: return
    x1, y1 = self.converter_coordenadas(x, y)
    x2, y2 = x1 + self.tamanho_pixel, y1 - self.tamanho_pixel
    self.tela.create_rectangle(x1, y1, x2, y2, fill=cor, outline=cor)
    l, c = self.converter_coordenadas_matriz(x, y)
    if 0 <= l < self.tamanho_matriz and 0 <= c < self.tamanho_matriz:
        self.matriz[l][c] = cor
    
  def checar_matriz(self, x, y):
    if not self.esta_dentro_dos_limites(x, y): return self.cor_borda
    l, c = self.converter_coordenadas_matriz(x, y)
    if 0 <= l < self.tamanho_matriz and 0 <= c < self.tamanho_matriz:
        return self.matriz[l][c]
    return 0

  def desenhar(self, objeto: list, cor):
    for p in objeto:
      self.desenhar_pixel(p[0], p[1], cor)

  def desenhar_marcador_temporario(self, x, y, cor):
      if not self.esta_dentro_dos_limites(x, y): return
      x1, y1 = self.converter_coordenadas(x, y)
      self.tela.create_oval(x1 + 2, y1 - 2, x1 + self.tamanho_pixel - 2, y1 - self.tamanho_pixel + 2, fill=cor, outline="", tags="marcador")

  def limpar_marcadores(self):
      self.tela.delete("marcador")

  def destacar_janela(self, xmin, ymin, xmax, ymax):
    x1_tela, y1_tela = self.converter_coordenadas(xmin, ymax)
    x2_tela, y2_tela = self.converter_coordenadas(xmax, ymin)
    self.tela.create_rectangle(x1_tela, y1_tela, x2_tela, y2_tela, outline='red', width=2)

  def limpar_tela(self):
    self.tela.delete("all")
    self.matriz = [[0 for _ in range(self.tamanho_matriz)] for _ in range(self.tamanho_matriz)]
    self.CriarTemplate()