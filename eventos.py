import pygame
import config

from algoritmos import desenhar_linha_dda, vizinhos_8conectado, pinta_8conectado, desenhar_circulo, desenhar_retangulo, desenhar_retangulo_preenchido
from botao import obter_ferramenta_clicada, obter_cor_clicada, mouse_sobre_algum_botao, mouse_sobre_interface



def obter_altura_barra():
    """
    Retorna a altura da barra superior.

    Se a constante ALTURA_BARRA ainda não existir em config.py,
    usa 0 para manter compatibilidade com a versão antiga do projeto.
    """

    return getattr(config, "ALTURA_BARRA", 0)


def mouse_sobre_barra(posicao_mouse):
    """
    Verifica se o mouse está na área da barra superior.
    """

    return posicao_mouse[1] < config.MENU_ALTURA


def converter_posicao_para_canvas(posicao_mouse):
    """
    Converte a posição do mouse na janela para a posição correta dentro do canvas.

    Exemplo:
    Se o canvas começa em x = 70 e y = 32, e o mouse está em (100, 80),
    então dentro do canvas o ponto correto é (30, 48).
    """

    x, y = posicao_mouse
    return (x - config.CANVAS_X, y - config.CANVAS_Y)


def ponto_dentro_canvas(canvas, ponto):
    """
    Verifica se o ponto está dentro dos limites do canvas.
    Isso evita erro ao usar ferramentas como o balde de tinta fora da área de desenho.
    """

    x, y = ponto
    return 0 <= x < canvas.get_width() and 0 <= y < canvas.get_height()


def ponto_janela_dentro_canvas(posicao_mouse):
    """
    Verifica se a posição do mouse, ainda em coordenadas da janela,
    está dentro da área visível do canvas.
    """

    x, y = posicao_mouse
    return (
        config.CANVAS_X <= x < config.CANVAS_X + config.CANVAS_LARGURA and
        config.CANVAS_Y <= y < config.CANVAS_Y + config.CANVAS_ALTURA
    )


def tratar_mouse_down(evento, estado, canvas):
    """
    Trata o clique do mouse.

    Primeiro verifica se o clique foi em algum botão.
    Se foi, troca a ferramenta.
    Se não foi, inicia o desenho no canvas.
    """

    if evento.button == 1:

        ferramenta_clicada = obter_ferramenta_clicada(evento.pos)

        # Se clicou em algum botão de ferramenta
        if ferramenta_clicada is not None:
            estado["ferramenta"] = ferramenta_clicada

            estado["mouse_pressionado"] = False
            estado["ponto_inicial"] = None
            estado["ponto_final"] = None

            return

        cor_clicada = obter_cor_clicada(evento.pos)

        # Se clicou em alguma cor da paleta
        if cor_clicada is not None:
            estado["cor_atual"] = cor_clicada

            estado["mouse_pressionado"] = False
            estado["ponto_inicial"] = None
            estado["ponto_final"] = None

            return

        # Evita desenhar em cima da área da interface
        if mouse_sobre_interface(evento.pos):
            return

        # Evita desenhar em cima da área da barra superior
        if mouse_sobre_barra(evento.pos):
            return

        # Evita desenhar em cima da área dos botões
        if mouse_sobre_algum_botao(evento.pos):
            return

        ponto_canvas = converter_posicao_para_canvas(evento.pos)

        if not ponto_dentro_canvas(canvas, ponto_canvas):
            return

        # Inicia o desenho no canvas
        estado["mouse_pressionado"] = True
        estado["ponto_inicial"] = ponto_canvas
        estado["ponto_final"] = ponto_canvas

        # Escopo para ferramentas que desenham ao clicar
        if estado["ferramenta"] == "lapis":
            desenhar_linha_dda(canvas, estado["ponto_inicial"], ponto_canvas, estado["cor_atual"], estado["espessura"])
            estado["ponto_inicial"] = ponto_canvas

        elif estado["ferramenta"] == "borracha":
            desenhar_linha_dda(canvas, estado["ponto_inicial"], ponto_canvas, estado["cor_fundo"], estado["espessura"])
            estado["ponto_inicial"] = ponto_canvas

        elif estado["ferramenta"] == "preenchimento":
            ponto = ponto_canvas
            cor_original = tuple(canvas.get_at(ponto)[:3])
            cor_nova = tuple(estado["cor_atual"][:3])
            if cor_original != cor_nova:
                visitado = vizinhos_8conectado(canvas, ponto, cor_original)
                pinta_8conectado(canvas, visitado, cor_nova)
    
        elif estado["ferramenta"] == "conta-gotas":
            cor_clicada = canvas.get_at(ponto_canvas)
            estado["cor_atual"] = cor_clicada


