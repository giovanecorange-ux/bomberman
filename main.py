import pygame
import random
import sys
import os
import json

pygame.init()
pygame.mixer.init()

# MAPA 100% IDÊNTICO AO VÍDEO - 33 colunas x 15 linhas - portal em cima/embaixo no meio
MAPA_INICIAL_RAW = [
    "################ ################",
    "# . . . . # . . . . # . . . . . #",
    "# ### ### # ### ### # ### ### ###",
    "# # . . . . . . . . . . . . . o #",
    "# # ### ### ### ### ### ### ### #",
    "# . . # . . # . . . . # . . # . #",
    "##### # ### # ####### # ### # ###",
    "##### . . . . . #G# . . . . . #####",
    "##### # ### ### ### ### ### # ###",
    "# . . # . . # . . . . # . . # . #",
    "# # ### ### # ####### # ### ### #",
    "# # . . . . . . .P. . . . . . . #",
    "# ### ### ### ### ### ### ### # #",
    "# . . . . # . . . . # . . . . o #",
    "################ ################",
]
# Garante tudo com 33 colunas
COLUNAS = max(len(r) for r in MAPA_INICIAL_RAW)
MAPA_INICIAL = [r.ljust(COLUNAS)[:COLUNAS] for r in MAPA_INICIAL_RAW]

PALETAS_FASES = [
    ((0, 68, 170), (218, 185, 92), (120, 220, 120)),
    ((15, 15, 35), (45, 140, 255), (255, 180, 50)),
    ((40, 10, 60), (235, 95, 165), (120, 255, 210)),
]

TAMANHO_BLOCO = 24
LINHAS = len(MAPA_INICIAL)
LARGURA = COLUNAS * TAMANHO_BLOCO
ALTURA = LINHAS * TAMANHO_BLOCO + 44

VERDE_BARRA = (115, 195, 115)
PRETO = (0, 0, 0)
CIANO_FANTASMA = (130, 230, 190)
AZUL_VULNERAVEL = (70, 120, 255)
AMARELO_PACMAN = (240, 230, 140)
VERMELHO_BONUS = (235, 65, 65)
VERDE_FOLHA = (80, 210, 90)
ARQ_RECORDE = "recorde_pacman.json"

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Pac-Man Atari - Idêntico ao Vídeo")
fonte = pygame.font.SysFont("courier", 20, bold=True)
fonte_grande = pygame.font.SysFont("courier", 34, bold=True)

def carregar_recorde():
    try:
        if os.path.exists(ARQ_RECORDE):
            with open(ARQ_RECORDE, "r") as f:
                return json.load(f)
    except: pass
    return {"fase": 1, "pontos": 0}

def salvar_recorde(fase, pontos):
    try:
        dados = {"fase": fase, "pontos": pontos}
        if os.path.exists(ARQ_RECORDE):
            try:
                with open(ARQ_RECORDE, "r") as f:
                    antigo = json.load(f)
                    if antigo.get("pontos", 0) >= pontos:
                        return antigo
            except: pass
        with open(ARQ_RECORDE, "w") as f:
            json.dump(dados, f)
        return dados
    except:
        return {"fase": fase, "pontos": pontos}

def obter_cores_fase(fase):
    return PALETAS_FASES[(fase - 1) % len(PALETAS_FASES)]

def iniciar_mapa():
    mapa = [list(linha) for linha in MAPA_INICIAL]
    pac_l, pac_c = 11, 16
    fant_l, fant_c = 7, 16
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
    # Portal em cima/embaixo no meio coluna 16 - igual Atari
    if c == 16 and (l < 0 or l >= LINHAS):
        return True
    if 0 <= l < LINHAS and 0 <= c < COLUNAS:
        if eh_fantasma and l == 6 and c == 16:
            return True
        return mapa[l][c] != "#"
    return False

def mover_fantasma(mapa, fant_l, fant_c, fant_dir, pac_l, pac_c, vulneravel):
    if fant_l == 7 and fant_c == 16:
        return 6, 16, (-1, 0)
    if fant_l == 6 and fant_c == 16:
        return 5, 16, (-1, 0)
    direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    oposto = (-fant_dir[0], -fant_dir[1])
    validas = []
    for dl, dc in direcoes:
        if (dl, dc) == oposto: continue
        if pode_mover(mapa, fant_l + dl, fant_c + dc, eh_fantasma=True):
            validas.append((dl, dc))
    if not validas:
        if pode_mover(mapa, fant_l + oposto[0], fant_c + oposto[1], eh_fantasma=True):
            validas.append(oposto)
        else:
            return fant_l, fant_c, fant_dir
    if random.random() < 0.25:
        escolha = random.choice(validas)
    else:
        def distancia(d):
            nl, nc = fant_l + d[0], fant_c + d[1]
            return abs(nl - pac_l) + abs(nc - pac_c)
        escolha = max(validas, key=distancia) if vulneravel else min(validas, key=distancia)
    nl = fant_l + escolha[0]
    nc = fant_c + escolha[1]
    if nl < 0 and nc == 16: nl = LINHAS - 2
    elif nl >= LINHAS and nc == 16: nl = 1
    if nc < 0: nc = COLUNAS - 1
    elif nc >= COLUNAS: nc = 0
    return nl, nc, escolha

