import pygame
import config


# Dicionário usado para guardar imagens já carregadas
# Isso evita carregar a mesma imagem toda hora dentro do loop principal
imagens_cache = {}


def carregar_imagem(caminho):
    """
    Tenta carregar uma imagem para colocar dentro do botão.

    Se a imagem não existir ou der erro, retorna None.
    Nesse caso, o botão exibirá texto no lugar da imagem.
    """

    if caminho in imagens_cache:
        return imagens_cache[caminho]

    try:
        imagem = pygame.image.load(caminho)
        imagem = imagem.convert_alpha()

        imagem = pygame.transform.scale(
            imagem,
            (
                config.BOTAO_IMAGEM_TAMANHO,
                config.BOTAO_IMAGEM_TAMANHO
            )
        )

        imagens_cache[caminho] = imagem
        return imagem

    except:
        imagens_cache[caminho] = None
        return None


def criar_botoes_ferramentas():
    """
    Cria os 6 botões alinhados horizontalmente.

    Cada botão recebe:
    - posição
    - tamanho
    - nome da ferramenta
    - texto
    - imagem
    """

    botoes = []

    for indice, ferramenta in enumerate(config.FERRAMENTAS):
        x = config.BOTAO_X_INICIAL + indice * (
            config.BOTAO_LARGURA + config.BOTAO_ESPACAMENTO
        )

        y = config.BOTAO_Y

        retangulo = pygame.Rect(
            x,
            y,
            config.BOTAO_LARGURA,
            config.BOTAO_ALTURA
        )

        botoes.append(
            {
                "retangulo": retangulo,
                "nome": ferramenta["nome"],
                "rotulo": ferramenta["rotulo"],
                "imagem": ferramenta["imagem"]
            }
        )

    return botoes


def obter_ferramenta_clicada(posicao_mouse):
    """
    Verifica se o usuário clicou em algum botão.

    Se clicou, retorna o nome da ferramenta.
    Se não clicou, retorna None.
    """

    botoes = criar_botoes_ferramentas()

    for botao in botoes:
        if botao["retangulo"].collidepoint(posicao_mouse):
            return botao["nome"]

    return None


def mouse_sobre_algum_botao(posicao_mouse):
    """
    Verifica se o mouse está sobre qualquer botão da barra.
    """

    botoes = criar_botoes_ferramentas()

    for botao in botoes:
        if botao["retangulo"].collidepoint(posicao_mouse):
            return True

    return False


def desenhar_botoes_ferramentas(tela, estado):
    """
    Desenha todos os botões de ferramentas na tela.

    O botão muda de aparência em três situações:
    - normal
    - mouse em cima, hover
    - ferramenta ativa
    """

    botoes = criar_botoes_ferramentas()

    posicao_mouse = pygame.mouse.get_pos()
    mouse_pressionado = pygame.mouse.get_pressed()[0]

    fonte = pygame.font.SysFont(None, 18)

    for botao in botoes:
        retangulo = botao["retangulo"]

        mouse_em_cima = retangulo.collidepoint(posicao_mouse)
        ferramenta_ativa = estado["ferramenta"] == botao["nome"]

        # Cor padrão do botão
        cor = config.COR_BOTAO

        # Se a ferramenta está selecionada, usa cor de ativo
        if ferramenta_ativa:
            cor = config.COR_BOTAO_ATIVO

        # Se o mouse está em cima do botão, usa cor de hover
        if mouse_em_cima:
            cor = config.COR_BOTAO_HOVER

        # Se o botão está sendo clicado, usa cor de clique
        if mouse_em_cima and mouse_pressionado:
            cor = config.COR_BOTAO_CLICADO

        # Desenha o fundo do botão
        pygame.draw.rect(tela, cor, retangulo)

        # Desenha a borda do botão
        pygame.draw.rect(tela, config.COR_BOTAO_BORDA, retangulo, 2)

        # Tenta carregar a imagem do botão
        imagem = carregar_imagem(botao["imagem"])

        if imagem is not None:
            # Centraliza a imagem dentro do botão
            imagem_rect = imagem.get_rect(center=retangulo.center)

            # Desenha a imagem no botão
            tela.blit(imagem, imagem_rect)

        else:
            # Se não houver imagem, mostra o texto da ferramenta
            texto = fonte.render(
                botao["rotulo"],
                True,
                config.COR_BOTAO_TEXTO
            )

            texto_rect = texto.get_rect(center=retangulo.center)

            tela.blit(texto, texto_rect)