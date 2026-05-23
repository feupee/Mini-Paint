import pygame

from config import LARGURA, ALTURA, CANVAS_LARGURA, CANVAS_ALTURA, COR_FUNDO, COR_DESENHO, FERRAMENTA_PADRAO
from canvas import criar_canvas, renderizar_canvas
from eventos import tratar_mouse_down, tratar_mouse_motion, tratar_mouse_up, carregar_cursores, atualizar_cursor
from botao import (
    desenhar_interface_classica,
    obter_rect_barra_janela,
    obter_rect_botao_minimizar,
    obter_rect_botao_maximizar,
    obter_rect_botao_fechar
)

try:
    from pygame._sdl2.video import Window
except:
    Window = None

pygame.init()

# Com pygame.NOFRAME, a barra padrão do Windows fica escondida.
tela = pygame.display.set_mode((LARGURA, ALTURA), pygame.NOFRAME)
pygame.display.set_caption("untitled - Paint")

# Carregar os cursores do paint
cursores = carregar_cursores()

janela = None

if Window is not None:
    try:
        janela = Window.from_display_module()
    except:
        janela = None

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
    "ponto_final": None,
    "arrastando_janela": False,
    "botao_janela_pressionado": None
}

while estado["rodando"]:

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            estado["rodando"] = False

        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:

                rect_fechar = obter_rect_botao_fechar(tela)
                rect_minimizar = obter_rect_botao_minimizar(tela)
                rect_maximizar = obter_rect_botao_maximizar(tela)
                rect_barra = obter_rect_barra_janela(tela)

                if rect_fechar.collidepoint(evento.pos):
                    estado["botao_janela_pressionado"] = "fechar"

                elif rect_minimizar.collidepoint(evento.pos):
                    estado["botao_janela_pressionado"] = "minimizar"

                elif rect_maximizar.collidepoint(evento.pos):
                    # Botão maximizar existe visualmente, mas não faz nada.
                    estado["botao_janela_pressionado"] = None

                elif rect_barra.collidepoint(evento.pos):
                    estado["arrastando_janela"] = True

                else:
                    tratar_mouse_down(evento, estado, canvas)
                    atualizar_cursor(estado["ferramenta"], cursores, evento.pos)

            else:
                tratar_mouse_down(evento, estado, canvas)
                atualizar_cursor(estado["ferramenta"], cursores, evento.pos)

        elif evento.type == pygame.MOUSEMOTION:
            if estado["arrastando_janela"]:

                if janela is not None:
                    x, y = janela.position
                    dx, dy = evento.rel
                    janela.position = (x + dx, y + dy)

            else:
                tratar_mouse_motion(evento, estado, canvas)
                atualizar_cursor(estado["ferramenta"], cursores, evento.pos)

        elif evento.type == pygame.MOUSEBUTTONUP:
            if evento.button == 1:

                rect_fechar = obter_rect_botao_fechar(tela)
                rect_minimizar = obter_rect_botao_minimizar(tela)

                if estado["botao_janela_pressionado"] == "fechar":
                    if rect_fechar.collidepoint(evento.pos):
                        estado["rodando"] = False

                elif estado["botao_janela_pressionado"] == "minimizar":
                    if rect_minimizar.collidepoint(evento.pos):
                        pygame.display.iconify()

                elif estado["arrastando_janela"]:
                    estado["arrastando_janela"] = False

                else:
                    tratar_mouse_up(evento, estado, canvas)

                estado["botao_janela_pressionado"] = None
                estado["arrastando_janela"] = False

            else:
                tratar_mouse_up(evento, estado, canvas)

    renderizar_canvas(tela, canvas)

    desenhar_interface_classica(tela, estado)

    pygame.display.update()

pygame.quit()