def desenhar_tudo(mapa, pac_l, pac_c, fant_l, fant_c, pontos, fase, vidas, bonus_ativo, bonus_pos, vulneravel_timer, game_over):
    cor_fundo, cor_parede, cor_especial = obter_cores_fase(fase)
    tela.fill(cor_fundo)
    for l in range(LINHAS):
        for c in range(COLUNAS):
            x = c * TAMANHO_BLOCO
            y = l * TAMANHO_BLOCO
            celula = mapa[l][c] if c < len(mapa[l]) else " "
            if celula == "#":
                pygame.draw.rect(tela, cor_parede, (x, y, TAMANHO_BLOCO, TAMANHO_BLOCO))
            elif celula == ".":
                pygame.draw.rect(tela, cor_parede, (x + 4, y + TAMANHO_BLOCO // 2 - 2, TAMANHO_BLOCO - 8, 4))
            elif celula == "o":
                pygame.draw.rect(tela, cor_especial, (x + 4, y + 4, TAMANHO_BLOCO - 8, TAMANHO_BLOCO - 8))
    if bonus_ativo:
        bx = bonus_pos[1] * TAMANHO_BLOCO + TAMANHO_BLOCO // 2
        by = bonus_pos[0] * TAMANHO_BLOCO + TAMANHO_BLOCO // 2
        pygame.draw.circle(tela, VERMELHO_BONUS, (bx - 4, by + 3), 5)
        pygame.draw.circle(tela, VERMELHO_BONUS, (bx + 4, by + 4), 5)
        pygame.draw.line(tela, VERDE_FOLHA, (bx - 4, by - 2), (bx + 1, by - 8), 2)
        pygame.draw.line(tela, VERDE_FOLHA, (bx + 4, by - 1), (bx + 1, by - 8), 2)
    fx = fant_c * TAMANHO_BLOCO
    fy = fant_l * TAMANHO_BLOCO
    cor_fant = AZUL_VULNERAVEL if vulneravel_timer > 0 else CIANO_FANTASMA
    pygame.draw.rect(tela, cor_fant, (fx + 3, fy + 3, TAMANHO_BLOCO - 6, TAMANHO_BLOCO - 6), border_top_left_radius=8, border_top_right_radius=8)
    px = pac_c * TAMANHO_BLOCO + TAMANHO_BLOCO // 2
    py = pac_l * TAMANHO_BLOCO + TAMANHO_BLOCO // 2
    pygame.draw.circle(tela, AMARELO_PACMAN, (px, py), TAMANHO_BLOCO // 2 - 2)
    barra_y = LINHAS * TAMANHO_BLOCO
    pygame.draw.rect(tela, PRETO, (0, barra_y, LARGURA, 6))
    pygame.draw.rect(tela, VERDE_BARRA, (0, barra_y + 6, LARGURA, 38))
    tela.blit(fonte.render(f"PONTOS:{pontos}", True, PRETO), (12, barra_y + 13))
    tela.blit(fonte.render(f"VIDAS:{vidas}", True, PRETO), (LARGURA // 2 - 55, barra_y + 13))
    tela.blit(fonte.render(f"FASE:{fase}", True, PRETO), (LARGURA - 115, barra_y + 13))
    if game_over:
        overlay = pygame.Surface((LARGURA, ALTURA))
        overlay.set_alpha(180)
        overlay.fill(PRETO)
        tela.blit(overlay, (0, 0))
        msg1 = fonte_grande.render("FIM DE JOGO", True, AMARELO_PACMAN)
        msg2 = fonte.render("Pressione ESPACO para jogar de novo", True, (255, 255, 255))
        tela.blit(msg1, (LARGURA // 2 - msg1.get_width() // 2, ALTURA // 2 - 35))
        tela.blit(msg2, (LARGURA // 2 - msg2.get_width() // 2, ALTURA // 2 + 10))

def tela_inicial():
    # Toca nes.mp3 se existir
    try:
        if os.path.exists("nes.mp3"):
            pygame.mixer.music.load("nes.mp3")
            pygame.mixer.music.set_volume(0.7)
            pygame.mixer.music.play(-1)
    except: pass

    rec = carregar_recorde()
    botao = pygame.Rect(LARGURA//2 - 130, ALTURA//2 - 20, 260, 55)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if botao.collidepoint(evento.pos):
                    try: pygame.mixer.music.stop()
                    except: pass
                    return
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                try: pygame.mixer.music.stop()
                except: pass
                return

        tela.fill((5, 10, 120))
        t1 = fonte_grande.render("CORANGE SOFTWARE", True, (100, 200, 255))
        t2 = fonte_grande.render("PACMAN CLASSICO", True, (255, 230, 80))
        if rec["pontos"] > 0:
            t_rec = fonte.render(f"RECORDE: {rec['pontos']} PTS", True, (255,255,150))
        else:
            t_rec = fonte.render("SEM RECORDE - JOGUE!", True, (255,255,150))

        tela.blit(t1, (LARGURA//2 - t1.get_width()//2, 60))
        tela.blit(t2, (LARGURA//2 - t2.get_width()//2, 110))
        tela.blit(t_rec, (LARGURA//2 - t_rec.get_width()//2, 170))

        # Desenho capa
        pygame.draw.circle(tela, AMARELO_PACMAN, (LARGURA//2 - 80, 260), 22)
        for i, cor in enumerate([(235,65,65),(255,150,200),(100,255,255),(255,180,50)]):
            x = LARGURA//2 - 20 + i*45
            pygame.draw.circle(tela, cor, (x, 260), 18)
            pygame.draw.rect(tela, cor, (x-18, 260, 36, 16))

        pygame.draw.rect(tela, (20, 180, 60), botao, border_radius=10)
        txt = fonte_grande.render("INICIAR JOGO", True, (255,255,255))
        tela.blit(txt, (LARGURA//2 - txt.get_width()//2, ALTURA//2 - 10))

        pix = fonte.render("PIX: 51993359782", True, (80,255,120))
        tela.blit(pix, (LARGURA//2 - pix.get_width()//2, ALTURA - 60))

        pygame.display.flip()
        pygame.time.Clock().tick(30)

def main():
    tela_inicial()
    clock = pygame.time.Clock()
    mapa, pac_l, pac_c, fant_l, fant_c = iniciar_mapa()
    pos_inicial_pac = (pac_l, pac_c)
    dir_l, dir_c = 0, 0
    prox_l, prox_c = 0, 0
    fant_dir = (-1, 0)
    pontos = 0
    proximo_marco_vida = 10000
    vidas = 4
    fase = 1
    game_over = False
    bonus_ativo = False
    bonus_timer = 0
    bonus_pos = (11, 16)
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
                    bonus_ativo = False
                    vulneravel_timer = 0
                    game_over = False
                elif not game_over:
                    if evento.key == pygame.K_UP: prox_l, prox_c = -1, 0
                    elif evento.key == pygame.K_DOWN: prox_l, prox_c = 1, 0
                    elif evento.key == pygame.K_LEFT: prox_l, prox_c = 0, -1
                    elif evento.key == pygame.K_RIGHT: prox_l, prox_c = 0, 1

        if not game_over:
            contador_frames += 1
            if contador_frames >= 4:
                contador_frames = 0
                if vulneravel_timer > 0: vulneravel_timer -= 1
                if bonus_ativo:
                    bonus_timer -= 1
                    if bonus_timer <= 0: bonus_ativo = False
                if pode_mover(mapa, pac_l + prox_l, pac_c + prox_c):
                    dir_l, dir_c = prox_l, prox_c
                if pode_mover(mapa, pac_l + dir_l, pac_c + dir_c):
                    pac_l += dir_l
                    pac_c += dir_c
                    if pac_l < 0 and pac_c == 16: pac_l = LINHAS - 2
                    elif pac_l >= LINHAS and pac_c == 16: pac_l = 1
                    if pac_c < 0: pac_c = COLUNAS - 1
                    elif pac_c >= COLUNAS: pac_c = 0
                    cel = mapa[pac_l][pac_c] if 0 <= pac_l < LINHAS and 0 <= pac_c < len(mapa[pac_l]) else " "
                    if cel == ".":
                        mapa[pac_l][pac_c] = " "
                        pontos += 10
                        if pontos % 70 == 0:
                            bonus_ativo = True
                            bonus_timer = 150
                    elif cel == "o":
                        mapa[pac_l][pac_c] = " "
                        pontos += 50
                        vulneravel_timer = 35
                if pontos >= proximo_marco_vida:
                    vidas += 1
                    proximo_marco_vida += 10000
                if pac_l == bonus_pos[0] and pac_c == bonus_pos[1] and bonus_ativo:
                    pontos += 100
                    bonus_ativo = False
                fant_l, fant_c, fant_dir = mover_fantasma(mapa, fant_l, fant_c, fant_dir, pac_l, pac_c, vulneravel_timer > 0)
                if fant_l == pac_l and fant_c == pac_c:
                    if vulneravel_timer > 0:
                        fant_l, fant_c = 7, 16
                        pontos += 200
                    else:
                        vidas -= 1
                        salvar_recorde(fase, pontos)
                        if vidas <= 0:
                            game_over = True
                        else:
                            pac_l, pac_c = pos_inicial_pac
                            fant_l, fant_c = 7, 16
                            dir_l, dir_c = 0, 0
                            prox_l, prox_c = 0, 0
                if sum(row.count(".") + row.count("o") for row in mapa) == 0:
                    fase += 1
                    salvar_recorde(fase, pontos)
                    mapa, pac_l, pac_c, fant_l, fant_c = iniciar_mapa()
                    bonus_ativo = False
                    vulneravel_timer = 0
        desenhar_tudo(mapa, pac_l, pac_c, fant_l, fant_c, pontos, fase, vidas, bonus_ativo, bonus_pos, vulneravel_timer, game_over)
        pygame.display.flip()
        clock.tick(15)

if __name__ == "__main__":
    main()
