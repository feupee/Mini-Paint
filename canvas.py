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

    # Copia o conteúdo do canvas para a tela na posição (0, 0)
    tela.blit(canvas, (0, 0))
    tela.blit(canvas, (0, config.ALTURA_BARRA))