def desenhar_linha_dda(canvas, ponto_inicial, ponto_final, cor):
    """
    Desenha uma linha usando o algoritmo DDA.

    O algoritmo DDA calcula pontos intermediários entre dois pontos:
    ponto_inicial = (x1, y1)
    ponto_final = (x2, y2)

    Depois, ele pinta pixel por pixel no canvas.
    """

    # Separa as coordenadas do ponto inicial
    x1, y1 = ponto_inicial

    # Separa as coordenadas do ponto final
    x2, y2 = ponto_final

    # Calcula a diferença entre os pontos no eixo X
    dx = x2 - x1

    # Calcula a diferença entre os pontos no eixo Y
    dy = y2 - y1

    # Define a quantidade de passos necessários para desenhar a linha
    # Usa o maior valor entre dx e dy para garantir que a linha fique contínua
    passos = max(abs(dx), abs(dy))

    # Caso especial:
    # Se o usuário clicar sem arrastar o mouse, o ponto inicial e final são iguais
    if passos == 0:

        # Verifica se o ponto está dentro dos limites do canvas
        if 0 <= x1 < canvas.get_width() and 0 <= y1 < canvas.get_height():

            # Desenha apenas um pixel
            canvas.set_at((x1, y1), cor)

        # Encerra a função
        return

    # Calcula quanto o X deve avançar a cada passo
    incremento_x = dx / passos

    # Calcula quanto o Y deve avançar a cada passo
    incremento_y = dy / passos

    # Começa o desenho no ponto inicial
    x = x1
    y = y1

    # Repete até chegar ao ponto final
    for _ in range(passos + 1):

        # Arredonda os valores para encontrar o pixel mais próximo
        pixel_x = round(x)
        pixel_y = round(y)

        # Verifica se o pixel está dentro dos limites do canvas
        # Verifica valores dentro do espaço dito de 800x600 sendo a ponta esquerda superior (0,0) e a ponta direita inferior (799, 599)
        if 0 <= pixel_x < canvas.get_width() and 0 <= pixel_y < canvas.get_height():

            # Pinta o pixel no canvas
            canvas.set_at((pixel_x, pixel_y), cor)

        # Avança para o próximo ponto da linha
        x += incremento_x
        y += incremento_y


def apagar_desenho(canvas, ponto_inicial, ponto_final, cor, espessura=1):
    """
    Apaga um desenho usando o algoritmo DDA com suporte a espessura variável.
    """
    # Separa as coordenadas
    x1, y1 = ponto_inicial
    x2, y2 = ponto_final

    dx = x2 - x1
    dy = y2 - y1

    passos = max(abs(dx), abs(dy))
    
    # Calcula o raio de espessura para apagar
    raio = espessura // 2
    ajuste_par = espessura % 2

    # Caso especial: clique sem arrastar (desenha apenas o ponto/bloco inicial)
    if passos == 0:
        for i in range(-raio, raio + ajuste_par):
            for j in range(-raio, raio + ajuste_par):
                px = x1 + i
                py = y1 + j
                if 0 <= px < canvas.get_width() and 0 <= py < canvas.get_height():
                    canvas.set_at((px, py), cor)
        return

    # Cálculos dos incrementos para o DDA
    incremento_x = dx / passos
    incremento_y = dy / passos

    x = x1
    y = y1

    # Desenha a linha passo a passo
    for _ in range(passos + 1):
        pixel_x = round(x)
        pixel_y = round(y)

        # Loops embutidos diretamente para criar o efeito de linha mais grossa
        for i in range(-raio, raio + ajuste_par):
            for j in range(-raio, raio + ajuste_par):
                px = pixel_x + i
                py = pixel_y + j
                
                # Verifica as bordas do canvas para cada pixel do bloco
                if 0 <= px < canvas.get_width() and 0 <= py < canvas.get_height():
                    canvas.set_at((px, py), cor)

        # Avança para o próximo ponto da linha
        x += incremento_x
        y += incremento_y