import pygame
import random
import sys

pygame.init()

# Legenda da matriz do mapa:
# '#' = Parede
# '.' = Pastilha (+10 pontos)
# 'o' = Pastilha especial (+50 pontos e deixa o fantasma azul/comível)
# ' ' = Caminho vazio / Túnel lateral
# 'G' = Posição inicial do Fantasma
# 'P' = Posição inicial do Pac-Man (também onde a comidinha bônus aparece)

MAPA_INICIAL = [
    "#################################",
    "# . . . . # . . . . # . . . . . #",
    "# ### ### # ### ### # ### ### ###",
    "# # . . . . . . . . . . . . . o #",
    "# # ### ### ### ### ### ### ### #",
    "# . . # . . # . . . . # . . # . #",
    "##### # ### # ####### # ### # ###",
    "      . . . . . #G# . . . . .    ",
    "##### # ### ### ### ### ### # ###",
    "# . . # . . # . . . . # . . # . #",
    "# # ### ### # ####### # ### ### #",
    "# # . . . . . . .P. . . . . . . #",
    "# ### ### ### ### ### ### ### # #",
    "# . . . . # . . . . # . . . . o #",
    "#################################"
]

# Paletas de cores por fase: (Fundo, Parede/Pastilha, Pastilha Especial)
PALETAS_FASES = [
    ((0, 68, 170), (218, 185, 92), (120, 220, 120)),    # Fase 1: Azul e Amarelo (Original)
    ((15, 15, 35), (45, 140, 255), (255, 180, 50)),     # Fase 2: Preto e Azul Arcade
    ((40, 10, 60), (235, 95, 165), (120, 255, 210)),    # Fase 3: Roxo Escuro e Rosa Neon
    ((10, 55, 45), (110, 230, 140), (255, 230, 90)),    # Fase 4: Verde Floresta
    ((75, 15, 15), (245, 155, 65), (110, 220, 255)),    # Fase 5: Vinho e Laranja
    ((25, 25, 25), (225, 225, 225), (255, 80, 80)),     # Fase 6: Grafite e Branco
]

TAMANHO_BLOCO = 24
LINHAS = len(MAPA_INICIAL)
COLUNAS = len(MAPA_INICIAL[0])

LARGURA = COLUNAS * TAMANHO_BLOCO
ALTURA = LINHAS * TAMANHO_BLOCO + 44

VERDE_BARRA = (115, 195, 115)
PRETO = (0, 0, 0)
CIANO_FANTASMA = (130, 230, 190)
AZUL_VULNERAVEL = (70, 120, 255)
AMARELO_PACMAN = (240, 230, 140)
VERMELHO_BONUS = (235, 65, 65)
VERDE_FOLHA = (80, 210, 90)

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Pac-Man Clássico - Loop Infinito")
fonte = pygame.font.SysFont("courier", 20, bold=True)
fonte_grande = pygame.font.SysFont("courier", 34, bold=True)


def obter_cores_fase(fase):
    indice = (fase - 1) % len(PALETAS_FASES)
    return PALETAS_FASES[indice]


def iniciar_mapa():
    mapa = [list(linha) for linha in MAPA_INICIAL]
    pac_l, pac_c = 11, 17
    fant_l, fant_c = 7, 17

    for l in range(LINHAS):
        for c in range(COLUNAS):
            if mapa[l][c] == "P":
                pac_l, pac_c = l, c
                mapa[l][c] = " "
            elif mapa[l][c] == "G":
                fant_l, fant_c = l, c
                mapa[l][c] = " "

    return mapa, pac_l, pac_c, fant_l, fant_c


def pode_mover(mapa, l, c, eh_fantasma=False):
    if l == 7 and (c < 0 or c >= COLUNAS):
        return True
    if 0 <= l < LINHAS and 0 <= c < COLUNAS:
        # Permite o fantasma sair da caixa central pelo teto (linha 6, coluna 17)
        if eh_fantasma and l == 6 and c == 17:
            return True
        return mapa[l][c] != "#"
    return False