def tratar_mouse_motion(evento, estado, canvas):
    """
    Trata o movimento do mouse.

    Essa função pode ser usada para ferramentas que desenham
    enquanto o mouse está pressionado, como lápis ou borracha.
    """

    if estado["mouse_pressionado"]:

        if not ponto_janela_dentro_canvas(evento.pos):
            return

        ponto_canvas = converter_posicao_para_canvas(evento.pos)

        if not ponto_dentro_canvas(canvas, ponto_canvas):
            return

        # Atualiza o ponto final enquanto o mouse se move
        estado["ponto_final"] = ponto_canvas

        # Escopo para ferramentas que desenham durante o movimento
        if estado["ferramenta"] == "lapis":
            desenhar_linha_dda(canvas, estado["ponto_inicial"], ponto_canvas, estado["cor_atual"])
            estado["ponto_inicial"] = ponto_canvas

        elif estado["ferramenta"] == "borracha":
            desenhar_linha_dda(canvas, estado["ponto_inicial"], ponto_canvas, estado["cor_fundo"], estado["espessura"])
            estado["ponto_inicial"] = ponto_canvas


def tratar_mouse_up(evento, estado, canvas):
    """
    Trata o momento em que o usuário solta o botão do mouse.
    """

    if evento.button == 1:

        # Se não existe ponto inicial, significa que o clique foi em algum botão
        # ou em uma área que não deve gerar desenho
        if estado["ponto_inicial"] is None:
            estado["mouse_pressionado"] = False
            estado["ponto_final"] = None
            return

        if not ponto_janela_dentro_canvas(evento.pos):
            estado["mouse_pressionado"] = False
            estado["ponto_inicial"] = None
            estado["ponto_final"] = None
            return

        ponto_canvas = converter_posicao_para_canvas(evento.pos)

        if not ponto_dentro_canvas(canvas, ponto_canvas):
            estado["mouse_pressionado"] = False
            estado["ponto_inicial"] = None
            estado["ponto_final"] = None
            return

        # Finaliza o desenho
        estado["mouse_pressionado"] = False
        estado["ponto_final"] = ponto_canvas

        # Ferramenta linha usando o algoritmo DDA
        if estado["ferramenta"] == "linha":
            desenhar_linha_dda(
                canvas,
                estado["ponto_inicial"],
                estado["ponto_final"],
                estado["cor_atual"], 
                estado["espessura"]
            )

        # Escopo para futuras ferramentas

        # elif estado["ferramenta"] == "lapis":
        #     pass

        # elif estado["ferramenta"] == "borracha":
        #     pass

        # Ferramenta retangulo
        elif estado["ferramenta"] == "retangulo" and estado["preenchido"] is False:
            desenhar_retangulo(
                canvas,
                estado["ponto_inicial"],
                estado["ponto_final"],
                estado["cor_atual"], 
                estado["espessura"]
            )

        elif estado["ferramenta"] == "retangulo" and estado["preenchido"] is True:
            desenhar_retangulo_preenchido(
                canvas,
                estado["ponto_inicial"],
                estado["ponto_final"],
                estado["cor_atual"],
                espessura=1
            )

        elif estado["ferramenta"] == "circulo":
             desenhar_circulo(
                 canvas,
                 estado["ponto_inicial"][0],
                 estado["ponto_inicial"][1],
                 max(abs(estado["ponto_final"][0] - estado["ponto_inicial"][0]), abs(estado["ponto_final"][1] - estado["ponto_inicial"][1])),
                 estado["cor_atual"], 
                 estado["espessura"]
             )

        # Limpa os pontos depois de finalizar o desenho
        estado["ponto_inicial"] = None
        estado["ponto_final"] = None

def carregar_cursor_png(caminho, hotspot=(0, 0)):
    """
    Carrega uma imagem PNG e transforma em cursor do pygame.
    """

    imagem = pygame.image.load(caminho).convert_alpha()
    cursor = pygame.cursors.Cursor(hotspot, imagem)

    return cursor

def carregar_cursores():
    cursores = {}

    for ferramenta in config.FERRAMENTAS:

        cursores[ferramenta["nome"]] = carregar_cursor_png(
            ferramenta["cursor"],
            ferramenta["hotspot"]
        )

    return cursores

def atualizar_cursor(ferramenta, cursores, posicao_mouse=None):
    """
    Altera o cursor do mouse de acordo com a ferramenta selecionada,
    mas somente quando o mouse está dentro da área do canvas.

    Fora do canvas, o cursor volta a ser o cursor padrão do sistema.
    """

    if posicao_mouse is None:
        posicao_mouse = pygame.mouse.get_pos()

    if not ponto_janela_dentro_canvas(posicao_mouse):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        return

    if ferramenta in cursores:
        pygame.mouse.set_cursor(cursores[ferramenta])
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
