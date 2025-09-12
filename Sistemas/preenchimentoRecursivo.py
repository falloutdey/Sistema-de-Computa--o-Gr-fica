# Sistemas/preenchimentoRecursivo.py
class PreenchimentoRecursivo:
  """
  Executa o algoritmo de preenchimento (Flood Fill) de forma iterativa,
  usando uma pilha (LIFO) para evitar o estouro de recursão que ocorreria
  com uma abordagem puramente recursiva em áreas grandes.
  """
  def __init__(self, ponto_inicial, cor_preenchimento, tela):
    """
    Inicializa o processo de preenchimento.

    Args:
        ponto_inicial (tuple): As coordenadas (x, y) do ponto de semente.
        cor_preenchimento (str): A cor no formato hexadecimal (ex: '#FF0000') para preencher a área.
        tela (Grid): A instância da classe Grid que gerencia a tela de desenho.
    """
    self.tela = tela
    self.cor_preenchimento = cor_preenchimento
    self.cor_borda = '#000000'
    
    # Obtém a cor original do ponto clicado para saber qual cor deve ser substituída.
    self.cor_alvo = self.tela.checar_matriz(ponto_inicial[0], ponto_inicial[1])

    # Inicia o processo de preenchimento iterativo a partir do ponto inicial.
    self.preencher_iterativo(ponto_inicial)

  def preencher_iterativo(self, ponto_inicial):
    """
    Executa o algoritmo Flood Fill usando uma pilha.

    Args:
        ponto_inicial (tuple): O ponto (x, y) a partir do qual o preenchimento começa.
    """
    # Condição inicial: não faz nada se a cor alvo for a cor da borda
    # ou se já for a cor de preenchimento (evita loops infinitos).
    if self.cor_alvo == self.cor_borda or self.cor_alvo == self.cor_preenchimento:
      return

    pilha = [ponto_inicial]

    while pilha:
      x, y = pilha.pop()
      cor_atual = self.tela.checar_matriz(x, y)

      # Se o pixel atual tem a cor alvo, pinta-o e adiciona seus vizinhos à pilha.
      if cor_atual == self.cor_alvo:
        self.tela.desenhar_pixel(x, y, self.cor_preenchimento)

        # Adiciona os 4 vizinhos (direita, esquerda, cima, baixo) à pilha para verificação.
        pilha.append((x + 1, y))
        pilha.append((x - 1, y))
        pilha.append((x, y + 1))
        pilha.append((x, y - 1))