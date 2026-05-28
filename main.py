import pygame

from config import (
    LARGURA,
    ALTURA,
    CANVAS_LARGURA,
    CANVAS_ALTURA,
    COR_FUNDO,
    COR_DESENHO,
    FERRAMENTA_PADRAO
)
from canvas import (
    criar_canvas,
    criar_canvas_visual,
    renderizar_canvas,
    limpar_estado_desenho,
    novo_arquivo,
    salvar_canvas_png
)
from eventos import (
    tratar_mouse_down,
    tratar_mouse_motion,
    tratar_mouse_up,
    carregar_cursores,
    atualizar_cursor,
    tratar_key_down_texto,
    desenhar_previa_texto
)
from botao import (
    desenhar_interface_classica,
    obter_rect_barra_janela,
    obter_rect_botao_minimizar,
    obter_rect_botao_maximizar,
    obter_rect_botao_fechar,
    obter_opcao_menu_clicada,
    obter_botoes_espessura,
    obter_botoes_preenchido,
    obter_botoes_tamanho_fonte
)

try:
    from pygame._sdl2.video import Window
except:
    Window = None

pygame.init()

# Com pygame.NOFRAME, a barra padrão do Windows fica escondida.
tela = pygame.display.set_mode((LARGURA, ALTURA), pygame.NOFRAME)
pygame.display.set_caption("untitled - Paint")

clock = pygame.time.Clock()

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

# Matriz lógica do desenho. Os algoritmos escrevem nela usando put_pixel.
canvas = criar_canvas(CANVAS_LARGURA, CANVAS_ALTURA, COR_FUNDO)

# Surface visual usada para exibição rápida, pré-visualização e exportação.
canvas_visual = criar_canvas_visual(CANVAS_LARGURA, CANVAS_ALTURA, COR_FUNDO)

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
    "menu_pressionado": None,
    "clicando_painel_opcoes": False,
    "espessura": 1,
    "preenchido": False,
    "texto_digitando": False,
    "texto_posicao": None,
    "texto_atual": "",
    "texto_tamanho": 20
}


def tratar_clique_espessura(posicao_mouse, estado):
    """
    Verifica se o usuário clicou em algum botão de espessura.
    Só funciona quando a ferramenta atual NÃO é texto.
    """

    if estado["ferramenta"] == "texto":
        return False

    for botao in obter_botoes_espessura():
        if botao["rect"].collidepoint(posicao_mouse):
            estado["espessura"] = botao["valor"]
            return True

    return False


def tratar_clique_tamanho_fonte(posicao_mouse, estado):
    """
    Verifica se o usuário clicou em algum botão de tamanho da fonte.
    Só funciona quando a ferramenta atual é texto.
    """

    if estado["ferramenta"] != "texto":
        return False

    for botao in obter_botoes_tamanho_fonte():
        if botao["rect"].collidepoint(posicao_mouse):
            estado["texto_tamanho"] = botao["valor"]
            return True

    return False


def tratar_clique_preenchido(posicao_mouse, estado):
    """
    Verifica se o usuário clicou em algum botão de preenchimento.
    Só funciona para retângulo e círculo.
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

    Trata:
    - espessura para ferramentas comuns;
    - tamanho da fonte para a ferramenta texto;
    - preenchido / não preenchido para retângulo e círculo.
    """

    clicou_em_espessura = tratar_clique_espessura(posicao_mouse, estado)
    clicou_em_fonte = tratar_clique_tamanho_fonte(posicao_mouse, estado)
    clicou_em_preenchido = tratar_clique_preenchido(posicao_mouse, estado)

    if clicou_em_espessura or clicou_em_fonte or clicou_em_preenchido:
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

                opcao_menu = obter_opcao_menu_clicada(evento.pos)

                if rect_fechar.collidepoint(evento.pos):
                    estado["botao_janela_pressionado"] = "fechar"

                elif rect_minimizar.collidepoint(evento.pos):
                    estado["botao_janela_pressionado"] = "minimizar"

                elif rect_maximizar.collidepoint(evento.pos):
                    # Botão maximizar existe visualmente, mas não faz nada.
                    estado["botao_janela_pressionado"] = None

                elif opcao_menu is not None:
                    estado["menu_pressionado"] = opcao_menu
                    limpar_estado_desenho(estado)

                elif rect_barra.collidepoint(evento.pos):
                    estado["arrastando_janela"] = True

                else:
                    clicou_no_painel = tratar_clique_painel_opcoes(evento.pos, estado)

                    if not clicou_no_painel:
                        tratar_mouse_down(evento, estado, canvas, canvas_visual)

                    atualizar_cursor(estado["ferramenta"], cursores, evento.pos)

            else:
                tratar_mouse_down(evento, estado, canvas, canvas_visual)
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
                tratar_mouse_motion(evento, estado, canvas, canvas_visual)
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

                elif estado["menu_pressionado"] is not None:
                    opcao_menu = obter_opcao_menu_clicada(evento.pos)

                    if opcao_menu == estado["menu_pressionado"]:

                        if opcao_menu.lower() == "new file":
                            novo_arquivo(canvas, canvas_visual, estado)

                        elif opcao_menu.lower() == "save":
                            caminho_salvo = salvar_canvas_png(canvas_visual)
                            print(f"Canvas salvo em: {caminho_salvo}")

                    estado["menu_pressionado"] = None

                elif estado["clicando_painel_opcoes"]:
                    estado["clicando_painel_opcoes"] = False
                    limpar_estado_desenho(estado)

                else:
                    tratar_mouse_up(evento, estado, canvas, canvas_visual)

                estado["botao_janela_pressionado"] = None
                estado["menu_pressionado"] = None
                estado["arrastando_janela"] = False
                estado["clicando_painel_opcoes"] = False

            else:
                tratar_mouse_up(evento, estado, canvas, canvas_visual)

        elif evento.type == pygame.KEYDOWN:
            if estado["texto_digitando"]:
                tratar_key_down_texto(evento, estado, canvas, canvas_visual)

    if estado["texto_digitando"]:
        canvas_exibicao = canvas_visual.copy()
        desenhar_previa_texto(canvas_exibicao, estado)
    else:
        canvas_exibicao = canvas_visual

    renderizar_canvas(tela, canvas_exibicao, estado)

    desenhar_interface_classica(tela, estado)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
