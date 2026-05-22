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


ALTURA_BARRA = 90


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
BOTAO_X_INICIAL = 8
BOTAO_Y = 28
BOTAO_LARGURA = 36
BOTAO_ALTURA = 36
BOTAO_ESPACAMENTO = 4

# Tamanho da imagem dentro do botão
BOTAO_IMAGEM_TAMANHO = 50

# Cores dos botões
COR_BARRA = (192, 192, 192)
COR_BOTAO = (212, 208, 200)
COR_BOTAO_HOVER = (230, 230, 230)
COR_BOTAO_CLICADO = (160, 160, 160)
COR_BOTAO_ATIVO = (255, 255, 255)

COR_BOTAO_BORDA_CLARA = (255, 255, 255)
COR_BOTAO_BORDA_ESCURA = (64, 64, 64)

# Cores da borda e do texto
COR_BOTAO_BORDA = (0, 0, 0)
COR_BOTAO_TEXTO = (0, 0, 0)