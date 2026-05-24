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


def fonte_classica(tamanho=14):
    """
    Retorna uma fonte parecida com a usada nas versões antigas do Windows.
    Se a fonte não existir no sistema, o Pygame usa uma fonte alternativa.
    """

    return pygame.font.SysFont("MS Sans Serif", tamanho)


def desenhar_borda_3d(tela, retangulo, pressionado=False):
    """
    Desenha o efeito 3D clássico do Windows 95/98.

    Quando pressionado=False, a borda parece elevada.
    Quando pressionado=True, a borda parece afundada.
    """

    if pressionado:
        cor_superior_esquerda = config.COR_CINZA_ESCURO
        cor_inferior_direita = config.COR_BOTAO_BORDA_CLARA
    else:
        cor_superior_esquerda = config.COR_BOTAO_BORDA_CLARA
        cor_inferior_direita = config.COR_CINZA_ESCURO

    pygame.draw.line(tela, cor_superior_esquerda, retangulo.topleft, retangulo.topright)
    pygame.draw.line(tela, cor_superior_esquerda, retangulo.topleft, retangulo.bottomleft)
    pygame.draw.line(tela, cor_inferior_direita, retangulo.bottomleft, retangulo.bottomright)
    pygame.draw.line(tela, cor_inferior_direita, retangulo.topright, retangulo.bottomright)


def desenhar_borda_rebaixada(tela, retangulo):
    """
    Desenha uma moldura rebaixada, como caixas e painéis do Paint clássico.
    """

    pygame.draw.line(tela, config.COR_CINZA_ESCURO, retangulo.topleft, retangulo.topright)
    pygame.draw.line(tela, config.COR_CINZA_ESCURO, retangulo.topleft, retangulo.bottomleft)
    pygame.draw.line(tela, config.COR_BOTAO_BORDA_CLARA, retangulo.bottomleft, retangulo.bottomright)
    pygame.draw.line(tela, config.COR_BOTAO_BORDA_CLARA, retangulo.topright, retangulo.bottomright)


def criar_botoes_ferramentas():
    """
    Cria os 6 botões em uma barra lateral, no estilo do Paint clássico.

    Cada botão recebe:
    - posição
    - tamanho
    - nome da ferramenta
    - texto
    - imagem
    """

    botoes = []

    for indice, ferramenta in enumerate(config.FERRAMENTAS):
        coluna = indice % config.BOTAO_COLUNAS
        linha = indice // config.BOTAO_COLUNAS

        x = config.BOTAO_X_INICIAL + coluna * (
            config.BOTAO_LARGURA + config.BOTAO_ESPACAMENTO
        )

        y = config.BOTAO_Y + linha * (
            config.BOTAO_ALTURA + config.BOTAO_ESPACAMENTO
        )

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


