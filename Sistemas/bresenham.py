import numpy as np

def bresenham(x0, y0, x1, y1):
    pontos = []
    deltax = abs(x1 - x0)
    deltay = abs(y1 - y0)
    sx = 1 if x1 > x0 else -1
    sy = 1 if y1 > y0 else -1
    x, y = x0, y0

    if deltax > deltay:
        e = 2 * deltay - deltax
        for _ in range(deltax + 1):
            pontos.append((x, y))
            if e >= 0:
                y += sy
                e -= 2 * deltax
            x += sx
            e += 2 * deltay
    else:
        e = 2 * deltax - deltay
        for _ in range(deltay + 1):
            pontos.append((x, y))
            if e >= 0:
                x += sx
                e -= 2 * deltay
            y += sy
            e += 2 * deltax
    return pontos

def criar_malha(x0, y0, x1, y1, linhas=15, colunas=15):
    tela = np.ones((linhas, colunas))
    pontos = bresenham(x0, y0, x1, y1)
    for x, y in pontos:
        if 0 <= x < colunas and 0 <= y < linhas:
            tela[y, x] = 0
    return tela
