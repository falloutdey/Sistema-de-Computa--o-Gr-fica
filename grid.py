# grid.py
from tkinter import *
import math # Importa a biblioteca de matemática

class Grid:
  def __init__(self, tamanho_tela, tamanho_matriz=50):
    self.tamanho_tela = tamanho_tela
    self.matriz = []
    self.tamanho_matriz = tamanho_matriz
    self.tamanho_pixel = int(self.tamanho_tela / self.tamanho_matriz)

    for i in range(self.tamanho_matriz):
        linha = []
        for j in range(self.tamanho_matriz):
          linha.append(0)
        self.matriz.append(linha)

    self.master = Tk()
    self.master.title("Sistema de Computação Gráfica")
    self.tela = Canvas(self.master,
                       width=self.tamanho_tela,
                       height=self.tamanho_tela,
                       bg="white")
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

  # >>> FUNÇÃO CORRIGIDA AQUI <<<
  def converter_para_coordenadas_grid(self, event_x, event_y):
      """Converte coordenadas do clique (em pixels) para as coordenadas da malha com precisão."""
      centro = self.tamanho_tela / 2
      
      # Usamos math.floor para garantir que a coordenada caia dentro da célula correta,
      # em vez de arredondar para a mais próxima.
      grid_x = math.floor((event_x - centro) / self.tamanho_pixel)
      grid_y = math.floor((centro - event_y) / self.tamanho_pixel)
      
      # Precisamos de um pequeno ajuste para o eixo Y devido à inversão de coordenadas.
      # Se o clique for exatamente na linha do eixo X, ele pode ficar deslocado.
      if event_y >= centro:
          grid_y = math.ceil((centro - event_y) / self.tamanho_pixel)

      return int(grid_x), int(grid_y)

  def converter_coordenadas_matriz(self, x, y):
    coluna = int(x + (self.tamanho_matriz / 2))
    linha = int((self.tamanho_matriz / 2) - y) - 1
    return linha, coluna

  def desenhar_pixel(self, x, y, cor):
    x1, y1 = self.converter_coordenadas(x, y)
    x2, y2 = x1 + self.tamanho_pixel, y1 - self.tamanho_pixel
    self.tela.create_rectangle(x1, y1, x2, y2, fill=cor, outline=cor)

    l, c = self.converter_coordenadas_matriz(x, y)
    if 0 <= l < self.tamanho_matriz and 0 <= c < self.tamanho_matriz:
        self.matriz[l][c] = cor

  def desenhar(self, objeto: list, cor):
    for p in objeto:
      self.desenhar_pixel(p[0], p[1], cor)

  def limpar_tela(self):
      self.tela.delete("all")
      self.CriarTemplate()

  def iniciar(self):
    self.master.mainloop()