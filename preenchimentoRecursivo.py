# preenchimento_recursivo.py
class PreenchimentoRecursivo:
  """
  Executa o algoritmo de preenchimento (Flood Fill) de forma iterativa,
  usando uma pilha para evitar o estouro de recursão.
  """
  def __init__(self, ponto_inicial, cor_preenchimento, tela):
    self.tela = tela
    self.cor_preenchimento = cor_preenchimento
    self.cor_borda = '#000000'
    
    # Obtém a cor original do ponto clicado para saber o que substituir.
    self.cor_alvo = self.tela.checar_matriz(ponto_inicial[0], ponto_inicial[1])

    # Inicia o processo de preenchimento iterativo
    self.preencher_iterativo(ponto_inicial)

  def preencher_iterativo(self, ponto_inicial):
    # Condição inicial: não faz nada se a cor alvo for a cor da borda
    # ou se já for a cor de preenchimento.
    if self.cor_alvo == self.cor_borda or self.cor_alvo == self.cor_preenchimento:
      return

    pilha = [ponto_inicial]

    while pilha:
      x, y = pilha.pop()
      cor_atual = self.tela.checar_matriz(x, y)

      if cor_atual == self.cor_alvo:
        self.tela.desenhar_pixel(x, y, self.cor_preenchimento)

        # Adiciona os 4 vizinhos à pilha para serem verificados.
        pilha.append((x + 1, y))
        pilha.append((x - 1, y))
        pilha.append((x, y + 1))
        pilha.append((x, y - 1))