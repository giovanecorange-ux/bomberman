import os, json, random, math, wave, struct
from kivy.app import App
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse, Line, Rectangle, Triangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.widget import Widget

ARQ_RECORDE = "recorde_pacman.json"
def salvar_recorde(fase, pontos):
    try:
        dados = {"fase": fase, "pontos": pontos}
        if os.path.exists(ARQ_RECORDE):
            try:
                with open(ARQ_RECORDE, "r") as f:
                    antigo = json.load(f)
                    if antigo.get("pontos", 0) >= pontos: return antigo
            except: pass
        with open(ARQ_RECORDE, "w") as f: json.dump(dados, f)
        return dados
    except: return {"fase": fase, "pontos": pontos}

def carregar_recorde():
    try:
        if os.path.exists(ARQ_RECORDE):
            with open(ARQ_RECORDE, "r") as f: return json.load(f)
    except: pass
    return {"fase": 1, "pontos": 0}

def criar_bip(nome, freq, duracao=0.2, volume=0.5):
    try:
        if os.path.exists(nome): return
        framerate = 44100; nframes = int(framerate * duracao)
        with wave.open(nome, 'w') as wav:
            wav.setnchannels(1); wav.setsampwidth(2); wav.setframerate(framerate)
            for i in range(nframes):
                v = volume * (1 - i / nframes)
                sample = int(v * 32767 * math.sin(2 * math.pi * freq * i / framerate))
                wav.writeframes(struct.pack('<h', sample))
    except: pass

_sons_cache = {}
def tocar_bip(nome):
    try:
        if not os.path.exists(nome): return
        if nome not in _sons_cache:
            s = SoundLoader.load(nome)
            _sons_cache[nome] = s
        s = _sons_cache.get(nome)
        if s: s.play()
    except: pass

def _mapa_de_texto(linhas):
    return [[1 if ch=='#' else 2 if ch=='P' else 0 for ch in l] for l in linhas]

# MAPA 100% IDÊNTICO AO VÍDEO ATARI 2600 - 17x21 COM PORTAL EM CIMA/EMBAIXO NO MEIO
FASES_MAPAS_TXT = [[
"######## ########",
"#..............P#",
"#.##.###.###.##.#",
"#.#............#",
"#.#.##.###.##.#.#",
"#.....#.#.....#.#",
"#####.#.#.#.#####",
"#####........####",
"#####.#.#.#.#####",
"#.....#.#.....#.#",
"#.#.#.#####.#.#.#",
"#.#.#.......#.#.#",
"#.#.##.###.##.#.#",
"#.....#.#.....#.#",
"#.###.#.#.###.#.#",
"#.#..........#.#",
"#.#.##.###.##.#.#",
"#...##..#..##...#",
"#.##.##.#.##.##.#",
"#P.............P#",
"######## ########",
]]

FASES_MAPAS = [_mapa_de_texto(m) for m in FASES_MAPAS_TXT] * 5

FASES_SKINS = [
    {"fixo": (0.12, 0.18, 1, 1), "nome": "Atari Azul"},
    {"fixo": (0, 0.85, 0, 1), "nome": "Atari Verde"},
    {"fixo": (1, 1, 0, 1), "nome": "Atari Amarelo"},
    {"fixo": (1, 0.15, 0.15, 1), "nome": "Atari Vermelho"},
    {"fixo": (0.7, 0.2, 1, 1), "nome": "Atari Roxo"},
]

