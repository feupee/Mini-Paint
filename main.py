import pygame

from config import LARGURA, ALTURA, CANVAS_LARGURA, CANVAS_ALTURA, COR_FUNDO, COR_DESENHO, FERRAMENTA_PADRAO
from canvas import criar_canvas, renderizar_canvas
from eventos import tratar_mouse_down, tratar_mouse_motion, tratar_mouse_up, carregar_cursores, atualizar_cursor
from botao import (
    desenhar_interface_classica,
    obter_rect_barra_janela,
    obter_rect_botao_minimizar,
    obter_rect_botao_maximizar,
    obter_rect_botao_fechar,
    obter_botoes_espessura,
    obter_botoes_preenchido
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
    "botao_janela_pressionado": None,
    "clicando_painel_opcoes": False,
    "espessura": 1,
    "preenchido": False
}


def limpar_estado_desenho(estado):
    """
    Limpa estados temporários de desenho para impedir que cliques no painel
    sejam interpretados como desenho no canvas.
    """

    estado["mouse_pressionado"] = False
    estado["ponto_inicial"] = None
    estado["ponto_final"] = None


def tratar_clique_espessura(posicao_mouse, estado):
    """
    Verifica se o usuário clicou em algum botão de espessura.
    Se clicou, altera estado["espessura"] e retorna True.
    Caso contrário, retorna False.
    """

    for botao in obter_botoes_espessura():
        if botao["rect"].collidepoint(posicao_mouse):
            estado["espessura"] = botao["valor"]
            return True

    return False


def tratar_clique_preenchido(posicao_mouse, estado):
    """
    Verifica se o usuário clicou em algum botão de preenchimento.
    Se clicou, altera estado["preenchido"] e retorna True.
    Caso contrário, retorna False.
    """

    if estado["ferramenta"] not in ["retangulo", "circulo"]:
        return False

    for botao in obter_botoes_preenchido():
        if botao["rect"].collidepoint(posicao_mouse):
            estado["preenchido"] = botao["valor"]
            return True

    return False


def tratar_clique_painel_opcoes(posicao_mouse, estado):
    """
    Verifica cliques nos botões do painel de opções.
    Atualmente trata:
    - espessura;
    - preenchido / não preenchido.
    """

    clicou_em_espessura = tratar_clique_espessura(posicao_mouse, estado)
    clicou_em_preenchido = tratar_clique_preenchido(posicao_mouse, estado)

    if clicou_em_espessura or clicou_em_preenchido:
        estado["clicando_painel_opcoes"] = True
        limpar_estado_desenho(estado)
        return True

    return False


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
                    clicou_no_painel = tratar_clique_painel_opcoes(evento.pos, estado)

                    if not clicou_no_painel:
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

            elif estado["clicando_painel_opcoes"]:
                atualizar_cursor(estado["ferramenta"], cursores, evento.pos)

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

                elif estado["clicando_painel_opcoes"]:
                    estado["clicando_painel_opcoes"] = False
                    limpar_estado_desenho(estado)

                else:
                    tratar_mouse_up(evento, estado, canvas)

                estado["botao_janela_pressionado"] = None
                estado["arrastando_janela"] = False
                estado["clicando_painel_opcoes"] = False

            else:
                tratar_mouse_up(evento, estado, canvas)

    renderizar_canvas(tela, canvas, estado)

    desenhar_interface_classica(tela, estado)

    pygame.display.update()

pygame.quit()