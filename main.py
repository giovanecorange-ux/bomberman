import pygame, random, os
pygame.init()
# SEM MIXER - SEM SOM - ANDROID
# CORANGE SISTEMAS - PIX 51993359782

LARG, ALT = 676, 572
TILE = 52
GRID_W, GRID_H = 13, 11
HUD = 30

tela = pygame.display.set_mode((LARG, ALT))
pygame.display.set_caption("CORANGE - BOMBERMAN - PIX 51993359782")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 18, bold=True)
font_big = pygame.font.SysFont("Arial", 32, bold=True)
font_small = pygame.font.SysFont("Arial", 13, bold=True)
PIX = "51993359782"
ARQ = "recorde.txt"

def carregar():
    try:
        if os.path.exists(ARQ):
            with open(ARQ,"r") as f: return int(f.read().strip())
    except: pass
    return 0
def salvar(v):
    try:
        with open(ARQ,"w") as f: f.write(str(v))
    except: pass

recorde = carregar()

def mostrar_venceu(pontos):
    tela.fill((10,10,20))
    t = font_big.render("Você Venceu!!!", True, (255,204,0))
    tela.blit(t, (LARG//2 - t.get_width()//2, 150))
    t2 = font.render(f"Pontos: {pontos}  Recorde: {recorde}", True, (255,255,255))
    tela.blit(t2, (LARG//2 - t2.get_width()//2, 220))
    t3 = font.render(f"PIX {PIX}", True, (0,255,100))
    tela.blit(t3, (LARG//2 - t3.get_width()//2, 260))
    t4 = font.render("Voltando para o Menu...", True, (200,200,200))
    tela.blit(t4, (LARG//2 - t4.get_width()//2, 300))
    pygame.display.flip()
    pygame.time.delay(3000)

def jogar():
    global recorde
    fase = 1
    vidas = 3
    pontos = 0
    while True: # loop das 6 fases
        # monta fase
        grid = []
        for y in range(GRID_H):
            linha=[]
            for x in range(GRID_W):
                if x==0 or y==0 or x==GRID_W-1 or y==GRID_H-1 or (x%2==0 and y%2==0):
                    linha.append(1)
                elif (x<3 and y<3) or (x>GRID_W-4 and y<3) or (x<3 and y>GRID_H-4) or (x>GRID_W-4 and y>GRID_H-4):
                    linha.append(0)
                elif random.random()<0.30:
                    linha.append(2)
                else:
                    linha.append(0)
            grid.append(linha)
        player = [1,1]
        qtd = 3 + (fase-1) # fase 1=3, fase 6=8
        posicoes = [[GRID_W-2,1],[GRID_W-2,GRID_H-2],[1,GRID_H-2],[GRID_W-2,GRID_H//2],[1,GRID_H//2],[GRID_W//2,GRID_H-2],[GRID_W-2,3],[1,3]]
        inimigos = [[posicoes[i][0], posicoes[i][1], i%3, 0] for i in range(min(qtd, len(posicoes)))]
        bombas=[]; fogos=[]; moedas=[]; invencivel=0; game_over=False
        # cores por fase
        cores_chao = [((62,194,50),(75,224,58)),((217,194,214),(200,169,197)),((46,196,176),(59,214,194)),((62,194,50),(107,232,90)),((26,138,232),(42,154,255)),((58,196,160),(74,216,176))][fase-1]
        while True:
            for e in pygame.event.get():
                if e.type==pygame.QUIT: return None
                if e.type==pygame.KEYDOWN and not game_over:
                    x,y=player; nx,ny=x,y
                    if e.key==pygame.K_w or e.key==pygame.K_UP: ny-=1
                    elif e.key==pygame.K_s or e.key==pygame.K_DOWN: ny+=1
                    elif e.key==pygame.K_a or e.key==pygame.K_LEFT: nx-=1
                    elif e.key==pygame.K_d or e.key==pygame.K_RIGHT: nx+=1
                    elif e.key==pygame.K_SPACE:
                        if len(bombas)<2 and not any(b[0]==x and b[1]==y for b in bombas):
                            bombas.append([x,y,28])
                    elif e.key==pygame.K_r:
                        grid=None; break
                    if 0<=nx<GRID_W and 0<=ny<GRID_H and grid[ny][nx]==0:
                        if not any(en[0]==nx and en[1]==ny for en in inimigos):
                            player=[nx,ny]
                            for m in moedas[:]:
                                if m[0]==nx and m[1]==ny:
                                    pontos+=100; moedas.remove(m)
            if grid is None: break
            if invencivel>0: invencivel-=1
            for b in bombas[:]:
                b[2]-=1
                if b[2]<=0:
                    bombas.remove(b)
                    x,y,_=b; pos=[[x,y]]
                    for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                        for i in range(1,3):
                            nx,ny=x+dx*i,y+dy*i
                            if not (0<=nx<GRID_W and 0<=ny<GRID_H): break
                            if grid[ny][nx]==1: break
                            pos.append([nx,ny])
                            if grid[ny][nx]==2:
                                grid[ny][nx]=0
                                if random.random()<0.40:
                                    moedas.append([nx,ny, 1 if random.random()<0.30 else 0])
                                break
                    for fx,fy in pos:
                        fogos.append([fx,fy,12])
                        if fx==player[0] and fy==player[1] and invencivel==0:
                            vidas-=1
                            if vidas<=0: game_over=True
                            else: player=[1,1]; invencivel=25
                        for en in inimigos[:]:
                            if en[0]==fx and en[1]==fy: inimigos.remove(en); pontos+=50
            for f in fogos[:]:
                f[2]-=1
                if f[2]<=0: fogos.remove(f)
            # inimigos
            if not game_over:
                for en in inimigos:
                    en[3]-=1
                    if en[3]>0: continue
                    en[3]=9 if en[2]==0 else 6 if en[2]==1 else 3
                    x,y,tipo,_=en; px,py=player
                    dx,dy=0,0
                    if tipo==2 and random.random()<0.7:
                        if abs(px-x)>abs(py-y): dx=1 if px>x else -1
                        else: dy=1 if py>y else -1
                    else:
                        dx,dy=random.choice([(1,0),(-1,0),(0,1),(0,-1)])
                    nx,ny=x+dx,y+dy
                    if 0<=nx<GRID_W and 0<=ny<GRID_H and grid[ny][nx]==0 and not any(b[0]==nx and b[1]==ny for b in bombas):
                        en[0],en[1]=nx,ny
                    if en[0]==player[0] and en[1]==player[1] and invencivel==0:
                        vidas-=1
                        if vidas<=0: game_over=True
                        else: player=[1,1]; invencivel=25
            # desenha
            tela.fill((0,0,0))
            tela.blit(font.render(f"VIDAS: {vidas}  FASE: {fase}/6  PONTOS: {pontos}  REC: {recorde}", True, (255,255,255)), (10,5))
            for y in range(GRID_H):
                for x in range(GRID_W):
                    px,py=x*TILE, y*TILE+HUD
                    cor=cores_chao[0] if (x+y)%2==0 else cores_chao[1]
                    pygame.draw.rect(tela, cor, (px,py,TILE,TILE))
                    t=grid[y][x]
                    if t==1: pygame.draw.rect(tela, (160,160,160), (px,py,TILE,TILE))
                    elif t==2: pygame.draw.rect(tela, (200,200,200), (px+3,py+3,TILE-6,TILE-6))
            for mx,my,tipo in moedas:
                pygame.draw.circle(tela, (255,204,0), (mx*TILE+TILE//2, my*TILE+HUD+TILE//2), 12)
            for fx,fy,_ in fogos:
                pygame.draw.rect(tela, (255,102,0), (fx*TILE+2, fy*TILE+HUD+2, TILE-4, TILE-4))
            for bx,by,_ in bombas:
                pygame.draw.circle(tela, (106,58,208), (bx*TILE+TILE//2, by*TILE+HUD+TILE//2), 14)
            for en in inimigos:
                c=[(255,122,192),(77,166,255),(255,59,59)][en[2]]
                pygame.draw.circle(tela, c, (en[0]*TILE+TILE//2, en[1]*TILE+HUD+TILE//2), 16)
            if not (invencivel>0 and invencivel%4<2):
                pygame.draw.circle(tela, (42,124,255), (player[0]*TILE+TILE//2, player[1]*TILE+HUD+TILE//2), 16)
            if game_over:
                tela.blit(font_big.render("GAME OVER", True, (255,50,50)), (LARG//2-100, 200))
                tela.blit(font.render("R = REINICIAR  Q = MENU", True, (255,255,255)), (LARG//2-110, 250))
            elif len(inimigos)==0:
                if fase==6:
                    if pontos>recorde: recorde=pontos; salvar(recorde)
                    mostrar_venceu(pontos)
                    return pontos # VOLTA PRO MENU
                else:
                    tela.blit(font_big.render(f"FASE {fase} COMPLETA!", True, (255,255,0)), (LARG//2-150, 200))
                    tela.blit(font.render("R = PROXIMA FASE", True, (255,255,255)), (LARG//2-100, 250))
            pygame.display.flip()
            clock.tick(30)
            # espera R para proxima / reiniciar
            if game_over or len(inimigos)==0:
                esperando=True
                while esperando:
                    for e in pygame.event.get():
                        if e.type==pygame.QUIT: return None
                        if e.type==pygame.KEYDOWN:
                            if e.key==pygame.K_r: esperando=False
                            if e.key==pygame.K_q: return pontos
                    clock.tick(30)
                if game_over:
                    if vidas<=0:
                        vidas=3; pontos=0; fase=1
                    break
                else:
                    if fase<6: fase+=1; break
                    else: break

while True:
    s=jogar()
    if s is None: break
    break