def mover_fantasma(mapa, fant_l, fant_c, fant_dir, pac_l, pac_c, vulneravel):
    # Se estiver dentro da caixa central (7, 17), sobe para sair
    if fant_l == 7 and fant_c == 17:
        return 6, 17, (-1, 0)
    if fant_l == 6 and fant_c == 17:
        return 5, 17, (-1, 0)

    direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    oposto = (-fant_dir[0], -fant_dir[1])
    validas = []

    for dl, dc in direcoes:
        if (dl, dc) == oposto:
            continue
        if pode_mover(mapa, fant_l + dl, fant_c + dc, eh_fantasma=True):
            validas.append((dl, dc))

    if not validas:
        if pode_mover(mapa, fant_l + oposto[0], fant_c + oposto[1], eh_fantasma=True):
            validas.append(oposto)
        else:
            return fant_l, fant_c, fant_dir

    # Escolhe direção: foge se vulnerável, persegue se normal (com toque aleatório)
    if random.random() < 0.25:
        escolha = random.choice(validas)
    else:
        def distancia(d):
            nl, nc = fant_l + d[0], fant_c + d[1]
            return abs(nl - pac_l) + abs(nc - pac_c)

        escolha = max(validas, key=distancia) if vulneravel else min(validas, key=distancia)

    nl = fant_l + escolha[0]
    nc = fant_c + escolha[1]

    if nc < 0:
        nc = COLUNAS - 1
    elif nc >= COLUNAS:
        nc = 0

    return nl, nc, escolha


