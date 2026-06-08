
def cor_para_inteiro(cor):
    """
    Converte uma cor RGB para inteiro no formato 0xRRGGBB.
    """

    r, g, b = cor[:3]

    return (r << 16) + (g << 8) + b


def inteiro_para_cor(valor):
    """
    Converte um inteiro 0xRRGGBB para uma cor RGB.
    """

    r = (valor >> 16) & 255
    g = (valor >> 8) & 255
    b = valor & 255

    return (r, g, b)


def criar_matriz_inteiros(largura, altura, cor_fundo):
    """
    Cria a matriz principal do canvas.
    """

    cor_inteira = cor_para_inteiro(cor_fundo)

    matriz = []

    for y in range(altura):
        linha = []

        for x in range(largura):
            linha.append(cor_inteira)

        matriz.append(linha)

    return matriz


def obter_largura(matriz):
    """
    Retorna a largura da matriz.
    """

    if len(matriz) == 0:
        return 0

    return len(matriz[0])


def obter_altura(matriz):
    """
    Retorna a altura da matriz.
    """

    return len(matriz)


def ponto_dentro_matriz(matriz, x, y):
    """
    Verifica se o ponto está dentro dos limites da matriz.
    """

    return 0 <= x < obter_largura(matriz) and 0 <= y < obter_altura(matriz)


def put_pixel(matriz, x, y, cor, canvas_visual=None):
    """
    Pinta um pixel na matriz de inteiros.

    Essa é a função equivalente a:

        put_pixel(x, y, cor)

    Se `canvas_visual` for informado, a Surface do Pygame também é atualizada
    naquele pixel. Isso evita converter a matriz inteira para Surface a cada
    frame e melhora o desempenho.
    """

    if not ponto_dentro_matriz(matriz, x, y):
        return

    cor_rgb = tuple(cor[:3])
    matriz[y][x] = cor_para_inteiro(cor_rgb)

    if canvas_visual is not None:
        # Atualização visual pontual. Não é o algoritmo que depende do Pygame;
        # é apenas o cache visual sendo sincronizado com a matriz.
        canvas_visual.fill(cor_rgb, (x, y, 1, 1))


def get_pixel(matriz, x, y):
    """
    Retorna a cor RGB de um pixel da matriz.
    """

    if not ponto_dentro_matriz(matriz, x, y):
        return None

    return inteiro_para_cor(matriz[y][x])


def plotar_ponto_seguro(matriz, x, y, cor, canvas_visual=None):
    """
    Pinta um ponto se ele estiver dentro dos limites do canvas.
    """

    put_pixel(matriz, x, y, cor, canvas_visual)


def plotar_ponto_espesso(matriz, x, y, cor, espessura, canvas_visual=None):
    """
    Em vez de pintar apenas um único pixel, pinta vários pixels ao redor da
    posição central.

    Essa função é usada para engrossar linhas e contornos.
    """

    raio = espessura // 2
    ajuste_par = espessura % 2

    for dx in range(-raio, raio + ajuste_par):
        for dy in range(-raio, raio + ajuste_par):
            plotar_ponto_seguro(matriz, x + dx, y + dy, cor, canvas_visual)


def desenhar_linha_dda(matriz, ponto_inicial, ponto_final, cor, espessura=1, canvas_visual=None):
    """
    Desenha uma linha usando o algoritmo DDA com uma espessura especificada.

    O algoritmo DDA calcula pontos intermediários entre dois pontos:
    ponto_inicial = (x1, y1)
    ponto_final = (x2, y2)

    Depois, ele pinta pixel por pixel na matriz. A espessura é aplicada
    desenhando um bloco de pixels ao redor de cada ponto calculado.
    """

    x1, y1 = ponto_inicial
    x2, y2 = ponto_final

    dx = x2 - x1
    dy = y2 - y1

    passos = max(abs(dx), abs(dy))

    if passos == 0:
        plotar_ponto_espesso(matriz, x1, y1, cor, espessura, canvas_visual)
        return

    incremento_x = dx / passos
    incremento_y = dy / passos

    x = x1
    y = y1

    for _ in range(passos + 1):
        pixel_x = round(x)
        pixel_y = round(y)

        plotar_ponto_espesso(
            matriz,
            pixel_x,
            pixel_y,
            cor,
            espessura,
            canvas_visual
        )

        x += incremento_x
        y += incremento_y


def vizinhos_8conectado(matriz, ponto, cor_original):
    """
    Detecta pixels conectados ao ponto especificado que possuem a mesma cor
    original do pixel clicado.

    A implementação usa pilha para evitar recursão profunda.
    """

    visitado = set()
    pilha = [ponto]

    largura = obter_largura(matriz)
    altura = obter_altura(matriz)

    if cor_original is None:
        return visitado

    cor_original = tuple(cor_original[:3])

    while pilha:
        x, y = pilha.pop()

        if not (0 <= x < largura and 0 <= y < altura):
            continue

        if (x, y) in visitado:
            continue

        cor_pixel = get_pixel(matriz, x, y)

        if cor_pixel != cor_original:
            continue

        visitado.add((x, y))

        vizinhos = [
            (x + 1, y),     # direita
            (x - 1, y),     # esquerda
            (x, y + 1),     # baixo
            (x, y - 1),     # cima
        ]

        for vx, vy in vizinhos:
            if (vx, vy) not in visitado:
                pilha.append((vx, vy))

    return visitado


