import pygame

from algoritmos import desenhar_linha_dda, vizinhos_8conectado, pinta_8conectado
from botao import obter_ferramenta_clicada, mouse_sobre_algum_botao


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

        # Evita desenhar em cima da área dos botões
        if mouse_sobre_algum_botao(evento.pos):
            return

        # Inicia o desenho no canvas
        estado["mouse_pressionado"] = True
        estado["ponto_inicial"] = evento.pos
        estado["ponto_final"] = evento.pos

        # Escopo para ferramentas que desenham ao clicar
        if estado["ferramenta"] == "lapis":
            desenhar_linha_dda(canvas, estado["ponto_inicial"], evento.pos, estado["cor_atual"])
            estado["ponto_inicial"] = evento.pos

        elif estado["ferramenta"] == "borracha":
            desenhar_linha_dda(canvas, estado["ponto_inicial"], evento.pos, estado["cor_fundo"], espessura=10)
            estado["ponto_inicial"] = evento.pos
            
        elif estado["ferramenta"] == "preenchimento":
            ponto = evento.pos
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

        # Atualiza o ponto final enquanto o mouse se move
        estado["ponto_final"] = evento.pos

        # Escopo para ferramentas que desenham durante o movimento
        if estado["ferramenta"] == "lapis":
            desenhar_linha_dda(canvas, estado["ponto_inicial"], evento.pos, estado["cor_atual"])
            estado["ponto_inicial"] = evento.pos

        elif estado["ferramenta"] == "borracha":
            desenhar_linha_dda(canvas, estado["ponto_inicial"], evento.pos, estado["cor_fundo"], espessura=10)
            estado["ponto_inicial"] = evento.pos


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

        # Finaliza o desenho
        estado["mouse_pressionado"] = False
        estado["ponto_final"] = evento.pos

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

        # elif estado["ferramenta"] == "retangulo":
        #     pass

        # elif estado["ferramenta"] == "circulo":
        #     pass


            
        # Limpa os pontos depois de finalizar o desenho
        estado["ponto_inicial"] = None
        estado["ponto_final"] = None
