import pygame
import sys
import time

pygame.init()

# ================= CONFIGURAÇÕES =================
LARGURA, ALTURA = 900, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo de Geografia")

clock = pygame.time.Clock()

# ================= CORES =================
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

# ================= FONTES =================
fonte = pygame.font.SysFont("arial", 26)
fonte_titulo = pygame.font.SysFont("arial", 40)

# ================= ESTADOS =================
MENU = 0
MODOS = 1
QUIZ = 2
RESULTADO = 3
estado = MENU

# ================= CONTROLE =================
modo = ""
indice = 0
imagem_resultado = None

# ================= TEMPO =================
TEMPO_MAX = 10
inicio_tempo = 0

# ================= FUNDOS =================
fundo_menu = pygame.image.load("jogo_pygame/FUNDO DO JOGO.png")
fundo_menu = pygame.transform.scale(fundo_menu, (LARGURA, ALTURA))

fundo_quiz = pygame.image.load("jogo_pygame/FUNDO DO JOGO 2.png")
fundo_quiz = pygame.transform.scale(fundo_quiz, (LARGURA, ALTURA))

# ================= IMAGENS RESULTADO =================
img_acerto = pygame.image.load("jogo_pygame/ACERTOU.png")
img_erro = pygame.image.load("jogo_pygame/ERROU.png")

img_acerto = pygame.transform.scale(img_acerto, (400, 200))
img_erro = pygame.transform.scale(img_erro, (400, 200))

# ================= PERGUNTAS =================
perguntas = {
    "Países": [
        ("Qual país tem a bandeira verde e amarela?",
         ["A - Brasil", "B - Argentina", "C - Portugal"], "A"),
        ("Qual país tem a bandeira azul, branca e celeste?",
         ["A - Chile", "B - Argentina", "C - Uruguai"], "B"),
        ("Qual país é europeu e fala português?",
         ["A - Espanha", "B - Itália", "C - Portugal"], "C"),
    ],

    "Municípios do RN": [
        ("Qual é a capital do Rio Grande do Norte?",
         ["A - Mossoró", "B - Natal", "C - Caicó"], "B"),
        ("Qual município é conhecido como Cidade do Sol?",
         ["A - Natal", "B - Currais Novos", "C - Pau dos Ferros"], "A"),
        ("Qual município fica no Seridó?",
         ["A - Macau", "B - Caicó", "C - Touros"], "B"),
    ],

    "Estados Brasileiros": [
        ("Qual estado é conhecido como SP?",
         ["A - São Paulo", "B - Bahia", "C - Paraná"], "A"),
        ("Qual estado tem a cidade do Cristo Redentor?",
         ["A - Espírito Santo", "B - Rio de Janeiro", "C - Sergipe"], "B"),
        ("Qual estado tem minas e queijo famoso?",
         ["A - Goiás", "B - Minas Gerais", "C - Tocantins"], "B"),
    ]
}

# ================= CLASSE BOTÃO =================
class Botao(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, texto):
        super().__init__()
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        self.image.fill((255, 255, 255, 220))
        pygame.draw.rect(self.image, PRETO, self.image.get_rect(), 3)

        txt = fonte.render(texto, True, PRETO)
        self.image.blit(
            txt,
            (w // 2 - txt.get_width() // 2,
             h // 2 - txt.get_height() // 2)
        )

        self.rect = self.image.get_rect(topleft=(x, y))
        self.texto = texto

# ================= GRUPOS =================
botoes_menu = pygame.sprite.Group()
botoes_modos = pygame.sprite.Group()
botoes_opcoes = pygame.sprite.Group()

# ================= BOTÕES MENU =================
btn_jogar = Botao(350, 260, 200, 55, "JOGAR")
botoes_menu.add(btn_jogar)

# ================= BOTÕES MODOS =================
btn_paises = Botao(300, 200, 300, 50, "PAÍSES")
btn_municipios = Botao(300, 270, 300, 50, "MUNICÍPIOS DO RN")
btn_estados = Botao(300, 340, 300, 50, "ESTADOS BRASILEIROS")

botoes_modos.add(btn_paises, btn_municipios, btn_estados)

# ================= FUNÇÕES =================
def carregar_pergunta():
    botoes_opcoes.empty()
    pergunta_texto, opcoes, _ = perguntas[modo][indice]

    for i, opcao in enumerate(opcoes):
        botoes_opcoes.add(Botao(300, 350 + i * 45, 300, 35, opcao))

def tela_menu():
    tela.blit(fundo_menu, (0, 0))
    titulo = fonte_titulo.render("JOGO DE GEOGRAFIA", True, PRETO)
    tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 120))
    botoes_menu.draw(tela)

def tela_modos():
    tela.blit(fundo_menu, (0, 0))
    titulo = fonte_titulo.render("TELA PARA ESCOLHER OS MODOS:", True, PRETO)
    tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 120))
    botoes_modos.draw(tela)

def tela_quiz():
    tela.blit(fundo_quiz, (0, 0))
    pergunta_texto, _, _ = perguntas[modo][indice]
    pergunta_render = fonte.render(pergunta_texto, True, BRANCO)
    tela.blit(
        pergunta_render,
        (LARGURA // 2 - pergunta_render.get_width() // 2, 150)
    )

    botoes_opcoes.draw(tela)

    tempo = TEMPO_MAX - int(time.time() - inicio_tempo)
    tela.blit(fonte.render(f"Tempo: {tempo}s", True, BRANCO), (20, 20))

def tela_resultado():
    tela.blit(fundo_quiz, (0, 0))
    if imagem_resultado:
        tela.blit(
            imagem_resultado,
            (LARGURA // 2 - imagem_resultado.get_width() // 2, 220)
        )

# ================= LOOP PRINCIPAL =================
rodando = True
while rodando:
    clock.tick(60)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if evento.type == pygame.MOUSEBUTTONDOWN:
            pos = evento.pos

            if estado == MENU:
                if btn_jogar.rect.collidepoint(pos):
                    estado = MODOS

            elif estado == MODOS:
                if btn_paises.rect.collidepoint(pos):
                    modo = "Países"
                elif btn_municipios.rect.collidepoint(pos):
                    modo = "Municípios do RN"
                elif btn_estados.rect.collidepoint(pos):
                    modo = "Estados Brasileiros"

                if modo:
                    indice = 0
                    inicio_tempo = time.time()
                    carregar_pergunta()
                    estado = QUIZ

            elif estado == QUIZ:
                resposta = perguntas[modo][indice][2]
                for botao in botoes_opcoes:
                    if botao.rect.collidepoint(pos):
                        letra = botao.texto[0]
                        imagem_resultado = img_acerto if letra == resposta else img_erro
                        estado = RESULTADO

            elif estado == RESULTADO:
                indice += 1
                if indice < len(perguntas[modo]):
                    imagem_resultado = None
                    inicio_tempo = time.time()
                    carregar_pergunta()
                    estado = QUIZ
                else:
                    estado = MENU
                    modo = ""

    if estado == QUIZ and TEMPO_MAX - int(time.time() - inicio_tempo) <= 0:
        imagem_resultado = img_erro
        estado = RESULTADO

    if estado == MENU:
        tela_menu()
    elif estado == MODOS:
        tela_modos()
    elif estado == QUIZ:
        tela_quiz()
    elif estado == RESULTADO:
        tela_resultado()

    pygame.display.update()
