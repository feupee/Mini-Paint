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
BOTAO_X_INICIAL = 10
BOTAO_Y = 10
BOTAO_LARGURA = 90
BOTAO_ALTURA = 50
BOTAO_ESPACAMENTO = 8

# Tamanho da imagem dentro do botão
BOTAO_IMAGEM_TAMANHO = 40

# Cores dos botões
COR_BOTAO = (220, 220, 220)
COR_BOTAO_HOVER = (200, 200, 200)
COR_BOTAO_CLICADO = (180, 180, 180)
COR_BOTAO_ATIVO = (160, 200, 255)

# Cores da borda e do texto
COR_BOTAO_BORDA = (0, 0, 0)
COR_BOTAO_TEXTO = (0, 0, 0)