class Bloco(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tipo = 'chao'; self.l = 0; self.c = 0
        self.bind(pos=self._redesenhar, size=self._redesenhar)
    def _redesenhar(self, *args): self.desenhar(self.tipo, None, None)
    def desenhar(self, tipo, cor_fase=None, skin=None, inimigo_tipo='vermelho', casa_set=None, porta=None, parede_set=None):
        self.tipo = tipo; self.canvas.clear()
        x, y = self.pos; w, h = self.size
        if w <= 1 or h <= 1: return
        fixo = skin["fixo"] if skin else (0.2,0.4,1,1)
        with self.canvas:
            Color(0,0,0,1); Rectangle(pos=(x, y), size=(w, h))
            if tipo == 'fixo':
                Color(*fixo); Line(rectangle=(x+1, y+1, w-2, h-2), width=1.6); return
            elif tipo == 'pastilha':
                m = min(w,h); Color(1,1,0.7,1); Ellipse(pos=(x + (w-m*0.28)/2, y + (h-m*0.28)/2), size=(m*0.28, m*0.28)); return
            elif tipo == 'poder':
                m = min(w,h); Color(1,0.9,0.9,1); Ellipse(pos=(x + (w-m*0.65)/2, y + (h-m*0.65)/2), size=(m*0.65, m*0.65)); return
            elif tipo == 'player':
                Color(1,1,0,1); Ellipse(pos=(x + w*0.10, y + h*0.10), size=(w*0.80, h*0.80))
                Color(0,0,0,1); Triangle(points=[x+w*0.55, y+h*0.5, x+w*0.95, y+h*0.70, x+w*0.95, y+h*0.30]); return
            elif tipo == 'assustado':
                Color(0,0,1,1); Ellipse(pos=(x + w*0.10, y + h*0.20), size=(w*0.80, h*0.60)); Rectangle(pos=(x + w*0.10, y + h*0.05), size=(w*0.80, h*0.30))
                Color(1,1,1,1); Ellipse(pos=(x + w*0.24, y + h*0.50), size=(w*0.20, h*0.24)); Ellipse(pos=(x + w*0.56, y + h*0.50), size=(w*0.20, h*0.24)); return
            elif tipo == 'inimigo':
                cores = {'vermelho': (1,0,0,1), 'rosa': (1,0.6,0.8,1), 'ciano': (0,1,1,1), 'laranja': (1,0.6,0,1)}
                c = cores.get(inimigo_tipo, (1,0,0,1))
                Color(*c); Ellipse(pos=(x + w*0.10, y + h*0.20), size=(w*0.80, h*0.60)); Rectangle(pos=(x + w*0.10, y + h*0.05), size=(w*0.80, h*0.30))
                Color(1,1,1,1); Ellipse(pos=(x + w*0.24, y + h*0.50), size=(w*0.20, h*0.24)); Ellipse(pos=(x + w*0.56, y + h*0.50), size=(w*0.20, h*0.24))
                Color(0,0,0,1); Ellipse(pos=(x + w*0.30, y + h*0.54), size=(w*0.09, h*0.14)); Ellipse(pos=(x + w*0.62, y + h*0.54), size=(w*0.09, h*0.14)); return
            elif tipo == 'casinha':
                Color(0,0,0,1); Rectangle(pos=(x, y), size=(w, h))
                Color(*fixo)
                if (self.l-1, self.c) not in (casa_set or set()) and (self.l-1, self.c) != porta: Line(points=[x, y+h, x+w, y+h], width=2.2)
                if (self.l+1, self.c) not in (casa_set or set()): Line(points=[x, y, x+w, y], width=2.2)
                if (self.l, self.c-1) not in (casa_set or set()): Line(points=[x, y, x, y+h], width=2.2)
                if (self.l, self.c+1) not in (casa_set or set()): Line(points=[x+w, y, x+w, y+h], width=2.2)
                return
            elif tipo == 'porta':
                Color(0,0,0,1); Rectangle(pos=(x, y), size=(w, h))
                Color(1,1,1,0.95); Rectangle(pos=(x, y + h*0.38), size=(w, h*0.24)); return

class DesenhoCapa(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self._desenhar, size=self._desenhar)
    def _desenhar(self, *args):
        self.canvas.clear()
        x, y = self.pos; w, h = self.size
        if w <= 10 or h <= 10: return
        lado = min(w / 4.5, h * 0.75)
        espaco = (w - (lado * 4)) / 5.0
        cy = y + (h - lado) / 2.0
        with self.canvas:
            Color(0,0,0,1); Rectangle(pos=(x, y), size=(w, h))
            bx = x + espaco
            Color(1,1,0,1); Ellipse(pos=(bx, cy), size=(lado, lado))
            Color(0,0,0,1); Triangle(points=[bx+lado*0.5, cy+lado*0.5, bx+lado*1.05, cy+lado*0.75, bx+lado*1.05, cy+lado*0.25])
            cores = [(1,0,0,1),(1,0.6,0.8,1),(0,1,1,1),(1,0.6,0,1)]
            for i, cor in enumerate(cores):
                fx = bx + (lado+espaco)*(i+1)
                Color(*cor); Ellipse(pos=(fx, cy+lado*0.2), size=(lado*0.8, lado*0.6)); Rectangle(pos=(fx, cy), size=(lado*0.8, lado*0.3))
                Color(1,1,1,1); Ellipse(pos=(fx+lado*0.15, cy+lado*0.5), size=(lado*0.18, lado*0.2)); Ellipse(pos=(fx+lado*0.45, cy+lado*0.5), size=(lado*0.18, lado*0.2))

class TelaInicial(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.musica = None
        layout = BoxLayout(orientation='vertical', padding=16, spacing=8)
        layout.add_widget(Label(text="CORANGE SOFTWARE", font_size='18sp', color=(0.4, 0.85, 1, 1), bold=True, size_hint_y=0.08))
        layout.add_widget(Label(text="PACMAN CLASSICO", font_size='34sp', color=(1, 0.85, 0.1, 1), bold=True, size_hint_y=0.12))
        self.lbl_recorde = Label(text="", font_size='16sp', color=(1, 1, 0.4, 1), bold=True, size_hint_y=0.08)
        layout.add_widget(self.lbl_recorde)
        layout.add_widget(DesenhoCapa(size_hint_y=0.34))
        btn = Button(text="INICIAR JOGO", font_size='24sp', bold=True, background_color=(0.15, 0.75, 0.25, 1), size_hint_y=0.16)
        btn.bind(on_release=self.ir_para_jogo)
        layout.add_widget(btn)
        layout.add_widget(Label(text="PIX: 51993359782", font_size='16sp', color=(0.3, 1, 0.45, 1), bold=True, size_hint_y=0.08))
        self.add_widget(layout)
    def on_enter(self):
        rec = carregar_recorde()
        if rec["pontos"] > 0: self.lbl_recorde.text = f"RECORDE: {rec['pontos']} PTS"
        else: self.lbl_recorde.text = "SEM RECORDE - JOGUE!"
        Clock.schedule_once(lambda dt: self.tocar_musica(), 0.3)
    def on_leave(self): self.parar_musica()
    def tocar_musica(self):
        try:
            if self.musica: self.musica.stop()
            caminho = "nes.mp3" if os.path.exists("nes.mp3") else None
            if caminho:
                self.musica = SoundLoader.load(caminho)
                if self.musica: 
                    self.musica.loop = True
                    self.musica.play()
        except: pass
    def parar_musica(self):
        try:
            if self.musica: self.musica.stop()
        except: pass
    def ir_para_jogo(self, *args):
        self.parar_musica()
        self.manager.get_screen('jogo').iniciar_fase(1, True)
        self.manager.current = 'jogo'

class BotaoSeta(Button):
    def __init__(self, direcao='cima', **kwargs):
        super().__init__(**kwargs)
        self.direcao = direcao; self.text = ""; self.background_color = (0.15, 0.3, 0.8, 1)
        self.bind(pos=self.desenhar_seta, size=self.desenhar_seta)
    def desenhar_seta(self, *args):
        self.canvas.after.clear()
        x, y = self.pos; w, h = self.size
        cx = x + w/2; cy = y + h/2; tam = min(w, h) * 0.35
        with self.canvas.after:
            Color(1, 1, 1, 1)
            if self.direcao == 'cima': Triangle(points=[cx, cy+tam, cx-tam, cy-tam, cx+tam, cy-tam])
            elif self.direcao == 'baixo': Triangle(points=[cx, cy-tam, cx-tam, cy+tam, cx+tam, cy+tam])
            elif self.direcao == 'esq': Triangle(points=[cx-tam, cy, cx+tam, cy+tam, cx+tam, cy-tam])
            elif self.direcao == 'dir': Triangle(points=[cx+tam, cy, cx-tam, cy+tam, cx-tam, cy-tam])

class TelaJogo(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.LINHAS = 21; self.COLUNAS = 17
        self.fase = 1; self.pontos = 0; self.vidas = 3
        self.proxima_vida_extra = 10000
        self.player = [18, 8]; self.spawn_player = [18, 8]
        self.casa_fantasmas = [(9,7),(9,8),(9,9),(10,7),(10,8),(10,9),(11,7),(11,8),(11,9)]
        self.porta_casinha = (8, 8)
        self.inimigos = []; self.mapa = []; self.blocos = []; self.game_over = False; self._event_inimigo = None
        self._event_andar = None; self._dir_atual = (0, 0); self._dir_desejada = (0, 0)
        self.pastilhas = set(); self.poderes = set(); self.modo_poder = False; self.tempo_poder = None; self.tempo_restante_poder = 0
        root = BoxLayout(orientation='vertical', spacing=2, padding=2)
        topo = BoxLayout(orientation='horizontal', size_hint_y=0.08, padding=[4,2,4,2], spacing=4)
        b_menu = Button(text="MENU", font_size='12sp', bold=True, background_color=(0.3,0.3,0.33,1), size_hint_x=0.18)
        b_menu.bind(on_release=lambda x: self.voltar_menu())
        topo.add_widget(b_menu)
        self.lbl_info = Label(text="VIDAS: 3", font_size='12sp', bold=True, size_hint_x=0.28)
        self.lbl_fase = Label(text="FASE 1", font_size='12sp', bold=True, size_hint_x=0.27)
        self.lbl_pontos = Label(text="0 PTS", font_size='13sp', bold=True, color=(1,1,0,1), size_hint_x=0.27)
        topo.add_widget(self.lbl_info); topo.add_widget(self.lbl_fase); topo.add_widget(self.lbl_pontos)
        root.add_widget(topo)
        self.lbl_recorde_tela = Label(text="", font_size='11sp', color=(0.6,1,0.6,1), bold=True, size_hint_y=0.03)
        root.add_widget(self.lbl_recorde_tela)
        self.grid = GridLayout(cols=self.COLUNAS, rows=self.LINHAS, spacing=0, size_hint_y=0.70)
        root.add_widget(self.grid)
        controles = BoxLayout(orientation='vertical', size_hint_y=0.19, spacing=4, padding=6)
        linha_cima = BoxLayout(orientation='horizontal')
        linha_cima.add_widget(Widget())
        b_cima = BotaoSeta(direcao='cima', size_hint_x=0.34)
        b_cima.bind(on_press=lambda x: self.set_direcao(-1, 0))
        linha_cima.add_widget(b_cima); linha_cima.add_widget(Widget())
        controles.add_widget(linha_cima)
        linha_meio = BoxLayout(orientation='horizontal', spacing=8)
        b_esq = BotaoSeta(direcao='esq'); b_esq.bind(on_press=lambda x: self.set_direcao(0, -1))
        b_baixo = BotaoSeta(direcao='baixo'); b_baixo.bind(on_press=lambda x: self.set_direcao(1, 0))
        b_dir = BotaoSeta(direcao='dir'); b_dir.bind(on_press=lambda x: self.set_direcao(0, 1))
        linha_meio.add_widget(b_esq); linha_meio.add_widget(b_baixo); linha_meio.add_widget(b_dir)
        controles.add_widget(linha_meio)
        root.add_widget(controles)
        self.add_widget(root)
        Window.bind(on_key_down=self.teclado)
    def teclado(self, window, key, *args):
        if self.manager and self.manager.current != 'jogo': return False
        if key == 273: self.set_direcao(-1, 0)
        elif key == 274: self.set_direcao(1, 0)
        elif key == 275: self.set_direcao(0, 1)
        elif key == 276: self.set_direcao(0, -1)
        return True
    def set_direcao(self, dl, dc):
        self._dir_desejada = (dl, dc)
        if self._dir_atual == (0,0): self._dir_atual = (dl, dc)
        if not self._event_andar:
            self._event_andar = Clock.schedule_interval(lambda dt: self.tentar_mover(), 0.09)
    def tentar_mover(self):
        if self.game_over: return
        if self._dir_desejada != (0,0):
            nl = self.player[0] + self._dir_desejada[0]; nc = self.player[1] + self._dir_desejada[1]
            if self.pode_andar(nl, nc, fantasma=False):
                self._dir_atual = self._dir_desejada
                self.mover(self._dir_atual[0], self._dir_atual[1]); return
        if self._dir_atual != (0,0):
            nl = self.player[0] + self._dir_atual[0]; nc = self.player[1] + self._dir_atual[1]
            if self.pode_andar(nl, nc, fantasma=False):
                self.mover(self._dir_atual[0], self._dir_atual[1]); return
    def definir_spawn_e_casinha(self):
        cr, cc = self.LINHAS//2, self.COLUNAS//2
        self.casa_fantasmas = [(cr-1,cc-1),(cr-1,cc),(cr-1,cc+1),(cr,cc-1),(cr,cc),(cr,cc+1),(cr+1,cc-1),(cr+1,cc),(cr+1,cc+1)]
        self.porta_casinha = (cr-2, cc)
        for (r,c) in self.casa_fantasmas:
            if 0 <= r < self.LINHAS and 0 <= c < self.COLUNAS:
                self.mapa[r][c] = 0
        self.mapa[self.porta_casinha[0]][self.porta_casinha[1]] = 0
        self.mapa[cr-3][cc] = 0
        self.spawn_player = [self.LINHAS-3, cc]
        self.mapa[self.spawn_player[0]][self.spawn_player[1]] = 0
        self.mapa[self.spawn_player[0]][self.spawn_player[1]-1] = 0
        self.mapa[self.spawn_player[0]][self.spawn_player[1]+1] = 0
    def iniciar_fase(self, fase, reset_mapa=False):
        self.fase = fase; self.game_over = False; self.modo_poder = False
        self._dir_atual = (0,0); self._dir_desejada = (0,0)
        if fase == 1 and reset_mapa:
            self.vidas = 3; self.pontos = 0; self.proxima_vida_extra = 10000
        if self.tempo_poder: self.tempo_poder.cancel(); self.tempo_poder = None
        if self._event_andar: self._event_andar.cancel(); self._event_andar = None
        idx_mapa = (fase-1) % len(FASES_MAPAS)
        idx_cor = (fase-1) % len(FASES_SKINS)
        self.mapa = [row[:] for row in FASES_MAPAS[idx_mapa]]
        self.skin_atual = FASES_SKINS[idx_cor]
        self.definir_spawn_e_casinha()
        self.player = self.spawn_player[:]
        if reset_mapa:
            self.pastilhas = set(); self.poderes = set()
            casa_set = set(self.casa_fantasmas)
            for l in range(self.LINHAS):
                for c in range(self.COLUNAS):
                    if (l,c) in casa_set: continue
                    if (l,c) == self.porta_casinha: continue
                    if [l,c] == self.spawn_player: continue
                    if self.mapa[l][c] == 0:
                        self.pastilhas.add((l,c))
                    elif self.mapa[l][c] == 2: self.poderes.add((l,c))
            if tuple(self.spawn_player) in self.pastilhas: self.pastilhas.remove(tuple(self.spawn_player))
        self.inimigos = []
        tipos = ['vermelho','rosa','ciano','laranja']
        for i, (l,c) in enumerate(self.casa_fantasmas[:4]):
            self.inimigos.append([l, c, random.choice([(1,0),(-1,0),(0,1),(0,-1)]), tipos[i], 0])
        self.grid.clear_widgets(); self.blocos = []
        for l in range(self.LINHAS):
            linha_blocos = []
            for c in range(self.COLUNAS):
                b = Bloco(); b.l = l; b.c = c
                self.grid.add_widget(b); linha_blocos.append(b)
            self.blocos.append(linha_blocos)
        self.atualizar_info(); self.desenhar_mapa()
        if self._event_inimigo: self._event_inimigo.cancel()
        self._event_inimigo = Clock.schedule_interval(lambda dt: self.atualizar_inimigos(), 0.35)
        self._event_andar = Clock.schedule_interval(lambda dt: self.tentar_mover(), 0.09)
    def reiniciar_apos_morte(self):
        self.player = self.spawn_player[:]
        self._dir_atual = (0,0); self._dir_desejada = (0,0)
        self.inimigos = []
        tipos = ['vermelho','rosa','ciano','laranja']
        for i, (l,c) in enumerate(self.casa_fantasmas[:4]):
            self.inimigos.append([l, c, random.choice([(1,0),(-1,0),(0,1),(0,-1)]), tipos[i], 0])
        self.modo_poder = False
        if self.tempo_poder: self.tempo_poder.cancel(); self.tempo_poder = None
        self.atualizar_info(); self.desenhar_mapa()
    def atualizar_info(self):
        nome = self.skin_atual["nome"]
        modo = " PODER!" if self.modo_poder else ""
        self.lbl_info.text = f"VIDAS: {self.vidas}{modo}"
        self.lbl_fase.text = f"FASE {self.fase} {nome}"
        self.lbl_pontos.text = f"{self.pontos} PTS"
        rec = carregar_recorde()
        if rec["pontos"] > 0: self.lbl_recorde_tela.text = f"RECORDE: {rec['pontos']} PTS | EXTRA em {self.proxima_vida_extra}"
        else: self.lbl_recorde_tela.text = f"VIDA EXTRA em {self.proxima_vida_extra} PTS"
    def desenhar_mapa(self):
        skin = self.skin_atual
        casa_set = set(self.casa_fantasmas)
        porta = getattr(self, 'porta_casinha', None)
        parede_set = set((l,c) for l in range(self.LINHAS) for c in range(self.COLUNAS) if self.mapa[l][c]==1)
        for l in range(self.LINHAS):
            for c in range(self.COLUNAS):
                tipo = 'chao'
                if self.mapa[l][c] == 1: tipo = 'fixo'
                elif (l,c) == porta: tipo = 'porta'
                elif (l,c) in casa_set: tipo = 'casinha'
                elif (l,c) in self.poderes: tipo = 'poder'
                elif (l,c) in self.pastilhas: tipo = 'pastilha'
                if [l, c] == self.player: tipo = 'player'
                self.blocos[l][c].desenhar(tipo, None, skin, 'vermelho', casa_set, porta, parede_set)
        for e in self.inimigos:
            self.blocos[e[0]][e[1]].desenhar('assustado' if self.modo_poder else 'inimigo', None, skin, e[3], casa_set, porta, parede_set)
    def pode_andar(self, l, c, fantasma=False):
        # Portal Atari no meio em cima/embaixo
        if c == 8 and (l < 0 or l >= self.LINHAS):
            return True
        if l < 0 or l >= self.LINHAS: return False
        if c < 0 or c >= self.COLUNAS: return False
        if self.mapa[l][c] == 1: return False
        if not fantasma:
            if (l,c) in set(self.casa_fantasmas): return False
            if (l,c) == self.porta_casinha: return False
        return True
    def ativar_poder(self):
        self.modo_poder = True; self.tempo_restante_poder = 6
        if self.tempo_poder: self.tempo_poder.cancel()
        self.tempo_poder = Clock.schedule_interval(lambda dt: self.contar_poder(), 1)
    def contar_poder(self):
        self.tempo_restante_poder -= 1
        if self.tempo_restante_poder <= 0: self.fim_poder()
    def checar_vida_extra(self):
        while self.pontos >= self.proxima_vida_extra:
            self.vidas += 1
            tocar_bip('bip_venceu.wav')
            self.proxima_vida_extra += 10000
    def mover(self, dl, dc):
        if self.game_over: return
        nl = self.player[0] + dl; nc = self.player[1] + dc
        # Portal
        if nc == 8 and nl < 0:
            nl = self.LINHAS - 1
        elif nc == 8 and nl >= self.LINHAS:
            nl = 0
        if not self.pode_andar(nl, nc, fantasma=False): return
        self.player = [nl, nc]
        if (nl, nc) in self.pastilhas:
            self.pastilhas.remove((nl, nc)); self.pontos += 10; tocar_bip('bip_venceu.wav')
        if (nl, nc) in self.poderes:
            self.poderes.remove((nl, nc)); self.pontos += 50
            self.ativar_poder(); tocar_bip('bip_venceu.wav')
        self.checar_vida_extra()
        cr, cc = self.LINHAS//2, self.COLUNAS//2
        for e in self.inimigos[:]:
            if e[0] == nl and e[1] == nc:
                if self.modo_poder:
                    e[0], e[1] = cr, cc; e[4] = 3; self.pontos += 200; tocar_bip('bip_bicho.wav')
                else: self.perdeu(); return
        self.atualizar_info()
        if len(self.pastilhas) == 0 and len(self.poderes) == 0: self.venceu_fase(); return
        self.desenhar_mapa()
    def atualizar_inimigos(self):
        if self.game_over or self.manager.current != 'jogo': return
        cr, cc = self.LINHAS//2, self.COLUNAS//2
        for e in self.inimigos[:]:
            if e[4] > 0:
                e[4] -= 1
                if e[4] == 0: e[0], e[1] = self.porta_casinha
                continue
            if (e[0], e[1]) in set(self.casa_fantasmas):
                if e[0] > self.porta_casinha[0]: e[0] -= 1; continue
                elif e[1] != self.porta_casinha[1]: e[1] += 1 if self.porta_casinha[1] > e[1] else -1; continue
                else: e[0] -= 1; continue
            possiveis = []
            for dl, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                if e[2] == (-dl, -dc) and len(possiveis) > 0: continue
                nl, nc = e[0] + dl, e[1] + dc
                # Portal fantasma
                if nc == 8 and nl < 0: nl = self.LINHAS - 1
                elif nc == 8 and nl >= self.LINHAS: nl = 0
                if self.pode_andar(nl, nc, fantasma=True):
                    possiveis.append((dl, dc, nl, nc))
            if possiveis:
                if self.modo_poder:
                    possiveis.sort(key=lambda x: - (abs(x[2]-self.player[0]) + abs(x[3]-self.player[1])))
                else:
                    if random.random() < 0.6:
                        possiveis.sort(key=lambda x: abs(x[2]-self.player[0]) + abs(x[3]-self.player[1]))
                    else:
                        random.shuffle(possiveis)
                melhor = possiveis[0]
                e[0], e[1] = melhor[2], melhor[3]; e[2] = (melhor[0], melhor[1])
            if [e[0], e[1]] == self.player:
                if self.modo_poder:
                    e[0], e[1] = cr, cc; e[4] = 3; self.pontos += 200; tocar_bip('bip_bicho.wav'); self.checar_vida_extra(); self.atualizar_info(); return
                else: self.perdeu(); return
        self.desenhar_mapa()
    def fim_poder(self):
        self.modo_poder = False; self.tempo_restante_poder = 0
        if self.tempo_poder: self.tempo_poder.cancel(); self.tempo_poder = None
        self.atualizar_info(); self.desenhar_mapa()
    def perdeu(self):
        if self.game_over: return
        tocar_bip('bip_morreu.wav'); self.vidas -= 1; salvar_recorde(self.fase, self.pontos)
        if self.tempo_poder: self.tempo_poder.cancel(); self.tempo_poder = None; self.modo_poder = False
        if self._event_andar: self._event_andar.cancel(); self._event_andar = None
        if self.vidas <= 0:
            self.game_over = True
            if self._event_inimigo: self._event_inimigo.cancel()
            self.lbl_pontos.text = f"FIM: {self.pontos} PTS"
            Clock.schedule_once(lambda dt: self.voltar_menu(), 2.0)
        else: self.reiniciar_apos_morte(); self._event_andar = Clock.schedule_interval(lambda dt: self.tentar_mover(), 0.09)
    def venceu_fase(self):
        if self.game_over: return
        self.game_over = True; tocar_bip('bip_venceu.wav'); self.pontos += 500; salvar_recorde(self.fase, self.pontos)
        self.checar_vida_extra()
        if self._event_inimigo: self._event_inimigo.cancel()
        if self._event_andar: self._event_andar.cancel(); self._event_andar = None
        if self.tempo_poder: self.tempo_poder.cancel(); self.tempo_poder = None
        self.lbl_pontos.text = f"FASE OK! {self.pontos} PTS"
        Clock.schedule_once(lambda dt: self.iniciar_fase(self.fase + 1, True), 1.5)
    def voltar_menu(self):
        if self._event_inimigo: self._event_inimigo.cancel()
        if self._event_andar: self._event_andar.cancel(); self._event_andar = None
        if self.tempo_poder: self.tempo_poder.cancel(); self.tempo_poder = None
        self.modo_poder = False
        self.manager.current = 'inicio'

class PacmanApp(App):
    def on_start(self):
        Clock.schedule_once(lambda dt: criar_bip('bip_boom.wav', 120, 0.3, 0.8), 0.5)
        Clock.schedule_once(lambda dt: criar_bip('bip_bicho.wav', 400, 0.15, 0.5), 0.6)
        Clock.schedule_once(lambda dt: criar_bip('bip_morreu.wav', 180, 0.7, 0.6), 0.7)
        Clock.schedule_once(lambda dt: criar_bip('bip_venceu.wav', 800, 0.25, 0.5), 0.8)
    def build(self):
        sm = ScreenManager()
        sm.add_widget(TelaInicial(name='inicio'))
        sm.add_widget(TelaJogo(name='jogo'))
        sm.current = 'inicio'
        return sm

if __name__ == '__main__':
    PacmanApp().run()
