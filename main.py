import os
import json
import random
import math
import wave
import struct
from kivy.app import App
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse, Line, Rectangle, Triangle
from kivy.resources import resource_find
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
                    if antigo.get("fase", 1) > fase: return antigo
                    if antigo.get("fase") == fase and antigo.get("pontos", 0) >= pontos: return antigo
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
        framerate = 44100
        nframes = int(framerate * duracao)
        with wave.open(nome, 'w') as wav:
            wav.setnchannels(1); wav.setsampwidth(2); wav.setframerate(framerate)
            for i in range(nframes):
                v = volume * (1 - i / nframes)
                sample = int(v * 32767 * math.sin(2 * math.pi * freq * i / framerate))
                wav.writeframes(struct.pack('<h', sample))
    except: pass

def tocar_bip(nome):
    try:
        s = SoundLoader.load(nome)
        if s: s.play()
    except: pass

FASES_MAPAS = [
    [[1,1,1,1,1,1,1,1,1,1,1],[1,2,0,0,1,0,1,0,0,2,1],[1,0,1,0,1,0,1,1,0,0,1],[1,0,1,0,0,0,0,1,0,1,1],[1,0,0,0,1,1,0,0,0,0,1],[1,0,1,0,0,0,0,1,0,1,1],[1,0,1,0,1,1,0,1,0,0,1],[1,0,0,0,0,0,0,0,1,0,1],[1,0,1,1,0,1,1,0,0,0,1],[1,2,0,0,0,0,0,0,0,2,1],[1,1,1,1,1,1,1,1,1,1,1]],
    [[1,1,1,1,1,1,1,1,1,1,1],[1,2,0,0,1,0,1,0,0,2,1],[1,0,1,0,0,0,0,0,1,0,1],[1,0,0,0,1,1,0,1,0,0,1],[1,0,1,0,0,0,0,0,1,0,1],[1,0,0,1,0,1,0,1,0,0,1],[1,0,1,0,0,0,0,0,1,0,1],[1,2,0,0,1,0,1,0,0,2,1],[1,0,1,0,0,0,0,0,1,0,1],[1,0,0,0,0,0,0,0,0,0,1],[1,1,1,1,1,1,1,1,1,1,1]],
    [[1,1,1,1,1,1,1,1,1,1,1],[1,2,0,1,0,1,0,1,0,2,1],[1,0,0,0,0,0,0,0,0,0,1],[1,0,1,0,1,1,0,1,0,1,1],[1,0,0,0,0,0,0,0,0,0,1],[1,0,1,0,1,0,1,0,1,0,1],[1,0,0,0,0,0,0,0,0,0,1],[1,2,0,1,0,1,0,1,0,2,1],[1,0,0,0,0,0,0,0,0,0,1],[1,0,1,0,1,0,1,0,1,0,1],[1,1,1,1,1,1,1,1,1,1,1]],
    [[1,1,1,1,1,1,1,1,1,1,1],[1,2,0,0,1,0,1,0,0,2,1],[1,0,1,0,0,0,0,0,1,0,1],[1,0,0,0,1,0,1,0,0,0,1],[1,0,1,1,0,0,0,1,1,0,1],[1,0,0,0,0,1,0,0,0,0,1],[1,0,1,0,1,0,1,0,1,0,1],[1,0,0,0,0,0,0,0,0,0,1],[1,0,1,1,0,1,1,0,1,0,1],[1,2,0,0,0,0,0,0,0,2,1],[1,1,1,1,1,1,1,1,1,1,1]],
    [[1,1,1,1,1,0,1,1,1,1,1],[1,2,0,0,0,0,0,0,0,2,1],[1,0,1,1,0,1,0,1,1,0,1],[1,0,0,0,0,0,0,0,0,0,1],[1,0,1,0,1,0,1,0,1,0,1],[1,0,0,0,0,1,0,0,0,0,1],[1,0,1,0,1,0,1,0,1,0,1],[1,2,0,0,0,0,0,0,0,2,1],[1,0,1,1,0,1,0,1,1,0,1],[1,0,0,0,0,0,0,0,0,0,1],[1,1,1,1,1,0,1,1,1,1,1]],
    [[1,1,1,1,1,1,1,1,1,1,1],[1,2,0,0,0,0,0,0,0,2,1],[1,0,1,1,1,1,1,1,1,0,1],[1,0,1,0,0,0,0,0,1,0,1],[1,0,1,0,1,1,1,0,1,0,1],[1,0,0,0,1,0,1,0,0,0,1],[1,0,1,0,1,0,1,0,1,0,1],[1,0,1,0,0,0,0,0,1,0,1],[1,0,1,1,1,1,1,1,1,0,1],[1,2,0,0,0,0,0,0,0,2,1],[1,1,1,1,1,1,1,1,1,1,1]],
]

