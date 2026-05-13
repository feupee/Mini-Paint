import pygame

from config import LARGURA, ALTURA, COR_FUNDO, COR_DESENHO, FERRAMENTA_PADRAO
from canvas import criar_canvas, renderizar_canvas
from eventos import tratar_mouse_down, tratar_mouse_motion, tratar_mouse_up, tratar_teclado

pygame.init()

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Mini Paint Raster")
canvas = criar_canvas(LARGURA, ALTURA, COR_FUNDO)

estado = {
    "rodando": True,
    "ferramenta": FERRAMENTA_PADRAO,
    "cor_atual": COR_DESENHO,
    "cor_fundo": COR_FUNDO,
    "mouse_pressionado": False,
    "ponto_inicial": None,
    "ponto_final": None
}

while estado["rodando"]:

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            estado["rodando"] = False

        elif evento.type == pygame.MOUSEBUTTONDOWN:
            tratar_mouse_down(evento, estado)

        elif evento.type == pygame.MOUSEMOTION:
            tratar_mouse_motion(evento, estado)

        elif evento.type == pygame.MOUSEBUTTONUP:
            tratar_mouse_up(evento, estado)

        elif evento.type == pygame.KEYDOWN:
            tratar_teclado(evento, estado, canvas)

    renderizar_canvas(tela, canvas)

    pygame.display.update()

pygame.quit()