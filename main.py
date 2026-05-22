import pygame

from config import LARGURA, ALTURA, CANVAS_LARGURA, CANVAS_ALTURA, COR_FUNDO, COR_DESENHO, FERRAMENTA_PADRAO
from canvas import criar_canvas, renderizar_canvas
from eventos import tratar_mouse_down, tratar_mouse_motion, tratar_mouse_up
from botao import desenhar_interface_classica

pygame.init()

# A moldura real da janela continua sendo controlada pelo sistema operacional.
# O visual do Paint clássico é desenhado dentro da janela do Pygame.
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("untitled - Paint")

try:
    icone = pygame.image.load("img/paint.png")
    pygame.display.set_icon(icone)
except:
    pass

canvas = criar_canvas(CANVAS_LARGURA, CANVAS_ALTURA, COR_FUNDO)

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
            tratar_mouse_down(evento, estado, canvas)

        elif evento.type == pygame.MOUSEMOTION:
            tratar_mouse_motion(evento, estado, canvas)

        elif evento.type == pygame.MOUSEBUTTONUP:
            tratar_mouse_up(evento, estado, canvas)

    renderizar_canvas(tela, canvas)

    desenhar_interface_classica(tela, estado)

    pygame.display.update()

pygame.quit()
