import pygame
import config

from algoritmos import desenhar_linha_dda, vizinhos_8conectado, pinta_8conectado, desenhar_circulo, desenhar_quadrado
from botao import obter_ferramenta_clicada, mouse_sobre_algum_botao


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

    return posicao_mouse[1] < obter_altura_barra()


def converter_posicao_para_canvas(posicao_mouse):
    """
    Converte a posição do mouse na janela para a posição correta dentro do canvas.

    Exemplo:
    Se a barra tem 90 pixels de altura e o mouse está em y = 120,
    então dentro do canvas o ponto correto é y = 30.
    """

    x, y = posicao_mouse
    return (x, y - obter_altura_barra())


def ponto_dentro_canvas(canvas, ponto):
    """
    Verifica se o ponto está dentro dos limites do canvas.
    Isso evita erro ao usar ferramentas como o balde de tinta fora da área de desenho.
    """

    x, y = ponto
    return 0 <= x < canvas.get_width() and 0 <= y < canvas.get_height()


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
            desenhar_linha_dda(canvas, estado["ponto_inicial"], ponto_canvas, estado["cor_atual"])
            estado["ponto_inicial"] = ponto_canvas

        elif estado["ferramenta"] == "borracha":
            desenhar_linha_dda(canvas, estado["ponto_inicial"], ponto_canvas, estado["cor_fundo"], espessura=10)
            estado["ponto_inicial"] = ponto_canvas

        elif estado["ferramenta"] == "preenchimento":
            ponto = ponto_canvas
            cor_original = tuple(canvas.get_at(ponto)[:3])
            cor_nova = tuple(estado["cor_atual"][:3])
            if cor_original != cor_nova:
                visitado = vizinhos_8conectado(canvas, ponto, cor_original)
                pinta_8conectado(canvas, visitado, cor_nova)


def tratar_mouse_motion(evento, estado, canvas):
    """
    Trata o movimento do mouse.

    Essa função pode ser usada para ferramentas que desenham
    enquanto o mouse está pressionado, como lápis ou borracha.
    """

    if estado["mouse_pressionado"]:

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
            desenhar_linha_dda(canvas, estado["ponto_inicial"], ponto_canvas, estado["cor_fundo"], espessura=10)
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
                estado["cor_atual"]
            )

        # Escopo para futuras ferramentas

        # elif estado["ferramenta"] == "lapis":
        #     pass

        # elif estado["ferramenta"] == "borracha":
        #     pass

        # Ferramenta retangulo
        elif estado["ferramenta"] == "retangulo":
            desenhar_quadrado(
                canvas,
                estado["ponto_inicial"],
                estado["ponto_final"],
                estado["cor_atual"]
            )

        elif estado["ferramenta"] == "circulo":
             desenhar_circulo(
                 canvas,
                 estado["ponto_inicial"][0],
                 estado["ponto_inicial"][1],
                 max(abs(estado["ponto_final"][0] - estado["ponto_inicial"][0]), abs(estado["ponto_final"][1] - estado["ponto_inicial"][1])),
                 estado["cor_atual"]
             )

        # Limpa os pontos depois de finalizar o desenho
        estado["ponto_inicial"] = None
        estado["ponto_final"] = None
