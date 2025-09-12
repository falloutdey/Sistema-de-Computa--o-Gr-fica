# grid.py
import tkinter as tk
import math

class Grid:
  """
  Gerencia a criação e manipulação da grade de desenho (Canvas) da aplicação.
  Esta classe é responsável por desenhar a grade, os eixos, converter coordenadas
  e desenhar pixels na tela.
  """
  def __init__(self, master, tamanho_tela, tamanho_matriz=50):
    """
    Inicializa a grade de desenho.

    Args:
        master (tk.Tk): A janela principal (root) da aplicação.
        tamanho_tela (int): A largura e altura da área de desenho em pixels.
        tamanho_matriz (int): A dimensão da matriz que representa a grade (ex: 50x50).
    """
    self.master = master
    self.tamanho_tela = tamanho_tela
    self.tamanho_matriz = tamanho_matriz
    self.meio_matriz = tamanho_matriz / 2
    self.tamanho_pixel = int(self.tamanho_tela / self.tamanho_matriz)
    self.cor_borda = '#000000'

    # Cria uma matriz 2D para armazenar as cores dos pixels,
    # útil para algoritmos de preenchimento.
    self.matriz = [[0] * self.tamanho_matriz for _ in range(self.tamanho_matriz)]
    
    self.master.resizable(width=False, height=False)
    
    # Cria o widget Canvas do Tkinter, que é a área de desenho.
    self.tela = tk.Canvas(self.master, width=self.tamanho_tela, height=self.tamanho_tela, bg="white")
    self.CriarTemplate()

  def CriarTemplate(self):
    """
    Desenha a grade quadriculada e os eixos cartesianos (x e y) na tela.
    """
    centro = int(self.tamanho_tela / 2)
    # Desenha as linhas verticais da grade.
    for x in range(0, self.tamanho_tela, self.tamanho_pixel):
      self.tela.create_line(x, 0, x, self.tamanho_tela, fill='#DCDCDC')
    # Desenha as linhas horizontais da grade.
    for y in range(0, self.tamanho_tela, self.tamanho_pixel):
      self.tela.create_line(0, y, self.tamanho_tela, y, fill='#DCDCDC')
    # Desenha os eixos principais em vermelho.
    self.tela.create_line(0, centro, self.tamanho_tela, centro, fill="#f00") # Eixo X
    self.tela.create_line(centro, 0, centro, self.tamanho_tela, fill="#f00") # Eixo Y

  def converter_coordenadas(self, x, y):
    """
    Converte coordenadas da grade (ex: -25 a 25) para coordenadas 
    do canvas do Tkinter (ex: 0 a 550).

    Args:
        x (int): A coordenada x na grade.
        y (int): A coordenada y na grade.

    Returns:
        tuple: As coordenadas (real_x, real_y) correspondentes no canvas.
    """
    real_x = int((self.tamanho_pixel * x) + (self.tamanho_tela / 2))
    real_y = int((self.tamanho_tela / 2) - (self.tamanho_pixel * y))
    return real_x, real_y

  def converter_para_coordenadas_grid(self, event_x, event_y):
    """
    Converte as coordenadas de um evento de clique do mouse (em pixels do canvas)
    para as coordenadas da grade.

    Args:
        event_x (int): A coordenada x do evento de clique.
        event_y (int): A coordenada y do evento de clique.

    Returns:
        tuple: As coordenadas (grid_x, grid_y) na grade.
    """
    centro = self.tamanho_tela / 2
    grid_x = math.floor((event_x - centro + (self.tamanho_pixel / 2)) / self.tamanho_pixel)
    grid_y = math.floor((centro - event_y + (self.tamanho_pixel / 2)) / self.tamanho_pixel)
    return int(grid_x), int(grid_y)
    
  def converter_coordenadas_matriz(self, x, y):
    """
    Converte coordenadas da grade para índices da matriz interna.

    Args:
        x (int): A coordenada x na grade.
        y (int): A coordenada y na grade.

    Returns:
        tuple: Os índices (linha, coluna) na matriz.
    """
    coluna = int(x + self.meio_matriz)
    linha = int(self.meio_matriz - y - 1)
    return linha, coluna

  def esta_dentro_dos_limites(self, x, y):
    """
    Verifica se uma coordenada da grade está dentro dos limites visíveis.

    Args:
        x (int): Coordenada x.
        y (int): Coordenada y.

    Returns:
        bool: True se estiver dentro dos limites, False caso contrário.
    """
    return -self.meio_matriz <= x < self.meio_matriz and -self.meio_matriz <= y < self.meio_matriz

  def desenhar_pixel(self, x, y, cor):
    """
    Desenha um 'pixel' (um retângulo) na grade e atualiza a matriz de cores.

    Args:
        x (int): A coordenada x do pixel na grade.
        y (int): A coordenada y do pixel na grade.
        cor (str): A cor do pixel em formato hexadecimal.
    """
    if not self.esta_dentro_dos_limites(x, y): return
    x1, y1 = self.converter_coordenadas(x, y)
    x2, y2 = x1 + self.tamanho_pixel, y1 - self.tamanho_pixel
    self.tela.create_rectangle(x1, y1, x2, y2, fill=cor, outline=cor)
    l, c = self.converter_coordenadas_matriz(x, y)
    self.matriz[l][c] = cor
    
  def checar_matriz(self, x, y):
    """
    Retorna a cor de um pixel específico na matriz interna.

    Args:
        x (int): A coordenada x do pixel na grade.
        y (int): A coordenada y do pixel na grade.

    Returns:
        str: A cor do pixel ou a cor da borda se estiver fora dos limites.
    """
    if not self.esta_dentro_dos_limites(x, y): return self.cor_borda
    l, c = self.converter_coordenadas_matriz(x, y)
    return self.matriz[l][c]

  def desenhar(self, objeto: list, cor):
    """
    Desenha uma lista de pontos na tela com uma cor específica.

    Args:
        objeto (list): Uma lista de pontos [x, y] a serem desenhados.
        cor (str): A cor para desenhar os pontos.
    """
    for p in objeto:
      self.desenhar_pixel(p[0], p[1], cor)

  def desenhar_marcador_temporario(self, x, y, cor):
      """
      Desenha um marcador oval temporário na tela, útil para indicar pontos de semente.

      Args:
          x (int): Coordenada x na grade.
          y (int): Coordenada y na grade.
          cor (str): Cor do marcador.
      """
      if not self.esta_dentro_dos_limites(x, y): return
      x1, y1 = self.converter_coordenadas(x, y)
      self.tela.create_oval(x1 + 2, y1 - 2, x1 + self.tamanho_pixel - 2, y1 - self.tamanho_pixel + 2, fill=cor, outline="", tags="marcador")

  def limpar_marcadores(self):
      """
      Remove todos os marcadores temporários da tela.
      """
      self.tela.delete("marcador")

  def destacar_janela(self, xmin, ymin, xmax, ymax):
    """
    Desenha um retângulo vermelho para destacar a janela de recorte.

    Args:
        xmin, ymin, xmax, ymax (int): Coordenadas da janela de recorte.
    """
    x1_tela, y1_tela = self.converter_coordenadas(xmin, ymax)
    x2_tela, y2_tela = self.converter_coordenadas(xmax, ymin)
    self.tela.create_rectangle(x1_tela, y1_tela, x2_tela, y2_tela, outline='red', width=2)

  def limpar_tela(self):
    """
    Limpa completamente o canvas e reinicializa a matriz de cores.
    """
    self.tela.delete("all")
    self.matriz = [[0 for _ in range(self.tamanho_matriz)] for _ in range(self.tamanho_matriz)]
    self.CriarTemplate()