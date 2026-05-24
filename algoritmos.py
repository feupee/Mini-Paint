def desenhar_linha_dda(canvas, ponto_inicial, ponto_final, cor, espessura=1):
    """
    Desenha uma linha usando o algoritmo DDA com uma espessura especificada.

    O algoritmo DDA calcula pontos intermediários entre dois pontos:
    ponto_inicial = (x1, y1)
    ponto_final = (x2, y2)

    Depois, ele pinta pixel por pixel no canvas. A espessura é aplicada desenhando um bloco de pixels ao redor de cada ponto calculado, criando uma linha mais grossa.
    """

    # Separa as coordenadas
    x1, y1 = ponto_inicial
    x2, y2 = ponto_final

    # Calcula a diferença entre os pontos no eixo X e Y
    dx = x2 - x1
    dy = y2 - y1

    # Define a quantidade de passos necessários para desenhar a linha
    # Usa o maior valor entre dx e dy para garantir que a linha fique contínua
    passos = max(abs(dx), abs(dy))
    
    # Calcula o raio de espessura para desenhar uma linha mais grossa
    raio = espessura // 2
    ajuste_par = espessura % 2

    # Caso especial: clique sem arrastar (desenha apenas o ponto/bloco inicial)
    if passos == 0:
        for i in range(-raio, raio + ajuste_par):
            for j in range(-raio, raio + ajuste_par):
                px = x1 + i
                py = y1 + j
                # Verifica se o ponto está dentro dos limites do canvas
                if 0 <= px < canvas.get_width() and 0 <= py < canvas.get_height():
                    # Desenha apenas um pixel
                    canvas.set_at((px, py), cor)
        return

    # Calcula quanto o X e Y devem avançar a cada passo
    incremento_x = dx / passos
    incremento_y = dy / passos

    # Começa o desenho no ponto inicial
    x = x1
    y = y1

    # Desenha a linha passo a passo (repete até chegar ao ponto final) e aplica o efeito de espessura
    for _ in range(passos + 1):
        # Arredonda os valores para encontrar o pixel mais próximo
        pixel_x = round(x)
        pixel_y = round(y)

        # Loops embutidos diretamente para criar o efeito de linha mais grossa
        for i in range(-raio, raio + ajuste_par):
            for j in range(-raio, raio + ajuste_par):
                px = pixel_x + i
                py = pixel_y + j
                # Verifica se o pixel está dentro dos limites do canvas
                # Verifica valores dentro do espaço dito de 800x600 sendo a ponta esquerda superior (0,0) e a ponta direita inferior (799, 599)
                if 0 <= px < canvas.get_width() and 0 <= py < canvas.get_height():
                    # Pinta o pixel no canvas
                    canvas.set_at((px, py), cor)

        # Avança para o próximo ponto da linha
        x += incremento_x
        y += incremento_y

def vizinhos_8conectado(canvas, ponto, cor_original):
    """
    Detecta os pixels 8-conectados ao redor do ponto especificado
    que possuem a mesma cor original do pixel clicado.

    Usa o DFS para detectar píxels conectados.
    """

    visitado = set()
    pilha = [ponto]

    largura = canvas.get_width()
    altura = canvas.get_height()

    # Pega a cor do píxel sem o nivel de intensidade
    cor_original = tuple(cor_original[:3])

    while pilha:
        x, y = pilha.pop()

        # Checa se o píxel está no canvas
        if not (0 <= x < largura and 0 <= y < altura):
            continue

        # Pula píxels já visitados
        if (x, y) in visitado:
            continue

        # Pega a cor atual do pixel
        cor_pixel = tuple(canvas.get_at((x, y))[:3])

        # Se a cor do pixel for diferente da cor original, não faz parte da região
        if cor_pixel != cor_original:
            continue

        visitado.add((x, y))

        vizinhos = [
            (x+1, y),     # direita
            (x-1, y),     # esquerda
            (x, y+1),     # baixo
            (x, y-1),     # cima
        ]
        """
            (x+1, y+1),   # diagonal inferior direita
            (x+1, y-1),   # diagonal superior direita
            (x-1, y+1),   # diagonal inferior esquerda
            (x-1, y-1)    # diagonal superior esquerda
        """

        for vx, vy in vizinhos:
            if (vx, vy) not in visitado:
                pilha.append((vx, vy))

    return visitado

def pinta_8conectado(canvas, visitado, cor):
    """
    Recebe o conjunto de píxels detectados pela função vizinhos_8conectado e pinta cada um deles com a cor especificada.
    """

    for x, y in visitado:
        canvas.set_at((x, y), cor)

def desenhar_quadrado(canvas, p1, p2, cor):
    x1, y1 = p1
    x2, y2 = p2
    # calculando os outros dois vértices
    p3 = (x1, y2)
    p4 = (x2, y1)
    # desenhando linhas entre os quatro pontos
    
    desenhar_linha_dda(canvas, p1, p3, cor)
    desenhar_linha_dda(canvas, p3, p2, cor)
    desenhar_linha_dda(canvas, p2, p4, cor)
    desenhar_linha_dda(canvas, p4, p1, cor)

# https://www.youtube.com/watch?v=hpiILbMkF9w
def desenhar_circulo(canvas, cx, cy, raio, cor):
    x = 0
    y = -raio
    p = -raio
    while x < -y:
        if p > 0:
            y += 1
            p += 2*(x+y) + 1
        else:
            p += 2*x + 1

        #plota os 8 lados do círculo
        canvas.set_at((cx + x, cy + y), cor)
        canvas.set_at((cx - x, cy + y), cor)
        canvas.set_at((cx + x, cy - y), cor)
        canvas.set_at((cx - x, cy - y), cor)
        canvas.set_at((cx + y, cy + x), cor)
        canvas.set_at((cx + y, cy - x), cor)
        canvas.set_at((cx - y, cy + x), cor)
        canvas.set_at((cx - y, cy - x), cor)
        x += 1


