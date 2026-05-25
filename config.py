# Largura fixa do canvas
CANVAS_LARGURA = 800

# Altura fixa do canvas
CANVAS_ALTURA = 600

# Cor de fundo do canvas
COR_FUNDO = (255, 255, 255)

# Cor usada para desenhar
COR_DESENHO = (0, 0, 0)

# Ferramenta inicial do programa
FERRAMENTA_PADRAO = "linha"


# -----------------------------------------------------------------------------
# Layout visual estilo Windows 95/98 / Paint clássico
# -----------------------------------------------------------------------------

# Altura da antiga barra superior. Mantida por compatibilidade com partes antigas
# do código, mas agora o layout usa as constantes específicas abaixo.
ALTURA_BARRA = 90

# Cores base do visual clássico
COR_JANELA = (192, 192, 192)
COR_BRANCO = (255, 255, 255)
COR_PRETO = (0, 0, 0)
COR_CINZA_CLARO = (223, 223, 223)
COR_CINZA_MEDIO = (128, 128, 128)
COR_CINZA_ESCURO = (64, 64, 64)
COR_AZUL_SELECAO = (0, 0, 128)

# Barra de menu superior
BARRA_TITULO_ALTURA = 28
MENU_ALTURA = 26
MENU_OPCOES = ["File", "Edit", "View", "Image", "Colors", "Help"]

# Espaçamentos gerais do layout.
MARGEM_EXTERNA = 4
MARGEM_ENTRE_AREAS = 3
CONTEUDO_Y = BARRA_TITULO_ALTURA + MENU_ALTURA + MARGEM_ENTRE_AREAS - 5

# Barra lateral de ferramentas.
# A largura foi aumentada para permitir que o painel de opções mostre
# espessura, tamanho de fonte e preenchimento sem invadir o canvas.
BARRA_FERRAMENTAS_X = MARGEM_EXTERNA
BARRA_FERRAMENTAS_Y = CONTEUDO_Y
BARRA_FERRAMENTAS_LARGURA = 72

# Barras falsas de rolagem, apenas visuais
SCROLLBAR_TAMANHO = 16

# Barra de status inferior
STATUS_ALTURA = 20

# Paleta de cores inferior
PALETA_X = 8
PALETA_ALTURA = 55
COR_TAMANHO = 20
COR_ESPACAMENTO = 4

# Área do canvas dentro da janela.
# O tamanho do canvas continua fixo em 800x600; apenas a posição muda.
CANVAS_X = BARRA_FERRAMENTAS_X + BARRA_FERRAMENTAS_LARGURA + MARGEM_ENTRE_AREAS
CANVAS_Y = CONTEUDO_Y

# Largura da janela do programa
LARGURA = CANVAS_X + CANVAS_LARGURA + SCROLLBAR_TAMANHO + 12

# Altura da janela do programa
ALTURA = CANVAS_Y + CANVAS_ALTURA + SCROLLBAR_TAMANHO + 12 + PALETA_ALTURA + 2 + STATUS_ALTURA

STATUS_Y = ALTURA - STATUS_ALTURA
PALETA_Y = STATUS_Y - PALETA_ALTURA - 2


# Lista com as 6 ferramentas do programa
# O campo "imagem" pode receber o caminho de uma imagem PNG, JPG etc.
# Se a imagem não existir, o botão mostra o texto da ferramenta.
FERRAMENTAS = [
    {
        "nome": "linha",
        "rotulo": "Linha",
        "imagem": "img/linha.png",
        "cursor": "img/cursor/linha.png",
        "hotspot": (15, 15)
    },
    {
        "nome": "lapis",
        "rotulo": "Lapis",
        "imagem": "img/lapis.png",
        "cursor": "img/cursor/lapis.png",
        "hotspot": (12, 24)
    },
    {                       
        "nome": "borracha",
        "rotulo": "Borracha",
        "imagem": "img/borracha.png",
        "cursor": "img/cursor/borracha.png",
        "hotspot": (5, 5)
    },
    {
        "nome": "retangulo",
        "rotulo": "Retângulo",
        "imagem": "img/retangulo.png",
        "cursor": "img/cursor/retangulo.png",
        "hotspot": (21, 21)
    },
    {
        "nome": "circulo",
        "rotulo": "Círculo",
        "imagem": "img/circulo.png",
        "cursor": "img/cursor/circulo.png",
        "hotspot": (15, 15)
    },
    {
        "nome": "conta-gotas",
        "rotulo": "Conta-Gotas",
        "imagem": "img/conta-gotas.png",
        "cursor": "img/cursor/conta-gotas.png",
        "hotspot": (9, 23)
    },
    {
        "nome": "preenchimento",
        "rotulo": "Preencher",
        "imagem": "img/balde.png",
        "cursor": "img/cursor/balde.png",
        "hotspot": (8, 21)
    },
    {
        "nome": "texto",
        "rotulo": "Texto",
        "imagem": "img/texto.png",
        "cursor": "img/cursor/texto.png",
        "hotspot": (8, 8)
    }
]

ICONE = [
    {
        "nome": "paint",
        "imagem": "img/icone.png"
    }
]

#Menu
BARRA_TITULO_ALTURA = 23
MENU_ALTURA = 26

# Configurações visuais dos botões
BOTAO_X_INICIAL = BARRA_FERRAMENTAS_X + 7
BOTAO_Y = BARRA_FERRAMENTAS_Y + 6
BOTAO_LARGURA = 25
BOTAO_ALTURA = 25
BOTAO_ESPACAMENTO = 4
BOTAO_COLUNAS = 2

# Tamanho da imagem dentro do botão
BOTAO_IMAGEM_TAMANHO = 15

# Cores dos botões
COR_BARRA = COR_JANELA
COR_BOTAO = (212, 208, 200)
COR_BOTAO_HOVER = (230, 230, 230)
COR_BOTAO_CLICADO = (160, 160, 160)
COR_BOTAO_ATIVO = COR_BRANCO
COR_BOTAO_PRESSIONADO = (180, 180, 180)

COR_BOTAO_BORDA_CLARA = COR_BRANCO
COR_BOTAO_BORDA_ESCURA = COR_CINZA_ESCURO

# Cores da borda e do texto
COR_BOTAO_BORDA = COR_PRETO
COR_BOTAO_TEXTO = COR_PRETO
COR_BORDA = (128, 128, 128)
COR_TEXTO = (0, 0, 0)

# Paleta no estilo do Paint clássico
CORES_PALETA = [
    (0, 0, 0),
    (128, 128, 128),
    (128, 0, 0),
    (128, 128, 0),
    (0, 128, 0),
    (0, 128, 128),
    (0, 0, 128),
    (128, 0, 128),
    (255, 255, 255),
    (192, 192, 192),
    (255, 0, 0),
    (255, 255, 0),
    (0, 255, 0),
    (0, 255, 255),
    (0, 0, 255),
    (255, 0, 255),
    (128, 64, 0),
    (255, 128, 64),
    (0, 64, 128),
    (0, 128, 255),
]