FASES_SKINS = [
    {"fixo": (1, 0.4, 0.6, 1), "nome": "Rosa"},
    {"fixo": (0.2, 0.7, 1, 1), "nome": "Azul"},
    {"fixo": (1, 0.8, 0.6, 1), "nome": "Bege"},
    {"fixo": (0.6, 0.2, 1, 1), "nome": "Roxo"},
    {"fixo": (1, 0.9, 0.2, 1), "nome": "Amarelo"},
    {"fixo": (1, 0.6, 0.8, 1), "nome": "Espiral"},
]

class Bloco(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tipo = 'chao'
        self.bind(pos=self._redesenhar, size=self._redesenhar)
    def _redesenhar(self, *args): self.desenhar(self.tipo, None, None)
    def desenhar(self, tipo, cor_fase=None, skin=None, inimigo_tipo='vermelho'):
        self.tipo = tipo
        self.canvas.clear()
        x, y = self.pos; w, h = self.size
        if w <= 1 or h <= 1: return
        fixo = skin["fixo"] if skin else (0,0.4,1,1)
        with self.canvas:
            Color(0,0,0,1); Rectangle(pos=(x, y), size=(w, h))
            if tipo == 'fixo':
                Color(*fixo); Rectangle(pos=(x, y), size=(w, h))
                Color(0,0,0,1); Rectangle(pos=(x+2, y+2), size=(w-4, h-4))
                Color(*fixo); Line(rectangle=(x+1, y+1, w-2, h-2), width=1.2)
                return
            elif tipo == 'pastilha':
                Color(1,1,1,1); Ellipse(pos=(x + w*0.38, y + h*0.38), size=(w*0.24, h*0.24))
                return
            elif tipo == 'poder':
                Color(1,1,1,1); Ellipse(pos=(x + w*0.15, y + h*0.15), size=(w*0.70, h*0.70))
                return
            elif tipo == 'player':
                Color(1,1,0,1); Ellipse(pos=(x + w*0.10, y + h*0.10), size=(w*0.80, h*0.80))
                Color(0,0,0,1); Ellipse(pos=(x + w*0.55, y + h*0.62), size=(w*0.12, h*0.12))
                Color(0,0,0,1); Triangle(points=[x+w*0.55, y+h*0.5, x+w*0.95, y+h*0.70, x+w*0.95, y+h*0.30])
                return
            elif tipo == 'assustado':
                Color(0,0,1,1); Ellipse(pos=(x + w*0.10, y + h*0.20), size=(w*0.80, h*0.60)); Rectangle(pos=(x + w*0.10, y + h*0.05), size=(w*0.80, h*0.30))
                Color(1,1,1,1); Ellipse(pos=(x + w*0.24, y + h*0.50), size=(w*0.20, h*0.24)); Ellipse(pos=(x + w*0.56, y + h*0.50), size=(w*0.20, h*0.24))
                return
            elif tipo == 'inimigo':
                cores = {'vermelho': (1,0,0,1), 'rosa': (1,0.6,0.8,1), 'ciano': (0,1,1,1), 'laranja': (1,0.6,0,1)}
                c = cores.get(inimigo_tipo, (1,0,0,1))
                Color(*c); Ellipse(pos=(x + w*0.10, y + h*0.20), size=(w*0.80, h*0.60)); Rectangle(pos=(x + w*0.10, y + h*0.05), size=(w*0.80, h*0.30))
                Color(1,1,1,1); Ellipse(pos=(x + w*0.24, y + h*0.50), size=(w*0.20, h*0.24)); Ellipse(pos=(x + w*0.56, y + h*0.50), size=(w*0.20, h*0.24))
                Color(0,0,0,1); Ellipse(pos=(x + w*0.30, y + h*0.54), size=(w*0.09, h*0.14)); Ellipse(pos=(x + w*0.62, y + h*0.54), size=(w*0.09, h*0.14))
                return

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
        layout.add_widget(Label(text="PACMAN", font_size='34sp', color=(1, 0.85, 0.1, 1), bold=True, size_hint_y=0.12))
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
        if rec["fase"] > 1 or rec["pontos"] > 0: self.lbl_recorde.text = f"RECORDE: FASE {rec['fase']} - {rec['pontos']} PONTOS"
        else: self.lbl_recorde.text = "SEM RECORDE - JOGUE!"
        Clock.schedule_once(lambda dt: self.tocar_musica(), 0.2)
    def on_leave(self): self.parar_musica()
    def tocar_musica(self):
        try:
            if self.musica: self.musica.stop()
            pasta = os.path.dirname(os.path.abspath(__file__))
            caminho = None
            for nome in os.listdir(pasta):
                if nome.lower() == "nes.mp3": caminho = os.path.join(pasta, nome); break
            if not caminho: caminho = resource_find("nes.mp3")
            if caminho and os.path.exists(caminho):
                self.musica = SoundLoader.load(caminho)
                if self.musica: self.musica.loop = True; self.musica.play()
        except: pass
    def parar_musica(self):
        try: 
            if self.musica: self.musica.stop()
        except: pass
    def ir_para_jogo(self, *args):
        self.parar_musica()
        self.manager.get_screen('jogo').iniciar_fase(1)
        self.manager.current = 'jogo'

class TelaJogo(Screen):
    LINHAS = 11; COLUNAS = 11
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fase = 1; self.pontos = 0; self.vidas = 3
        self.player = [1, 1]; self.inimigos = []; self.mapa = []; self.blocos = []; self.game_over = False; self._event_inimigo = None
        self._event_andar = None; self._dir_andar = (0, 0); self.pastilhas = set(); self.poderes = set(); self.modo_poder = False; self.tempo_poder = None
        root = BoxLayout(orientation='vertical', spacing=2, padding=2)
        self.lbl_info = Label(text="VIDAS: 3 - FASE 1/6", font_size='14sp', bold=True, size_hint_y=0.06, color=(1, 1, 1, 1))
        root.add_widget(self.lbl_info)
        self.grid = GridLayout(cols=self.COLUNAS, rows=self.LINHAS, spacing=1, size_hint_y=0.78)
        root.add_widget(self.grid)
        controles = BoxLayout(orientation='horizontal', spacing=6, size_hint_y=0.16)
        controles.add_widget(Widget(size_hint_x=0.20))
        dpad = GridLayout(cols=3, rows=3, spacing=4, size_hint_x=0.60)
        dpad.add_widget(Widget())
        b_cima = Button(text="CIMA", font_size='12sp', bold=True, background_color=(0.25, 0.25, 0.28, 1))
        b_cima.bind(on_press=lambda x: self.iniciar_andar(-1, 0)); b_cima.bind(on_release=lambda x: self.parar_andar())
        dpad.add_widget(b_cima); dpad.add_widget(Widget())
        b_esq = Button(text="ESQ", font_size='12sp', bold=True, background_color=(0.25, 0.25, 0.28, 1))
        b_esq.bind(on_press=lambda x: self.iniciar_andar(0, -1)); b_esq.bind(on_release=lambda x: self.parar_andar())
        dpad.add_widget(b_esq); dpad.add_widget(Widget())
        b_dir = Button(text="DIR", font_size='12sp', bold=True, background_color=(0.25, 0.25, 0.28, 1))
        b_dir.bind(on_press=lambda x: self.iniciar_andar(0, 1)); b_dir.bind(on_release=lambda x: self.parar_andar())
        dpad.add_widget(b_dir); dpad.add_widget(Widget())
        b_baixo = Button(text="BAIXO", font_size='12sp', bold=True, background_color=(0.25, 0.25, 0.28, 1))
        b_baixo.bind(on_press=lambda x: self.iniciar_andar(1, 0)); b_baixo.bind(on_release=lambda x: self.parar_andar())
        dpad.add_widget(b_baixo); dpad.add_widget(Widget())
        controles.add_widget(dpad)
        controles.add_widget(Widget(size_hint_x=0.05))
        b_voltar = Button(text="VOLTAR", font_size='11sp', bold=True, background_color=(0.3, 0.3, 0.35, 1), size_hint_x=0.15)
        b_voltar.bind(on_release=lambda x: self.voltar_menu())
        controles.add_widget(b_voltar)
        root.add_widget(controles)
        self.add_widget(root)
        Window.bind(on_key_down=self.teclado)
    def teclado(self, window, key, *args):
        if self.manager and self.manager.current != 'jogo': return False
        if key in [273, 274, 275, 276]:
            if key == 273: self.mover(-1, 0)
            elif key == 274: self.mover(1, 0)
            elif key == 275: self.mover(0, 1)
            elif key == 276: self.mover(0, -1)
        return True
    def iniciar_andar(self, dl, dc):
        self._dir_andar = (dl, dc); self.mover(dl, dc)
        if self._event_andar: self._event_andar.cancel()
        self._event_andar = Clock.schedule_interval(lambda dt: self.mover(self._dir_andar[0], self._dir_andar[1]), 0.22)
    def parar_andar(self, *args):
        if self._event_andar: self._event_andar.cancel(); self._event_andar = None
    def iniciar_fase(self, fase):
        self.fase = fase; self.game_over = False; self.modo_poder = False
        if fase == 1: self.vidas = 3; self.pontos = 0
        if self.tempo_poder: self.tempo_poder.cancel(); self.tempo_poder = None
        self.player = [1, 1]; self.inimigos = []; self.mapa = [row[:] for row in FASES_MAPAS[fase-1]]
        self.pastilhas = set(); self.poderes = set()
        for l in range(self.LINHAS):
            for c in range(self.COLUNAS):
                if self.mapa[l][c] == 0: self.pastilhas.add((l,c))
                elif self.mapa[l][c] == 2: self.poderes.add((l,c))
        self.mapa[1][1] = 0
        if (1,1) in self.pastilhas: self.pastilhas.remove((1,1))
        if (1,1) in self.poderes: self.poderes.remove((1,1))
        tipos = ['vermelho','rosa','ciano','laranja']
        livres = [(l,c) for l in range(3,8) for c in range(3,8) if self.mapa[l][c] != 1]
        random.shuffle(livres)
        for i in range(4):
            if i < len(livres):
                l,c = livres[i]
                self.inimigos.append([l, c, random.choice([(1,0),(-1,0),(0,1),(0,-1)]), tipos[i]])
        self.grid.clear_widgets(); self.blocos = []
        for l in range(self.LINHAS):
            linha_blocos = []
            for c in range(self.COLUNAS):
                b = Bloco(); self.grid.add_widget(b); linha_blocos.append(b)
            self.blocos.append(linha_blocos)
        self.atualizar_info(); self.desenhar_mapa()
        if self._event_inimigo: self._event_inimigo.cancel()
        self._event_inimigo = Clock.schedule_interval(lambda dt: self.atualizar_inimigos(), 0.45)
    def atualizar_info(self):
        nome = FASES_SKINS[self.fase-1]["nome"]
        modo = " PODER!" if self.modo_poder else ""
        self.lbl_info.text = f"VIDAS: {self.vidas} - FASE {self.fase}/6 {nome}{modo} - {self.pontos} PTS"
    def desenhar_mapa(self):
        skin = FASES_SKINS[self.fase - 1]
        for l in range(self.LINHAS):
            for c in range(self.COLUNAS):
                tipo = 'chao'
                if self.mapa[l][c] == 1: tipo = 'fixo'
                elif (l,c) in self.poderes: tipo = 'poder'
                elif (l,c) in self.pastilhas: tipo = 'pastilha'
                if [l, c] == self.player: tipo = 'player'
                for e in self.inimigos:
                    if e[0] == l and e[1] == c:
                        tipo = 'assustado' if self.modo_poder else 'inimigo'
                self.blocos[l][c].desenhar(tipo, None, skin, e[3] if 'e' in locals() and e[0]==l and e[1]==c else 'vermelho')
        # desenha certo com tipo do fantasma
        for l in range(self.LINHAS):
            for c in range(self.COLUNAS):
                for e in self.inimigos:
                    if e[0]==l and e[1]==c:
                        self.blocos[l][c].desenhar('assustado' if self.modo_poder else 'inimigo', None, skin, e[3])

    def pode_andar(self, l, c):
        if l < 0 or l >= self.LINHAS or c < 0 or c >= self.COLUNAS: return False
        return self.mapa[l][c] != 1
    def mover(self, dl, dc):
        if self.game_over: return
        nl, nc = self.player[0] + dl, self.player[1] + dc
        if not self.pode_andar(nl, nc): return
        self.player = [nl, nc]
        if (nl, nc) in self.pastilhas: self.pastilhas.remove((nl, nc)); self.pontos += 10; tocar_bip('bip_venceu.wav')
        if (nl, nc) in self.poderes: self.poderes.remove((nl, nc)); self.pontos += 50; self.modo_poder = True; tocar_bip('bip_venceu.wav'); 
        if self.tempo_poder: self.tempo_poder.cancel()
        if self.modo_poder and (nl,nc) in self.poderes or self.modo_poder: 
            if self.tempo_poder: self.tempo_poder.cancel()
            self.tempo_poder = Clock.schedule_once(lambda dt: self.fim_poder(), 7)
        # corrige timer poder
        if (nl,nc) in self.poderes or self.modo_poder and len(self.poderes) < 4:
            if not self.tempo_poder:
                self.tempo_poder = Clock.schedule_once(lambda dt: self.fim_poder(), 7)
        for e in self.inimigos[:]:
            if e[0] == nl and e[1] == nc:
                if self.modo_poder: self.inimigos.remove(e); self.pontos += 200; tocar_bip('bip_bicho.wav')
                else: self.perdeu(); return
        self.atualizar_info()
        if len(self.pastilhas) == 0 and len(self.poderes) == 0: self.venceu_fase(); return
        self.desenhar_mapa()
    def atualizar_inimigos(self):
        if self.game_over or self.manager.current != 'jogo': return
        for e in self.inimigos[:]:
            dl, dc = e[2]
            if e[3] == 'vermelho' and not self.modo_poder and random.random() < 0.7:
                if self.player[0] > e[0]: dl, dc = 1, 0
                elif self.player[0] < e[0]: dl, dc = -1, 0
                elif self.player[1] > e[1]: dl, dc = 0, 1
                elif self.player[1] < e[1]: dl, dc = 0, -1
            nl, nc = e[0] + dl, e[1] + dc
            if not self.pode_andar(nl, nc): e[2] = random.choice([(1,0),(-1,0),(0,1),(0,-1)])
            else: e[0], e[1] = nl, nc; e[2] = (dl, dc)
            if [e[0], e[1]] == self.player:
                if self.modo_poder: self.inimigos.remove(e); self.pontos += 200; tocar_bip('bip_bicho.wav'); self.atualizar_info(); return
                else: self.perdeu(); return
        self.desenhar_mapa()
    def fim_poder(self): self.modo_poder = False; self.tempo_poder = None; self.atualizar_info(); self.desenhar_mapa()
    def perdeu(self):
        if self.game_over: return
        tocar_bip('bip_morreu.wav'); self.vidas -= 1; salvar_recorde(self.fase, self.pontos)
        if self.tempo_poder: self.tempo_poder.cancel(); self.tempo_poder = None; self.modo_poder = False
        if self.vidas <= 0:
            self.game_over = True
            if self._event_inimigo: self._event_inimigo.cancel()
            self.lbl_info.text = f"VOCE PERDEU! {self.pontos} PTS"; self.desenhar_mapa()
        else: self.player = [1, 1]; self.atualizar_info(); self.desenhar_mapa()
    def venceu_fase(self):
        if self.game_over: return
        self.game_over = True; tocar_bip('bip_venceu.wav'); self.pontos += 200; salvar_recorde(self.fase, self.pontos)
        if self._event_inimigo: self._event_inimigo.cancel()
        if self.tempo_poder: self.tempo_poder.cancel(); self.tempo_poder = None
        if self.fase >= 6: self.lbl_info.text = f"ZEROU! {self.pontos} PTS!"; Clock.schedule_once(lambda dt: self.voltar_menu(), 2.5)
        else: self.lbl_info.text = f"FASE {self.fase} OK! {self.pontos} PTS"; Clock.schedule_once(lambda dt: self.iniciar_fase(self.fase + 1), 1.5)
    def voltar_menu(self):
        if self._event_inimigo: self._event_inimigo.cancel()
        if self._event_andar: self._event_andar.cancel()
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
        return sm

if __name__ == '__main__':
    PacmanApp().run()
