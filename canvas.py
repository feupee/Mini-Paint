import pygame
import config
from algoritmos import desenhar_linha_dda, desenhar_circulo, desenhar_retangulo, vizinhos_8conectado, pinta_8conectado


def criar_canvas(largura, altura, cor_fundo):
    """
    Cria uma superfície separada para desenhar.

    Essa superfície funciona como a área de desenho do Mini Paint.
    Tudo que for desenhado nela permanece salvo enquanto o programa estiver rodando.
    """

    # Cria uma nova superfície com a largura e altura recebidas
    canvas = pygame.Surface((largura, altura))

    # Preenche o canvas com a cor de fundo
    canvas.fill(cor_fundo)

    # Retorna o canvas criado
    return canvas


def criar_canvas_preview(canvas, estado):
    """
    Cria uma cópia temporária do canvas com o preview da linha.

    A linha provisória aparece enquanto o botão do mouse está pressionado,
    mas não é gravada no canvas definitivo.
    """

    if (
        estado["ferramenta"] == "linha" and
        estado["mouse_pressionado"] and
        estado["ponto_inicial"] is not None and
        estado["ponto_final"] is not None
    ):
        # Copia o canvas original para desenhar apenas a pré-visualização.
        canvas_preview = canvas.copy()

        desenhar_linha_dda(
            canvas_preview,
            estado["ponto_inicial"],
            estado["ponto_final"],
            estado["cor_atual"],
            estado["espessura"]
        )
        return canvas_preview
    if (
        estado["ferramenta"] == "circulo" and
        estado["mouse_pressionado"] and
        estado["ponto_inicial"] is not None and
        estado["ponto_final"] is not None
    ):
        # Copia o canvas original para desenhar apenas a pré-visualização.
        canvas_preview = canvas.copy()

        desenhar_circulo(
            canvas_preview,
            estado["ponto_inicial"][0],
            estado["ponto_inicial"][1],
            max(abs(estado["ponto_final"][0] - estado["ponto_inicial"][0]), abs(estado["ponto_final"][1] - estado["ponto_inicial"][1])),
            estado["cor_atual"], 
            estado["espessura"]
        )
        return canvas_preview

    elif (
        estado["ferramenta"] == "retangulo" and
        estado["mouse_pressionado"] and
        estado["ponto_inicial"] is not None and
        estado["ponto_final"] is not None and
        estado["preenchido"] is False
    ):
        # Copia o canvas original para desenhar apenas a pré-visualização.
        canvas_preview = canvas.copy()

        desenhar_retangulo(
            canvas_preview,
                estado["ponto_inicial"],
                estado["ponto_final"],
                estado["cor_atual"], 
                estado["espessura"]
        )
        return canvas_preview
    
    elif (
        estado["ferramenta"] == "retangulo" and
        estado["mouse_pressionado"] and
        estado["ponto_inicial"] is not None and
        estado["ponto_final"] is not None and
        estado["preenchido"] is True
    ):
        canvas_preview = canvas.copy()
        ponto = estado["ponto_inicial"]
        cor_original = tuple(canvas_preview.get_at(ponto)[:3])
        cor_nova = tuple(estado["cor_atual"][:3])
        desenhar_retangulo(
            canvas_preview,
            estado["ponto_inicial"],
            estado["ponto_final"],
            estado["cor_atual"], 
            estado["espessura"]
        )
        if cor_original != cor_nova:
            visitado = vizinhos_8conectado(canvas_preview, ponto, cor_original)
            pinta_8conectado(canvas_preview, visitado, cor_nova)
        return canvas_preview

    return canvas


def renderizar_canvas(tela, canvas, estado=None):
    """
    Desenha o canvas principal dentro da janela do Pygame.

    Se receber o estado atual do programa, também desenha uma cópia
    temporária do canvas com a pré-visualização da linha.
    """

    # Pinta a janela com o cinza clássico do Windows 95/98
    tela.fill(config.COR_JANELA)

    canvas_para_renderizar = canvas

    if estado is not None:
        canvas_para_renderizar = criar_canvas_preview(canvas, estado)

    # Copia o conteúdo do canvas para a tela na posição reservada para desenho
    tela.blit(canvas_para_renderizar, (config.CANVAS_X, config.CANVAS_Y))

def limpar_estado_desenho(estado):
    """
    Limpa estados temporários de desenho para impedir que cliques no painel
    sejam interpretados como desenho no canvas.
    """

    estado["mouse_pressionado"] = False
    estado["ponto_inicial"] = None
    estado["ponto_final"] = None