def desenhar_tudo(mapa, pac_l, pac_c, fant_l, fant_c, pontos, fase, vidas, bonus_ativo, bonus_pos, vulneravel_timer, game_over):
    cor_fundo, cor_parede, cor_especial = obter_cores_fase(fase)
    tela.fill(cor_fundo)

    for l in range(LINHAS):
        for c in range(COLUNAS):
            x = c * TAMANHO_BLOCO
            y = l * TAMANHO_BLOCO
            celula = mapa[l][c]

            if celula == "#":
                pygame.draw.rect(tela, cor_parede, (x, y, TAMANHO_BLOCO, TAMANHO_BLOCO))
            elif celula == ".":
                pygame.draw.rect(
                    tela,
                    cor_parede,
                    (x + 4, y + TAMANHO_BLOCO // 2 - 2, TAMANHO_BLOCO - 8, 4),
                )
            elif celula == "o":
                pygame.draw.rect(
                    tela,
                    cor_especial,
                    (x + 4, y + 4, TAMANHO_BLOCO - 8, TAMANHO_BLOCO - 8),
                )

    # Desenha a comidinha ponto extra (cereja retrô) quando ativa
    if bonus_ativo:
        bx = bonus_pos[1] * TAMANHO_BLOCO + TAMANHO_BLOCO // 2
        by = bonus_pos[0] * TAMANHO_BLOCO + TAMANHO_BLOCO // 2
        pygame.draw.circle(tela, VERMELHO_BONUS, (bx - 4, by + 3), 5)
        pygame.draw.circle(tela, VERMELHO_BONUS, (bx + 4, by + 4), 5)
        pygame.draw.line(tela, VERDE_FOLHA, (bx - 4, by - 2), (bx + 1, by - 8), 2)
        pygame.draw.line(tela, VERDE_FOLHA, (bx + 4, by - 1), (bx + 1, by - 8), 2)

    # Desenha o Fantasma (azul piscando quando vulnerável)
    fx = fant_c * TAMANHO_BLOCO
    fy = fant_l * TAMANHO_BLOCO
    cor_fant = AZUL_VULNERAVEL if vulneravel_timer > 0 else CIANO_FANTASMA
    pygame.draw.rect(
        tela,
        cor_fant,
        (fx + 3, fy + 3, TAMANHO_BLOCO - 6, TAMANHO_BLOCO - 6),
        border_top_left_radius=8,
        border_top_right_radius=8,
    )

    # Desenha o Pac-Man
    px = pac_c * TAMANHO_BLOCO + TAMANHO_BLOCO // 2
    py = pac_l * TAMANHO_BLOCO + TAMANHO_BLOCO // 2
    pygame.draw.circle(tela, AMARELO_PACMAN, (px, py), TAMANHO_BLOCO // 2 - 2)

    # Barra verde inferior com Pontos, Vidas e Fase
    barra_y = LINHAS * TAMANHO_BLOCO
    pygame.draw.rect(tela, PRETO, (0, barra_y, LARGURA, 6))
    pygame.draw.rect(tela, VERDE_BARRA, (0, barra_y + 6, LARGURA, 38))

    texto_pontos = fonte.render(f"PONTOS:{pontos}", True, PRETO)
    texto_vidas = fonte.render(f"VIDAS:{vidas}", True, PRETO)
    texto_fase = fonte.render(f"FASE:{fase}", True, PRETO)

    tela.blit(texto_pontos, (12, barra_y + 13))
    tela.blit(texto_vidas, (LARGURA // 2 - 55, barra_y + 13))
    tela.blit(texto_fase, (LARGURA - 115, barra_y + 13))

    if game_over:
        overlay = pygame.Surface((LARGURA, ALTURA))
        overlay.set_alpha(180)
        overlay.fill(PRETO)
        tela.blit(overlay, (0, 0))
        msg1 = fonte_grande.render("FIM DE JOGO", True, AMARELO_PACMAN)
        msg2 = fonte.render("Pressione ESPACO para jogar de novo", True, (255, 255, 255))
        tela.blit(msg1, (LARGURA // 2 - msg1.get_width() // 2, ALTURA // 2 - 35))
        tela.blit(msg2, (LARGURA // 2 - msg2.get_width() // 2, ALTURA // 2 + 10))


def main():
    clock = pygame.time.Clock()
    mapa, pac_l, pac_c, fant_l, fant_c = iniciar_mapa()
    pos_inicial_pac = (pac_l, pac_c)
    pos_inicial_fant = (fant_l, fant_c)

    dir_l, dir_c = 0, 0
    prox_l, prox_c = 0, 0
    fant_dir = (-1, 0)

    pontos = 0
    proximo_marco_vida = 10000
    vidas = 4
    fase = 1
    game_over = False

    # Controle da comidinha ponto extra
    pastilhas_comidas = 0
    bonus_ativo = False
    bonus_timer = 0
    bonus_pos = (11, 17)

    vulneravel_timer = 0
    contador_frames = 0

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if game_over and evento.key == pygame.K_SPACE:
                    mapa, pac_l, pac_c, fant_l, fant_c = iniciar_mapa()
                    dir_l, dir_c = 0, 0
                    prox_l, prox_c = 0, 0
                    pontos = 0
                    proximo_marco_vida = 10000
                    vidas = 4
                    fase = 1
                    pastilhas_comidas = 0
                    bonus_ativo = False
                    vulneravel_timer = 0
                    game_over = False
                elif not game_over:
                    if evento.key == pygame.K_UP:
                        prox_l, prox_c = -1, 0
                    elif evento.key == pygame.K_DOWN:
                        prox_l, prox_c = 1, 0
                    elif evento.key == pygame.K_LEFT:
                        prox_l, prox_c = 0, -1
                    elif evento.key == pygame.K_RIGHT:
                        prox_l, prox_c = 0, 1

        if not game_over:
            contador_frames += 1
            if contador_frames >= 4:
                contador_frames = 0

                if vulneravel_timer > 0:
                    vulneravel_timer -= 1

                if bonus_ativo:
                    bonus_timer -= 1
                    if bonus_timer <= 0:
                        bonus_ativo = False

                # Move Pac-Man
                if pode_mover(mapa, pac_l + prox_l, pac_c + prox_c):
                    dir_l, dir_c = prox_l, prox_c

                if pode_mover(mapa, pac_l + dir_l, pac_c + dir_c):
                    pac_l += dir_l
                    pac_c += dir_c

                    if pac_c < 0:
