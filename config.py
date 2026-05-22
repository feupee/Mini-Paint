# Largura da janela do programa
LARGURA = 800

# Altura da janela do programa
ALTURA = 600

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
MENU_ALTURA = 24
MENU_OPCOES = ["File", "Edit", "View", "Image", "Colors", "Help"]

# Barra lateral de ferramentas
BARRA_FERRAMENTAS_X = 4
BARRA_FERRAMENTAS_Y = MENU_ALTURA + 4
BARRA_FERRAMENTAS_LARGURA = 58

# Barras falsas de rolagem, apenas visuais
SCROLLBAR_TAMANHO = 16

# Barra de status inferior
STATUS_ALTURA = 22
STATUS_Y = ALTURA - STATUS_ALTURA

# Paleta de cores inferior
PALETA_X = 8
PALETA_ALTURA = 44
PALETA_Y = STATUS_Y - PALETA_ALTURA - 2
COR_TAMANHO = 18
COR_ESPACAMENTO = 2

# Área do canvas dentro da janela
CANVAS_X = BARRA_FERRAMENTAS_X + BARRA_FERRAMENTAS_LARGURA + 8
CANVAS_Y = MENU_ALTURA + 8
CANVAS_LARGURA = LARGURA - CANVAS_X - 28
CANVAS_ALTURA = PALETA_Y - CANVAS_Y - SCROLLBAR_TAMANHO - 12


# Lista com as 6 ferramentas do programa
# O campo "imagem" pode receber o caminho de uma imagem PNG, JPG etc.
# Se a imagem não existir, o botão mostra o texto da ferramenta.
FERRAMENTAS = [
    {
        "nome": "linha",
        "rotulo": "Linha",
        "imagem": "img/linha.png"
    },
    {
        "nome": "lapis",
        "rotulo": "Lapis",
        "imagem": "img/lapis.png"
    },
    {
        "nome": "borracha",
        "rotulo": "Borracha",
        "imagem": "img/borracha.png"
    },
    {
        "nome": "retangulo",
        "rotulo": "Retângulo",
        "imagem": "img/retangulo.png"
    },
    {
        "nome": "circulo",
        "rotulo": "Círculo",
        "imagem": "img/circulo.png"
    },
    {
        "nome": "preenchimento",
        "rotulo": "Preencher",
        "imagem": "img/balde.png"
    }
]


# Configurações visuais dos botões
BOTAO_X_INICIAL = BARRA_FERRAMENTAS_X + 4
BOTAO_Y = BARRA_FERRAMENTAS_Y + 4
BOTAO_LARGURA = 24
BOTAO_ALTURA = 24
BOTAO_ESPACAMENTO = 2
BOTAO_COLUNAS = 2

# Tamanho da imagem dentro do botão
BOTAO_IMAGEM_TAMANHO = 18

# Cores dos botões
COR_BARRA = COR_JANELA
COR_BOTAO = (212, 208, 200)
COR_BOTAO_HOVER = (230, 230, 230)
COR_BOTAO_CLICADO = (160, 160, 160)
COR_BOTAO_ATIVO = COR_BRANCO

COR_BOTAO_BORDA_CLARA = COR_BRANCO
COR_BOTAO_BORDA_ESCURA = COR_CINZA_ESCURO

# Cores da borda e do texto
COR_BOTAO_BORDA = COR_PRETO
COR_BOTAO_TEXTO = COR_PRETO

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