def pinta_8conectado(matriz, visitado, cor, canvas_visual=None):
    """
    Recebe o conjunto de pixels detectados pela função vizinhos_8conectado e
    pinta cada um deles com a cor especificada.
    """

    for x, y in visitado:
        put_pixel(matriz, x, y, cor, canvas_visual)


def desenhar_retangulo(matriz, p1, p2, cor, espessura=1, canvas_visual=None):
    """
    Desenha um retângulo usando linhas DDA entre os quatro vértices.
    """

    x1, y1 = p1
    x2, y2 = p2

    p3 = (x1, y2)
    p4 = (x2, y1)

    desenhar_linha_dda(matriz, p1, p3, cor, espessura, canvas_visual)
    desenhar_linha_dda(matriz, p3, p2, cor, espessura, canvas_visual)
    desenhar_linha_dda(matriz, p2, p4, cor, espessura, canvas_visual)
    desenhar_linha_dda(matriz, p4, p1, cor, espessura, canvas_visual)


# https://www.youtube.com/watch?v=hpiILbMkF9w
def desenhar_circulo(matriz, cx, cy, raio, cor, espessura=1, canvas_visual=None):
    """
    Desenha o contorno de um círculo usando o algoritmo do ponto médio.

    Para cada ponto calculado pelo algoritmo, são desenhados outros sete pontos
    simétricos em relação ao centro. Dessa forma, o círculo completo é formado
    sem precisar calcular todos os seus pontos individualmente.
    """

    if raio < 0:
        raio = abs(raio)

    x = 0
    y = -raio
    p = -raio

    while x < -y:
        if p > 0:
            y += 1 
            p += 2 * (x + y) + 1
        else:
            p += 2 * x + 1

        plotar_ponto_espesso(matriz, cx + x, cy + y, cor, espessura, canvas_visual)
        plotar_ponto_espesso(matriz, cx - x, cy + y, cor, espessura, canvas_visual)
        plotar_ponto_espesso(matriz, cx + x, cy - y, cor, espessura, canvas_visual)
        plotar_ponto_espesso(matriz, cx - x, cy - y, cor, espessura, canvas_visual)

        plotar_ponto_espesso(matriz, cx + y, cy + x, cor, espessura, canvas_visual)
        plotar_ponto_espesso(matriz, cx + y, cy - x, cor, espessura, canvas_visual)
        plotar_ponto_espesso(matriz, cx - y, cy + x, cor, espessura, canvas_visual)
        plotar_ponto_espesso(matriz, cx - y, cy - x, cor, espessura, canvas_visual)

        x += 1


def desenhar_retangulo_preenchido(matriz, p1, p2, cor, espessura=1, canvas_visual=None):
    """
    Desenha um retângulo preenchido pintando todos os pixels entre o ponto
    inicial e o ponto final.
    """

    x1, y1 = p1
    x2, y2 = p2

    inicio_x = min(x1, x2)
    fim_x = max(x1, x2)
    inicio_y = min(y1, y2)
    fim_y = max(y1, y2)

    for y in range(inicio_y, fim_y + 1):
        for x in range(inicio_x, fim_x + 1):
            put_pixel(matriz, x, y, cor, canvas_visual)


def desenhar_circulo_preenchido(matriz, cx, cy, raio, cor, espessura = 3, canvas_visual=None):
    """
    Desenha um círculo preenchido usando varredura sobre a matriz de inteiros.

    A função percorre a área quadrada que envolve o círculo e pinta somente os
    pixels que satisfazem a equação:

        (x - cx)² + (y - cy)² <= raio²

    Depois, desenha a borda usando o algoritmo de círculo já implementado.

    A matriz é atualizada por put_pixel. Para manter o desempenho na versão
    híbrida, a Surface visual é preenchida com pygame.draw.circle uma única vez,
    evitando milhares de atualizações individuais na interface.
    """

    if raio < 0:
        raio = abs(raio)

    largura = obter_largura(matriz)
    altura = obter_altura(matriz)
    raio_quadrado = raio ** 2

    inicio_x = max(0, cx - raio)
    fim_x = min(largura - 1, cx + raio)
    inicio_y = max(0, cy - raio)
    fim_y = min(altura - 1, cy + raio)

    for y in range(inicio_y, fim_y + 1):
        for x in range(inicio_x, fim_x + 1):
            if (x - cx) ** 2 + (y - cy) ** 2 <= raio_quadrado:
                put_pixel(matriz, x, y, cor)

    if canvas_visual is not None:
        import pygame

        pygame.draw.circle(
            canvas_visual,
            cor,
            (cx, cy),
            raio,
            0
        )

    if espessura > 0:
        desenhar_circulo(
            matriz,
            cx,
            cy,
            raio,
            cor,
            espessura,
            canvas_visual
        )