def criar_botoes_cores():
    """
    Cria os retângulos clicáveis da paleta de cores inferior.
    """

    botoes = []
    inicio_x = config.PALETA_X + 58
    inicio_y = config.PALETA_Y + 8

    for indice, cor in enumerate(config.CORES_PALETA):
        coluna = indice % 10
        linha = indice // 10

        x = inicio_x + coluna * (config.COR_TAMANHO + config.COR_ESPACAMENTO)
        y = inicio_y + linha * (config.COR_TAMANHO + config.COR_ESPACAMENTO)

        botoes.append(
            {
                "retangulo": pygame.Rect(x, y, config.COR_TAMANHO, config.COR_TAMANHO),
                "cor": cor
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


def obter_cor_clicada(posicao_mouse):
    """
    Verifica se o usuário clicou em alguma cor da paleta.
    """

    botoes_cores = criar_botoes_cores()

    for botao_cor in botoes_cores:
        if botao_cor["retangulo"].collidepoint(posicao_mouse):
            return botao_cor["cor"]

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


def mouse_sobre_interface(posicao_mouse):
    """
    Verifica se o mouse está em alguma área da interface que não é o canvas.
    """

    x, y = posicao_mouse
    dentro_canvas = (
        config.CANVAS_X <= x < config.CANVAS_X + config.CANVAS_LARGURA and
        config.CANVAS_Y <= y < config.CANVAS_Y + config.CANVAS_ALTURA
    )

    return not dentro_canvas


def desenhar_menu(tela):
    """
    Desenha a barra de menu superior: File, Edit, View, Image, Colors e Help.
    """

    pygame.draw.rect(
        tela,
        config.COR_JANELA,
        (0, 0, config.LARGURA, config.MENU_ALTURA)
    )

    pygame.draw.line(
        tela,
        config.COR_BOTAO_BORDA_CLARA,
        (0, 0),
        (config.LARGURA, 0)
    )
    pygame.draw.line(
        tela,
        config.COR_CINZA_MEDIO,
        (0, config.MENU_ALTURA - 1),
        (config.LARGURA, config.MENU_ALTURA - 1)
    )

    fonte_menu = fonte_classica(18)

    x_menu = 8
    for menu in config.MENU_OPCOES:
        texto_menu = fonte_menu.render(menu, True, config.COR_PRETO)
        tela.blit(texto_menu, (x_menu, 5))
        x_menu += texto_menu.get_width() + 18

def desenhar_area_ferramentas(tela):
    """
    Desenha o painel cinza da barra lateral de ferramentas.
    """

    retangulo = pygame.Rect(
        config.BARRA_FERRAMENTAS_X,
        config.BARRA_FERRAMENTAS_Y,
        config.BARRA_FERRAMENTAS_LARGURA,
        config.CANVAS_ALTURA + config.SCROLLBAR_TAMANHO
    )

    pygame.draw.rect(tela, config.COR_JANELA, retangulo)


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

    fonte = fonte_classica(12)

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

        # Desenha a borda do botão estilo Windows clássico
        desenhar_borda_3d(
            tela,
            retangulo,
            pressionado=ferramenta_ativa or (mouse_em_cima and mouse_pressionado)
        )

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

def obter_rect_painel_opcoes():
    """
    Retorna o retângulo do painel de opções da ferramenta.
    """

    return pygame.Rect(
        config.BOTAO_X_INICIAL,
        config.BOTAO_Y + 4 * (config.BOTAO_ALTURA + config.BOTAO_ESPACAMENTO),
        config.BARRA_FERRAMENTAS_LARGURA - 8,
        88
    )


def desenhar_painel_opcoes_ferramenta(tela, estado):
    """
    Desenha um pequeno painel decorativo abaixo dos botões, parecido com o Paint clássico.
    """

    painel = obter_rect_painel_opcoes()

    pygame.draw.rect(tela, config.COR_JANELA, painel)

    fonte = pygame.font.SysFont(None, 15)

    # Texto Espessura
    texto_espessura = fonte.render("Espessura", True, config.COR_TEXTO)
    tela.blit(texto_espessura, (painel.x + 0, painel.y + 5))

    # Botões de espessura
    botoes_espessura = obter_botoes_espessura()

    for botao in botoes_espessura:
        rect = botao["rect"]
        valor = botao["valor"]

        if estado["espessura"] == valor:
            cor = config.COR_BOTAO_PRESSIONADO
        else:
            cor = config.COR_BOTAO

        pygame.draw.rect(tela, cor, rect)
        pygame.draw.rect(tela, config.COR_BORDA, rect, 1)

        texto_valor = fonte.render(str(valor), True, config.COR_TEXTO)

        texto_x = rect.centerx - texto_valor.get_width() // 2
        texto_y = rect.centery - texto_valor.get_height() // 2

        tela.blit(texto_valor, (texto_x, texto_y))

    # Botões de preenchimento aparecem somente para formas
    if estado["ferramenta"] in ["retangulo", "circulo"]:

        texto_forma = fonte.render("Forma", True, config.COR_TEXTO)
        tela.blit(texto_forma, (painel.x + 0, painel.y + 55))

        botoes_preenchido = obter_botoes_preenchido()

        for botao in botoes_preenchido:
            rect = botao["rect"]
            valor = botao["valor"]

            if estado["preenchido"] == valor:
                cor = config.COR_BOTAO_PRESSIONADO
            else:
                cor = config.COR_BOTAO

            pygame.draw.rect(tela, cor, rect)
            pygame.draw.rect(tela, config.COR_BORDA, rect, 1)

            desenhar_icone_preenchido(tela, rect, valor)
    
def desenhar_moldura_canvas(tela):
    """
    Desenha a moldura e as barras falsas de rolagem da área de desenho.
    """

    moldura = pygame.Rect(
        config.CANVAS_X - 2,
        config.CANVAS_Y - 2,
        config.CANVAS_LARGURA + 4,
        config.CANVAS_ALTURA + 4
    )

    desenhar_borda_rebaixada(tela, moldura)

    barra_vertical = pygame.Rect(
        config.CANVAS_X + config.CANVAS_LARGURA,
        config.CANVAS_Y,
        config.SCROLLBAR_TAMANHO,
        config.CANVAS_ALTURA
    )

    barra_horizontal = pygame.Rect(
        config.CANVAS_X,
        config.CANVAS_Y + config.CANVAS_ALTURA,
        config.CANVAS_LARGURA,
        config.SCROLLBAR_TAMANHO
    )

    canto = pygame.Rect(
        config.CANVAS_X + config.CANVAS_LARGURA,
        config.CANVAS_Y + config.CANVAS_ALTURA,
        config.SCROLLBAR_TAMANHO,
        config.SCROLLBAR_TAMANHO
    )

    pygame.draw.rect(tela, config.COR_CINZA_CLARO, barra_vertical)
    pygame.draw.rect(tela, config.COR_CINZA_CLARO, barra_horizontal)
    pygame.draw.rect(tela, config.COR_JANELA, canto)

    desenhar_borda_3d(tela, barra_vertical, pressionado=True)
    desenhar_borda_3d(tela, barra_horizontal, pressionado=True)

    # Setas falsas da barra vertical
    pygame.draw.polygon(
        tela,
        config.COR_PRETO,
        [
            (barra_vertical.centerx, barra_vertical.y + 5),
            (barra_vertical.x + 5, barra_vertical.y + 11),
            (barra_vertical.right - 5, barra_vertical.y + 11)
        ]
    )
    pygame.draw.polygon(
        tela,
        config.COR_PRETO,
        [
            (barra_vertical.centerx, barra_vertical.bottom - 5),
            (barra_vertical.x + 5, barra_vertical.bottom - 11),
            (barra_vertical.right - 5, barra_vertical.bottom - 11)
        ]
    )

    # Setas falsas da barra horizontal
    pygame.draw.polygon(
        tela,
        config.COR_PRETO,
        [
            (barra_horizontal.x + 5, barra_horizontal.centery),
            (barra_horizontal.x + 11, barra_horizontal.y + 5),
            (barra_horizontal.x + 11, barra_horizontal.bottom - 5)
        ]
    )
    pygame.draw.polygon(
        tela,
        config.COR_PRETO,
        [
            (barra_horizontal.right - 5, barra_horizontal.centery),
            (barra_horizontal.right - 11, barra_horizontal.y + 5),
            (barra_horizontal.right - 11, barra_horizontal.bottom - 5)
        ]
    )


def desenhar_paleta_cores(tela, estado):
    """
    Desenha a paleta de cores no rodapé e destaca a cor atual.
    """

    area_paleta = pygame.Rect(0, config.PALETA_Y - 4, config.LARGURA, config.PALETA_ALTURA + 8)
    pygame.draw.rect(tela, config.COR_JANELA, area_paleta)
    pygame.draw.line(tela, config.COR_BOTAO_BORDA_CLARA, area_paleta.topleft, area_paleta.topright)

    # Caixa de cor atual, no estilo do Paint antigo
    caixa_cor = pygame.Rect(config.PALETA_X, config.PALETA_Y + 5, 42, 32)
    pygame.draw.rect(tela, config.COR_JANELA, caixa_cor)
    desenhar_borda_rebaixada(tela, caixa_cor)

    cor_fundo_rect = pygame.Rect(caixa_cor.x + 18, caixa_cor.y + 6, 16, 16)
    cor_atual_rect = pygame.Rect(caixa_cor.x + 8, caixa_cor.y + 14, 16, 16)

    pygame.draw.rect(tela, estado["cor_fundo"], cor_fundo_rect)
    pygame.draw.rect(tela, config.COR_PRETO, cor_fundo_rect, 1)

    pygame.draw.rect(tela, estado["cor_atual"], cor_atual_rect)
    pygame.draw.rect(tela, config.COR_PRETO, cor_atual_rect, 1)

    for botao_cor in criar_botoes_cores():
        retangulo = botao_cor["retangulo"]
        cor = botao_cor["cor"]

        pygame.draw.rect(tela, cor, retangulo)
        pygame.draw.rect(tela, config.COR_PRETO, retangulo, 1)

        if tuple(estado["cor_atual"][:3]) == cor:
            destaque = retangulo.inflate(4, 4)
            pygame.draw.rect(tela, config.COR_PRETO, destaque, 1)
            pygame.draw.rect(tela, config.COR_BRANCO, destaque.inflate(-2, -2), 1)


def desenhar_barra_status(tela):
    """
    Desenha a barra de status inferior com coordenadas do mouse.
    """

    area_status = pygame.Rect(0, config.STATUS_Y, config.LARGURA, config.STATUS_ALTURA)
    pygame.draw.rect(tela, config.COR_JANELA, area_status)
    pygame.draw.line(tela, config.COR_BOTAO_BORDA_CLARA, area_status.topleft, area_status.topright)

    fonte = fonte_classica(12)
    texto_ajuda = fonte.render("For Help, click Help Topics on the Help Menu.", True, config.COR_PRETO)
    tela.blit(texto_ajuda, (6, config.STATUS_Y + 5))

    mouse_x, mouse_y = pygame.mouse.get_pos()
    if (
        config.CANVAS_X <= mouse_x < config.CANVAS_X + config.CANVAS_LARGURA and
        config.CANVAS_Y <= mouse_y < config.CANVAS_Y + config.CANVAS_ALTURA
    ):
        coordenadas = f"{mouse_x - config.CANVAS_X},{mouse_y - config.CANVAS_Y}"
    else:
        coordenadas = ""

    caixa_coord = pygame.Rect(config.LARGURA - 176, config.STATUS_Y + 2, 78, config.STATUS_ALTURA - 4)
    caixa_tamanho = pygame.Rect(config.LARGURA - 96, config.STATUS_Y + 2, 88, config.STATUS_ALTURA - 4)

    desenhar_borda_rebaixada(tela, caixa_coord)
    desenhar_borda_rebaixada(tela, caixa_tamanho)

    texto_coord = fonte.render(coordenadas, True, config.COR_PRETO)
    texto_tamanho = fonte.render(f"{config.CANVAS_LARGURA}x{config.CANVAS_ALTURA}", True, config.COR_PRETO)

    tela.blit(texto_coord, (caixa_coord.x + 5, caixa_coord.y + 4))
    tela.blit(texto_tamanho, (caixa_tamanho.x + 5, caixa_tamanho.y + 4))

ALTURA_BARRA_JANELA = 24


def obter_rect_barra_janela(tela):
    largura = tela.get_width()
    return pygame.Rect(0, 0, largura, ALTURA_BARRA_JANELA)


def obter_rect_botao_minimizar(tela):
    largura = tela.get_width()
    return pygame.Rect(largura - 64, 3, 18, 18)


def obter_rect_botao_maximizar(tela):
    largura = tela.get_width()
    return pygame.Rect(largura - 43, 3, 18, 18)


def obter_rect_botao_fechar(tela):
    largura = tela.get_width()
    return pygame.Rect(largura - 22, 3, 18, 18)


def desenhar_botao_janela_win98(tela, rect, tipo, pressionado=False, desativado=False):
    # Corpo cinza do botão
    pygame.draw.rect(tela, (192, 192, 192), rect)

    if pressionado:
        # Efeito afundado
        pygame.draw.line(tela, (64, 64, 64), rect.topleft, rect.topright)
        pygame.draw.line(tela, (64, 64, 64), rect.topleft, rect.bottomleft)

        pygame.draw.line(tela, (255, 255, 255), rect.bottomleft, rect.bottomright)
        pygame.draw.line(tela, (255, 255, 255), rect.topright, rect.bottomright)
    else:
        # Efeito normal elevado
        pygame.draw.line(tela, (255, 255, 255), rect.topleft, rect.topright)
        pygame.draw.line(tela, (255, 255, 255), rect.topleft, rect.bottomleft)

        pygame.draw.line(tela, (64, 64, 64), rect.bottomleft, rect.bottomright)
        pygame.draw.line(tela, (64, 64, 64), rect.topright, rect.bottomright)

    # Borda interna
    pygame.draw.rect(tela, (128, 128, 128), rect, 1)

    deslocamento = 1 if pressionado else 0

    if tipo == "fechar":
        desenhar_icone_fechar_win98(tela, rect, deslocamento, desativado)

    elif tipo == "minimizar":
        desenhar_icone_minimizar_win98(tela, rect, deslocamento, desativado)

    elif tipo == "maximizar":
        desenhar_icone_maximizar_win98(tela, rect, deslocamento, desativado)


def desenhar_icone_fechar_win98(tela, rect, deslocamento=0, desativado=False):
    x = rect.x + deslocamento
    y = rect.y + deslocamento

    cor = (128, 128, 128) if desativado else (0, 0, 0)

    pygame.draw.line(tela, cor, (x + 5, y + 5), (x + 12, y + 12), 2)
    pygame.draw.line(tela, cor, (x + 12, y + 5), (x + 5, y + 12), 2)


def desenhar_icone_minimizar_win98(tela, rect, deslocamento=0, desativado=False):
    x = rect.x + deslocamento
    y = rect.y + deslocamento

    cor = (128, 128, 128) if desativado else (0, 0, 0)

    pygame.draw.rect(tela, cor, (x + 4, y + 13, 9, 2))


def desenhar_icone_maximizar_win98(tela, rect, deslocamento=0, desativado=False):
    x = rect.x + deslocamento
    y = rect.y + deslocamento

    cor = (128, 128, 128) if desativado else (0, 0, 0)

    # Ícone de maximizar estilo Windows 98
    pygame.draw.rect(tela, cor, (x + 4, y + 4, 10, 10), 1)
    pygame.draw.line(tela, cor, (x + 5, y + 6), (x + 13, y + 6), 1)


def desenhar_barra_superior(tela, estado):
    largura = tela.get_width()

    rect_minimizar = obter_rect_botao_minimizar(tela)
    rect_maximizar = obter_rect_botao_maximizar(tela)
    rect_fechar = obter_rect_botao_fechar(tela)

    fonte_titulo = pygame.font.SysFont("Tahoma", 13, bold=True)

    # Barra azul superior estilo Windows 98
    pygame.draw.rect(tela, (0, 0, 128), (0, 0, largura, ALTURA_BARRA_JANELA))

    # Linha de brilho no topo
    pygame.draw.line(tela, (32, 32, 180), (0, 0), (largura, 0))

    # Ícone do Paint no canto esquerdo
    icone_paint = carregar_imagem(config.ICONE[0]["imagem"])
    if icone_paint is not None:
        tela.blit(icone_paint, (4, 4))

    # Título
    texto_titulo = fonte_titulo.render("untitled - Paint", True, (255, 255, 255))
    tela.blit(texto_titulo, (10 + icone_paint.get_width(), 3))
    

    botao_pressionado = estado.get("botao_janela_pressionado")

    # Botão minimizar
    desenhar_botao_janela_win98(
        tela,
        rect_minimizar,
        "minimizar",
        pressionado=botao_pressionado == "minimizar"
    )

    # Botão maximizar desativado
    desenhar_botao_janela_win98(
        tela,
        rect_maximizar,
        "maximizar",
        pressionado=False,
        desativado=True
    )

    # Botão fechar
    desenhar_botao_janela_win98(
        tela,
        rect_fechar,
        "fechar",
        pressionado=botao_pressionado == "fechar"
    )

def obter_botoes_espessura():
    """
    Retorna os botões de espessura alinhados 2 por 2,
    na parte superior do painel.
    """

    painel = obter_rect_painel_opcoes()

    valores = [1, 2, 4, 6]
    botoes = []

    largura_botao = 20
    altura_botao = 14
    espacamento_x = 4
    espacamento_y = 3

    x_inicial = painel.x + 4
    y_inicial = painel.y + 20

    for indice, valor in enumerate(valores):
        coluna = indice % 2
        linha = indice // 2

        rect = pygame.Rect(
            x_inicial + coluna * (largura_botao + espacamento_x),
            y_inicial + linha * (altura_botao + espacamento_y),
            largura_botao,
            altura_botao
        )

        botoes.append({
            "rect": rect,
            "valor": valor
        })

    return botoes

def obter_botoes_preenchido():
    """
    Retorna os botões de preenchimento abaixo dos botões de espessura.
    False = apenas contorno
    True = preenchido
    """

    painel = obter_rect_painel_opcoes()

    largura_botao = 20
    altura_botao = 14
    espacamento_x = 4

    x_inicial = painel.x + 4
    y_inicial = painel.y + 68

    botoes = [
        {
            "rect": pygame.Rect(
                x_inicial,
                y_inicial,
                largura_botao,
                altura_botao
            ),
            "valor": False
        },
        {
            "rect": pygame.Rect(
                x_inicial + largura_botao + espacamento_x,
                y_inicial,
                largura_botao,
                altura_botao
            ),
            "valor": True
        }
    ]

    return botoes

def desenhar_icone_preenchido(tela, rect, preenchido):
    """
    Desenha o ícone de contorno ou preenchido dentro do botão.
    """

    icone = pygame.Rect(
        rect.x + 5,
        rect.y + 3,
        rect.width - 10,
        rect.height - 6
    )

    if preenchido:
        pygame.draw.rect(tela, config.COR_TEXTO, icone)
    else:
        pygame.draw.rect(tela, config.COR_TEXTO, icone, 1)


def desenhar_interface_classica(tela, estado):
    """
    Desenha todos os elementos visuais que simulam o Paint clássico.
    """

    desenhar_menu(tela)
    desenhar_area_ferramentas(tela)
    desenhar_botoes_ferramentas(tela, estado)
    desenhar_painel_opcoes_ferramenta(tela, estado)
    desenhar_moldura_canvas(tela)
    desenhar_paleta_cores(tela, estado)
    desenhar_barra_status(tela)
    desenhar_barra_superior(tela, estado)
    

