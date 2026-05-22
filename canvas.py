import pygame
import config


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


def renderizar_canvas(tela, canvas):
    """
    Desenha o canvas principal dentro da janela do Pygame.
    """

    # Pinta a janela com o cinza clássico do Windows 95/98
    tela.fill(config.COR_JANELA)

    # Copia o conteúdo do canvas para a tela na posição reservada para desenho
    tela.blit(canvas, (config.CANVAS_X, config.CANVAS_Y))
