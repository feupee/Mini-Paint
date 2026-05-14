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