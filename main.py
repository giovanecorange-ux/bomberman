import os, sys, pygame, math, importlib

# CORANGE SISTEMAS - PIX 51993359782
PIX = "51993359782"
BASE = os.path.dirname(os.path.abspath(__file__))

# ANDROID: tem que iniciar o video antes do som
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
try:
    pygame.mixer.init(frequency=44100, size=-16, channels=2)
except:
    pass

try:
    if os.path.exists(os.path.join(BASE, "icon.png")):
        icone = pygame.image.load(os.path.join(BASE, "icon.png"))
        pygame.display.set_icon(icone)
except:
    pass

def beep(f=800, ms=80, vol=0.5):
    try:
        sr=44100; n=int(sr*ms/1000); buf=bytearray()
        for i in range(n):
            s=int(vol*32767*math.sin(2*math.pi*f*i/sr)*(1-i/n*0.5))
            buf+=s.to_bytes(2,'little',signed=True)*2
        return pygame.mixer.Sound(buffer=bytes(buf))
    except:
        return None

snd_click = beep(900, 100, 0.6)

def ler_recorde(arq):
    try:
        caminho = os.path.join(BASE, arq)
        if os.path.exists(caminho):
            with open(caminho, "r") as f:
                return int(f.read().strip())
    except:
        pass
    return 0

def criar_tela_menu():
    return pygame.display.set_mode((0,0), pygame.FULLSCREEN)

screen = criar_tela_menu()
LARGURA, ALTURA = screen.get_size()
pygame.display.set_caption(f"CORANGE SISTEMAS - 3 JOGOS - PIX {PIX}")

# CORREÇÃO ANDROID: usa fonte padrão, não Arial
def texto(txt, tamanho, cor, bold=True):
    try:
        f = pygame.font.Font(None, tamanho)
        # tira emoji que o Android não desenha e crasha
        txt = txt.replace("🐍","").replace("🧱","").replace("💣","").strip()
        return f.render(txt, True, cor)
    except:
        f = pygame.font.Font(None, 30)
        return f.render("ERRO FONTE", True, cor)

def rodar(nome_arquivo):
    if snd_click:
        try:
            snd_click.play()
            pygame.time.delay(120)
        except:
            pass
    nome = nome_arquivo.replace(".py", "")
    print(f"Abrindo {nome}...")
    try:
        if nome in sys.modules:
            del sys.modules[nome]
        importlib.import_module(nome)
    except Exception as e:
        print(f"Erro: {e}")
        pygame.time.delay(1000)
    global screen, LARGURA, ALTURA
    try:
        pygame.mixer.init(frequency=44100, size=-16, channels=2)
    except:
        pass
    screen = criar_tela_menu()
    LARGURA, ALTURA = screen.get_size()

while True:
    rec_cobra = ler_recorde("recorde_cobrinha.txt")
    rec_tetris = ler_recorde("recorde_tetris.txt")
    rec_bomber = ler_recorde("recorde_bomber.txt")
    if rec_bomber==0:
        rec_bomber = ler_recorde("recorde.txt")

    screen.fill((10,10,20))
    t = texto("CORANGE SISTEMAS", int(ALTURA*0.045), (255,204,0))
    screen.blit(t, (LARGURA//2 - t.get_width()//2, ALTURA*0.05))
    t = texto("3 JOGOS", int(ALTURA*0.03), (255,255,255))
    screen.blit(t, (LARGURA//2 - t.get_width()//2, ALTURA*0.11))
    t = texto(f"PIX {PIX}", int(ALTURA*0.032), (0,255,136))
    screen.blit(t, (LARGURA//2 - t.get_width()//2, ALTURA*0.155))

    botoes = []
    dados = [
        (f"COBRINHA - REC {rec_cobra}", (0,255,136), "cobrinha.py"),
        (f"TETRIS - REC {rec_tetris}", (0,204,255), "tetris.py"),
        (f"BOMBERMAN - REC {rec_bomber}", (255,204,0), "bomberman.py"),
    ]
    for i, (txt, cor, arq) in enumerate(dados):
        y = ALTURA*0.24 + i*ALTURA*0.18
        rect = pygame.Rect(LARGURA*0.07, y, LARGURA*0.86, ALTURA*0.12)
        pygame.draw.rect(screen, cor, rect, border_radius=20)
        pygame.draw.rect(screen, (255,255,255), rect, 2, border_radius=20)
        lbl = texto(txt, int(ALTURA*0.024), (0,0,0))
        screen.blit(lbl, (rect.centerx - lbl.get_width()//2, rect.centery - lbl.get_height()//2))
        botoes.append((rect, arq))

    t = texto("Toque para jogar - Som beep interno", int(ALTURA*0.02), (150,150,150), bold=False)
    screen.blit(t, (LARGURA//2 - t.get_width()//2, ALTURA*0.82))
    t = texto(f"Corange Sistemas - PIX {PIX}", int(ALTURA*0.018), (0,255,136), bold=False)
    screen.blit(t, (LARGURA//2 - t.get_width()//2, ALTURA*0.86))

    pygame.display.flip()

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            sys.exit()
        if ev.type == pygame.MOUSEBUTTONDOWN:
            pos = ev.pos
            for rect, arq in botoes:
                if rect.collidepoint(pos):
                    rodar(arq)
        if ev.type == pygame.FINGERDOWN:
            pos = (ev.x*LARGURA, ev.y*ALTURA)
            for rect, arq in botoes:
                if rect.collidepoint(pos):
                    rodar(arq)
