def desenhar_linha_dda(canvas, ponto_inicial, ponto_final, cor, espessura):
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

def balde_de_tinta(canvas, ponto, cor_atual, cor_nova):
    if cor_atual != cor_nova:
        visitado = vizinhos_8conectado(canvas, ponto, cor_atual)
        pinta_8conectado(canvas, visitado, cor_nova)

def desenhar_retangulo(canvas, p1, p2, cor, espessura):
    x1, y1 = p1
    x2, y2 = p2
    # calculando os outros dois vértices
    p3 = (x1, y2)
    p4 = (x2, y1)
    # desenhando linhas entre os quatro pontos
    
    desenhar_linha_dda(canvas, p1, p3, cor, espessura)
    desenhar_linha_dda(canvas, p3, p2, cor, espessura)
    desenhar_linha_dda(canvas, p2, p4, cor, espessura)
    desenhar_linha_dda(canvas, p4, p1, cor, espessura)

# https://www.youtube.com/watch?v=hpiILbMkF9w
def desenhar_circulo(canvas, cx, cy, raio, cor, espessura=1):
    """
    Funcionamento:
        Para cada ponto calculado pelo algoritmo, são desenhados outros
        sete pontos simétricos em relação ao centro. Dessa forma, o círculo
        completo é formado sem precisar calcular todos os seus pontos
        individualmente.

        A espessura é aplicada por meio da função plotar_ponto_espesso.
        Em vez de desenhar apenas um pixel em cada posição da borda,
        a função desenha uma pequena área ao redor de cada ponto.

    Observação:
        Esta função desenha apenas o contorno do círculo.
        O preenchimento do círculo deve ser tratado separadamente ou por
        uma versão da função que receba um parâmetro como preenchido=True.

    """

    # Começa calculando o círculo a partir do ponto superior.
    # x começa em 0 e y começa negativo porque o algoritmo percorre
    # inicialmente a região superior do círculo.
    x = 0
    y = -raio

    # Variável de decisão do algoritmo do ponto médio.
    # Ela define quando o próximo ponto deve avançar apenas em x
    # ou também ajustar a coordenada y.
    p = -raio

    # O algoritmo calcula somente até o limite do primeiro oitavo.
    # Depois disso, os outros pontos são obtidos por simetria.
    while x < -y:

        # Se p > 0, o ponto médio ficou fora da circunferência.
        # Nesse caso, y é ajustado para aproximar o traçado do círculo.
        if p > 0:
            y += 1
            p += 2 * (x + y) + 1

        # Se p <= 0, o próximo ponto continua avançando apenas em x.
        else:
            p += 2 * x + 1

        # Plota os 8 pontos simétricos do círculo.
        # Cada ponto é desenhado com espessura para formar uma borda grossa.
        plotar_ponto_espesso(canvas, cx + x, cy + y, cor, espessura)
        plotar_ponto_espesso(canvas, cx - x, cy + y, cor, espessura)
        plotar_ponto_espesso(canvas, cx + x, cy - y, cor, espessura)
        plotar_ponto_espesso(canvas, cx - x, cy - y, cor, espessura)

        plotar_ponto_espesso(canvas, cx + y, cy + x, cor, espessura)
        plotar_ponto_espesso(canvas, cx + y, cy - x, cor, espessura)
        plotar_ponto_espesso(canvas, cx - y, cy + x, cor, espessura)
        plotar_ponto_espesso(canvas, cx - y, cy - x, cor, espessura)

        # Avança para o próximo ponto do oitavo calculado.
        x += 1

def plotar_ponto_seguro(canvas, x, y, cor):
    """
    Funcionamento:
        Antes de chamar canvas.set_at, a função verifica se a posição
        está dentro da largura e da altura do canvas.

    Importância:
        Essa verificação evita erros quando uma ferramenta tenta desenhar
        fora da área válida do canvas, por exemplo, quando parte de um
        círculo ultrapassa a borda da área de desenho.

    """

    largura = canvas.get_width()
    altura = canvas.get_height()

    if 0 <= x < largura and 0 <= y < altura:
        canvas.set_at((x, y), cor)

def plotar_ponto_espesso(canvas, x, y, cor, espessura):
    """
    Funcionamento:
        Em vez de pintar apenas um único pixel, a função pinta vários
        pixels ao redor da posição central.

        Para isso, ela percorre uma pequena área quadrada em torno do ponto
        original, usando deslocamentos em x e y.

    Importância:
        Essa função é usada para engrossar o contorno do círculo.

        Sem ela, aumentar a espessura desenhando apenas círculos
        concêntricos pode gerar falhas ou buracos na borda. Ao engrossar
        cada ponto individualmente, o contorno tende a ficar mais contínuo.

    """

    metade = espessura // 2

    for dx in range(-metade, metade + 1):
        for dy in range(-metade, metade + 1):
            plotar_ponto_seguro(canvas, x + dx, y + dy, cor)


def desenhar_retangulo_preenchido(canvas, p1, p2, cor, espessura):
    """
    Desenha um retângulo preenchido pintando todos os pixels
    entre o ponto inicial e o ponto final.

    Depois desenha a borda usando a função desenhar_retangulo.
    """

    x1, y1 = p1
    x2, y2 = p2

    # Garante que funciona independentemente da direção do arrasto do mouse
    inicio_x = min(x1, x2)
    fim_x = max(x1, x2)
    inicio_y = min(y1, y2)
    fim_y = max(y1, y2)


    # Pinta todos os pixels dentro da área do retângulo
    for y in range(inicio_y, fim_y + 1):
        for x in range(inicio_x, fim_x + 1):

            # Verifica se o pixel está dentro dos limites do canvas
            if 0 <= x < canvas.get_width() and 0 <= y < canvas.get_height():
                canvas.set_at((x, y), cor)

def desenhar_circulo_preenchido(canvas, cx, cy, raio, cor, espessura):
    """
    Desenha um círculo preenchido pintando todos os pixels
    dentro do círculo usando o algoritmo de preenchimento por varredura.

    Depois desenha a borda usando a função desenhar_circulo.
    """

    for y in range(cy - raio, cy + raio + 1):
        for x in range(cx - raio, cx + raio + 1):
            if (x - cx) ** 2 + (y - cy) ** 2 <= raio ** 2:
                if 0 <= x < canvas.get_width() and 0 <= y < canvas.get_height():
                    canvas.set_at((x, y), cor)

