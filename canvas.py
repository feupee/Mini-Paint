import os
from datetime import datetime

import pygame

import config
from algoritmos import criar_matriz_inteiros, cor_para_inteiro, inteiro_para_cor


def criar_canvas(largura, altura, cor_fundo):
    """
    Cria a matriz principal do canvas.

    A matriz é a representação lógica do desenho. Os algoritmos trabalham nela
    usando put_pixel e get_pixel.
    """

    return criar_matriz_inteiros(largura, altura, cor_fundo)


def criar_canvas_visual(largura, altura, cor_fundo):
    """
    Cria a Surface usada apenas para exibição rápida e exportação.

    Ela evita converter a matriz inteira para imagem a cada frame.
    """

    canvas_visual = pygame.Surface((largura, altura))
    canvas_visual.fill(cor_fundo)

    return canvas_visual


def obter_largura_canvas(canvas):
    if len(canvas) == 0:
        return 0

    return len(canvas[0])


def obter_altura_canvas(canvas):
    return len(canvas)


def limpar_matriz(canvas, cor_fundo):
    """
    Preenche toda a matriz com a cor de fundo.
    """

    cor_inteira = cor_para_inteiro(cor_fundo)

    for y in range(obter_altura_canvas(canvas)):
        for x in range(obter_largura_canvas(canvas)):
            canvas[y][x] = cor_inteira


def copiar_canvas(canvas):
    """
    Cria uma cópia da matriz do canvas.
    """

    return [linha[:] for linha in canvas]


def criar_canvas_preview(canvas_visual, estado):
    """
    Cria uma cópia temporária da Surface visual com a pré-visualização.

    A prévia usa Pygame por desempenho e não altera a matriz definitiva. Quando
    o mouse é solto, o desenho real é gravado na matriz pelos algoritmos.
    """

    if not estado.get("mouse_pressionado"):
        return canvas_visual

    if estado.get("ponto_inicial") is None or estado.get("ponto_final") is None:
        return canvas_visual

    ferramenta = estado.get("ferramenta")

    if ferramenta not in ["linha", "circulo", "retangulo"]:
        return canvas_visual

    canvas_preview = canvas_visual.copy()
    cor = estado["cor_atual"]
    espessura = max(1, estado.get("espessura", 1))
    p1 = estado["ponto_inicial"]
    p2 = estado["ponto_final"]

    if ferramenta == "linha":
        pygame.draw.line(canvas_preview, cor, p1, p2, espessura)

    elif ferramenta == "circulo":
        raio = max(abs(p2[0] - p1[0]), abs(p2[1] - p1[1]))

        if estado.get("preenchido"):
            pygame.draw.circle(canvas_preview, cor, p1, raio, 0)
        else:
            pygame.draw.circle(canvas_preview, cor, p1, raio, espessura)

    elif ferramenta == "retangulo":
        x1, y1 = p1
        x2, y2 = p2

        esquerda = min(x1, x2)
        topo = min(y1, y2)
        largura = abs(x2 - x1)
        altura = abs(y2 - y1)

        rect = pygame.Rect(esquerda, topo, largura, altura)

        if estado.get("preenchido"):
            pygame.draw.rect(canvas_preview, cor, rect, 0)
        else:
            pygame.draw.rect(canvas_preview, cor, rect, espessura)

    return canvas_preview


def renderizar_canvas(tela, canvas_visual, estado=None):
    """
    Desenha o canvas visual dentro da janela do Pygame.
    """

    tela.fill(config.COR_JANELA)

    canvas_para_renderizar = canvas_visual

    if estado is not None:
        canvas_para_renderizar = criar_canvas_preview(canvas_visual, estado)

    tela.blit(canvas_para_renderizar, (config.CANVAS_X, config.CANVAS_Y))


def limpar_estado_desenho(estado):
    """
    Limpa estados temporários de desenho para impedir que cliques no painel
    sejam interpretados como desenho no canvas.
    """

    estado["mouse_pressionado"] = False
    estado["ponto_inicial"] = None
    estado["ponto_final"] = None


def novo_arquivo(canvas, canvas_visual, estado=None):
    """
    Limpa a matriz e a Surface visual, voltando para a tela branca.
    """

    limpar_matriz(canvas, config.COR_FUNDO)
    canvas_visual.fill(config.COR_FUNDO)

    if estado is not None:
        limpar_estado_desenho(estado)


def salvar_canvas_png(canvas_visual):
    """
    Exporta a Surface visual do canvas em PNG.
    """

    os.makedirs("exports", exist_ok=True)

    nome_arquivo = datetime.now().strftime("desenho_%Y%m%d_%H%M%S.png")
    caminho = os.path.join("exports", nome_arquivo)

    pygame.image.save(canvas_visual, caminho)

    return caminho


def sincronizar_regiao_surface_para_matriz(canvas, canvas_visual, rect):
    """
    Copia uma região da Surface visual para a matriz.

    Essa função é usada principalmente pela ferramenta de texto, porque o texto
    é renderizado pelo Pygame. A sincronização é feita só na região alterada,
    não no canvas inteiro.
    """

    esquerda = max(0, rect.left)
    direita = min(obter_largura_canvas(canvas), rect.right)
    topo = max(0, rect.top)
    baixo = min(obter_altura_canvas(canvas), rect.bottom)

    if esquerda >= direita or topo >= baixo:
        return

    pixels = pygame.PixelArray(canvas_visual)

    try:
        for y in range(topo, baixo):
            for x in range(esquerda, direita):
                cor = canvas_visual.unmap_rgb(pixels[x, y])
                canvas[y][x] = cor_para_inteiro(cor[:3])
    finally:
        del pixels


def desenhar_surface_na_matriz(canvas, canvas_visual, superficie, posicao):
    """
    Desenha uma Surface sobre o canvas visual e sincroniza a região alterada
    com a matriz de inteiros.
    """

    rect_atualizado = canvas_visual.blit(superficie, posicao)
    sincronizar_regiao_surface_para_matriz(canvas, canvas_visual, rect_atualizado)

    return rect_atualizado


def matriz_para_surface(canvas):
    """
    Converte a matriz inteira para uma Surface.

    Esta função não é usada a cada frame. Ela fica disponível apenas para
    diagnóstico ou eventual reconstrução completa da visualização.
    """

    largura = obter_largura_canvas(canvas)
    altura = obter_altura_canvas(canvas)

    superficie = pygame.Surface((largura, altura))
    pixels = pygame.PixelArray(superficie)

    try:
        for y in range(altura):
            for x in range(largura):
                pixels[x, y] = superficie.map_rgb(inteiro_para_cor(canvas[y][x]))
    finally:
        del pixels

    return superficie
