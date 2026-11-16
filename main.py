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

# === SO AQUI MUDOU: PACMAN - FUNDO PRETO + 5 MAPAS COLORIDOS ===
FASES_SKINS = [
    {"chao": (0,0,0,1), "fixo": (0, 0.4, 1, 1), "dest": (0,0,0,1), "detalhe": (0,0.4,1,1), "nome": "Azul"},
    {"chao": (0,0,0,1), "fixo": (0, 0.8, 0.2, 1), "dest": (0,0,0,1), "detalhe": (0,0.8,0.2,1), "nome": "Verde"},
    {"chao": (0,0,0,1), "fixo": (1, 0.2, 0.2, 1), "dest": (0,0,0,1), "detalhe": (1,0.2,0.2,1), "nome": "Vermelho"},
    {"chao": (0,0,0,1), "fixo": (0.6, 0.2, 1, 1), "dest": (0,0,0,1), "detalhe": (0.6,0.2,1,1), "nome": "Roxo"},
    {"chao": (0,0,0,1), "fixo": (1, 0.9, 0.2, 1), "dest": (0,0,0,1), "detalhe": (1,0.9,0.2,1), "nome": "Amarelo"},
]

# Labirinto Pacman 11x11 - 1=parede, 0=pastilha
MAPA_PACMAN = [
    [1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,1,0,0,0,0,1],
    [1,0,1,1,0,1,0,1,1,0,1],
    [1,0,1,0,0,0,0,0,1,0,1],
    [1,0,0,0,1,1,1,0,0,0,1],
    [1,1,0,1,1,0,1,1,0,1,1],
    [1,0,0,0,1,0,1,0,0,0,1],
    [1,0,1,0,0,0,0,0,1,0,1],
    [1,0,1,1,0,1,0,1,1,0,1],
    [1,0,0,0,0,1,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1],
]

class Bloco(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tipo = 'chao'
        self.cor_atual = (0,0,0,1)
        self.bind(pos=self._redesenhar, size=self._redesenhar)
    def _redesenhar(self, *args): self.desenhar(self.tipo, self.cor_atual)
    def desenhar(self, tipo, cor_fase=None, skin=None, inimigo_tipo='vermelho'):
        self.tipo = tipo
        if cor_fase: self.cor_atual = cor_fase
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
            elif tipo == 'moeda':
                Color(1,1,0,1); Ellipse(pos=(x + w*0.30, y + h*0.30), size=(w*0.40, h*0.40))
                return
            elif tipo == 'player':
                # PACMAN AMARELO - igual teu icone
                Color(1,1,0,1); Ellipse(pos=(x + w*0.10, y + h*0.10), size=(w*0.80, h*0.80))
                Color(0,0,0,1); Ellipse(pos=(x + w*0.55, y + h*0.62), size=(w*0.12, h*0.12))
                Color(0,0,0,1); Triangle(points=[x+w*0.55, y+h*0.5, x+w*0.95, y+h*0.70, x+w*0.95, y+h*0.30])
                return
            elif tipo == 'inimigo':
                # 4 FANTASMAS - igual teu icone
                cores = {'vermelho': (1,0,0,1), 'rosa': (1,0.6,0.8,1), 'ciano': (0,1,1,1), 'laranja': (1,0.6,0,1), 'azul': (0,1,1,1), 'verde': (1,0,0,1)}
                c = cores.get(inimigo_tipo, (1,0,0,1))
                Color(*c); Ellipse(pos=(x + w*0.10, y + h*0.20), size=(w*0.80, h*0.60))
                Rectangle(pos=(x + w*0.10, y + h*0.05), size=(w*0.80, h*0.30))
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
            # Pacman igual icone
            Color(1,1,0,1); Ellipse(pos=(bx, cy), size=(lado, lado))
            Color(0,0,0,1); Triangle(points=[bx+lado*0.5, cy+lado*0.5, bx+lado*1.05, cy+lado*0.75, bx+lado*1.05, cy+lado*0.25])
            cores = [(1,0,0,1),(1,0.6,0.8,1),(0,1,1,1),(1,0.6,0,1)]
            for i, cor in enumerate(cores):
                fx = bx + (lado+espaco)*(i+1)
                Color(*cor); Ellipse(pos=(fx, cy+lado*0.2), size=(lado*0.8, lado*0.6))
                Rectangle(pos=(fx, cy), size=(lado*0.8, lado*0.3))
                Color(1,1,1,1); Ellipse(pos=(fx+lado*0.15, cy+lado*0.5), size=(lado*0.18, lado*0.2)); Ellipse(pos=(fx+lado*0.45, cy+lado*0.5), size=(lado*0.18, lado*0.2))
                Color(0,0,0,1); Ellipse(pos=(fx+lado*0.20, cy+lado*0.54), size=(lado*0.08, lado*0.1)); Ellipse(pos=(fx+lado*0.50, cy+lado*0.54), size=(lado*0.08, lado*0.1))

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
        if rec["fase"] > 1 or rec["pontos"] > 0:
            self.lbl_recorde.text = f"RECORDE: FASE {rec['fase']} - {rec['pontos']} PONTOS"
        else:
            self.lbl_recorde.text = "SEM RECORDE - JOGUE!"
        Clock.schedule_once(lambda dt: self.tocar_musica(), 0.2)
    def on_leave(self): self.parar_musica()
    def tocar_musica(self):
        try:
            if self.musica: self.musica.stop()
            nome_arquivo = None
            pasta = os.path.dirname(os.path.abspath(__file__))
            for nome in os.listdir(pasta):
                if nome.lower() == "nes.mp3":
                    nome_arquivo = nome
                    break
            caminho = None
            if nome_arquivo:
                caminho = os.path.join(pasta, nome_arquivo)
            else:
                caminho = resource_find("nes.mp3")
                if not caminho: caminho = resource_find("nes.Mp3")
            if caminho and os.path.exists(caminho):
                self.musica = SoundLoader.load(caminho)
                if self.musica:
                    self.musica.loop = True
                    self.musica.volume = 1.0
                    self.musica.play()
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
    CORES_FASE = [s["chao"] for s in FASES_SKINS]
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fase = 1; self.pontos = 0; self.vidas = 3
        self.player = [1, 1]; self.inimigos = []; self.mapa = []; self.blocos = []; self.game_over = False; self._event_inimigo = None; self.itens = {}
        self._event_andar = None; self._dir_andar = (0, 0); self.pastilhas = set()
        root = BoxLayout(orientation='vertical', spacing=4, padding=4)
        self.lbl_info = Label(text="VIDAS: 3 - FASE 1/5", font_size='16sp', bold=True, size_hint_y=0.08, color=(1, 1, 1, 1))
        root.add_widget(self.lbl_info)
        self.grid = GridLayout(cols=self.COLUNAS, rows=self.LINHAS, spacing=1, size_hint_y=0.68)
        root.add_widget(self.grid)
        controles = BoxLayout(orientation='horizontal', spacing=8, size_hint_y=0.24)
        dpad = GridLayout(cols=3, rows=3, spacing=6)
        dpad.add_widget(Widget())
        b_cima = Button(text="CIMA", font_size='16sp', bold=True, background_color=(0.25, 0.25, 0.28, 1))
        b_cima.bind(on_press=lambda x: self.iniciar_andar(-1, 0))
        b_cima.bind(on_release=lambda x: self.parar_andar())
        dpad.add_widget(b_cima)
        dpad.add_widget(Widget())
        b_esq = Button(text="ESQ", font_size='16sp', bold=True, background_color=(0.25, 0.25, 0.28, 1))
        b_esq.bind(on_press=lambda x: self.iniciar_andar(0, -1))
        b_esq.bind(on_release=lambda x: self.parar_andar())
        dpad.add_widget(b_esq)
        dpad.add_widget(Widget())
        b_dir = Button(text="DIR", font_size='16sp', bold=True, background_color=(0.25, 0.25, 0.28, 1))
        b_dir.bind(on_press=lambda x: self.iniciar_andar(0, 1))
        b_dir.bind(on_release=lambda x: self.parar_andar())
        dpad.add_widget(b_dir)
        dpad.add_widget(Widget())
        b_baixo = Button(text="BAIXO", font_size='16sp', bold=True, background_color=(0.25, 0.25, 0.28, 1))
        b_baixo.bind(on_press=lambda x: self.iniciar_andar(1, 0))
        b_baixo.bind(on_release=lambda x: self.parar_andar())
        dpad.add_widget(b_baixo)
        dpad.add_widget(Widget())
        controles.add_widget(dpad)
        acoes = BoxLayout(orientation='vertical', spacing=8)
        b_bomba = Button(text="TURBO", font_size='28sp', bold=True, background_color=(1, 0.85, 0, 1), color=(0,0,0,1), size_hint_y=0.7)
        b_bomba.bind(on_release=lambda x: self.turbo())
        acoes.add_widget(b_bomba)
        b_voltar = Button(text="VOLTAR", font_size='16sp', background_color=(0.3, 0.3, 0.35, 1), size_hint_y=0.3)
        b_voltar.bind(on_release=lambda x: self.voltar_menu())
        acoes.add_widget(b_voltar)
        controles.add_widget(acoes)
        root.add_widget(controles)
        self.add_widget(root)
        Window.bind(on_key_down=self.teclado)
    def teclado(self, window, key, *args):
        if self.manager and self.manager.current != 'jogo': return False
        if key == 273: self.mover(-1, 0)
        elif key == 274: self.mover(1, 0)
        elif key == 275: self.mover(0, 1)
        elif key == 276: self.mover(0, -1)
        elif key == 32: self.turbo()
        return True
    def iniciar_andar(self, dl, dc):
        self._dir_andar = (dl, dc)
        self.mover(dl, dc)
        if self._event_andar: self._event_andar.cancel()
        self._event_andar = Clock.schedule_interval(lambda dt: self.mover(self._dir_andar[0], self._dir_andar[1]), 0.25)
    def parar_andar(self, *args):
        if self._event_andar:
            self._event_andar.cancel()
            self._event_andar = None
    def turbo(self):
        if not self.game_over:
            self.mover(self._dir_andar[0], self._dir_andar[1])
            self.mover(self._dir_andar[0], self._dir_andar[1])
    def iniciar_fase(self, fase):
        self.fase = fase; self.game_over = False
        if fase == 1: self.vidas = 3; self.pontos = 0
        self.player = [1, 1]; self.inimigos = []; self.mapa = []; self.itens = {}
        self.mapa = [row[:] for row in MAPA_PACMAN]
        self.pastilhas = set()
        for l in range(self.LINHAS):
            for c in range(self.COLUNAS):
                if self.mapa[l][c] == 0:
                    self.pastilhas.add((l,c))
        tipos = ['vermelho','rosa','ciano','laranja']
        pos_f = [(5,5),(5,6),(6,5),(6,6)]
        for i, (l,c) in enumerate(pos_f):
            self.inimigos.append([l, c, random.choice([(1,0),(-1,0),(0,1),(0,-1)]), tipos[i]])
        self.grid.clear_widgets(); self.blocos = []
        for l in range(self.LINHAS):
            linha_blocos = []
            for c in range(self.COLUNAS):
                b = Bloco(); self.grid.add_widget(b); linha_blocos.append(b)
            self.blocos.append(linha_blocos)
        self.atualizar_info(); self.desenhar_mapa()
        if self._event_inimigo: self._event_inimigo.cancel()
        self._event_inimigo = Clock.schedule_interval(lambda dt: self.atualizar_inimigos(), 0.5)
    def atualizar_info(self):
        coracoes = "♥ " * self.vidas
        nome = FASES_SKINS[self.fase-1]["nome"]
        self.lbl_info.text = f"{coracoes} FASE {self.fase}/5 {nome} - {self.pontos} PTS"
    def desenhar_mapa(self):
        cor_fase = self.CORES_FASE[self.fase - 1]
        skin = FASES_SKINS[self.fase - 1]
        for l in range(self.LINHAS):
            for c in range(self.COLUNAS):
                tipo = 'chao'
                if self.mapa[l][c] == 1: tipo = 'fixo'
                elif (l,c) in self.pastilhas: tipo = 'pastilha'
                if [l, c] == self.player: tipo = 'player'
                inimigo_tipo = 'vermelho'
                for e in self.inimigos:
                    if e[0] == l and e[1] == c:
                        tipo = 'inimigo'
                        inimigo_tipo = e[3]
                self.blocos[l][c].desenhar(tipo, cor_fase, skin, inimigo_tipo)
    def pode_andar(self, l, c):
        if l < 0 or l >= self.LINHAS or c < 0 or c >= self.COLUNAS: return False
        return self.mapa[l][c] != 1
    def mover(self, dl, dc):
        if self.game_over: return
        nl, nc = self.player[0] + dl, self.player[1] + dc
        if not self.pode_andar(nl, nc): return
        self.player = [nl, nc]
        if (nl, nc) in self.pastilhas:
            self.pastilhas.remove((nl, nc))
            self.pontos += 10
            tocar_bip('bip_venceu.wav')
            self.atualizar_info()
            if len(self.pastilhas) == 0:
                self.venceu_fase(); return
        for e in self.inimigos:
            if e[0] == nl and e[1] == nc: self.perdeu(); return
        self.desenhar_mapa()
    def atualizar_inimigos(self):
        if self.game_over or self.manager.current != 'jogo': return
        for e in self.inimigos:
            tipo = e[3]
            dl, dc = e[2]
            if tipo == 'vermelho' and random.random() < 0.7:
                if self.player[0] > e[0]: dl, dc = 1, 0
                elif self.player[0] < e[0]: dl, dc = -1, 0
                elif self.player[1] > e[1]: dl, dc = 0, 1
                elif self.player[1] < e[1]: dl, dc = 0, -1
            elif tipo in ['rosa','ciano'] and random.random() < 0.4:
                dl, dc = random.choice([(1,0),(-1,0),(0,1),(0,-1)])
            nl, nc = e[0] + dl, e[1] + dc
            if not self.pode_andar(nl, nc): e[2] = random.choice([(1,0),(-1,0),(0,1),(0,-1)])
            else: e[0], e[1] = nl, nc; e[2] = (dl, dc)
            if [e[0], e[1]] == self.player: self.perdeu(); return
        self.desenhar_mapa()
    def perdeu(self):
        if self.game_over: return
        tocar_bip('bip_morreu.wav')
        self.vidas -= 1
        salvar_recorde(self.fase, self.pontos)
        if self.vidas <= 0:
            self.game_over = True
            if self._event_inimigo: self._event_inimigo.cancel()
            self.lbl_info.text = f"VOCE PERDEU! {self.pontos} PTS - VOLTAR"
            self.desenhar_mapa()
        else:
            self.player = [1, 1]
            self.atualizar_info(); self.desenhar_mapa()
    def venceu_fase(self):
        if self.game_over: return
        self.game_over = True; tocar_bip('bip_venceu.wav')
        self.pontos += 200
        salvar_recorde(self.fase, self.pontos)
        if self._event_inimigo: self._event_inimigo.cancel()
        if self.fase >= 5:
            self.lbl_info.text = f"ZEROU! {self.pontos} PTS!"
            Clock.schedule_once(lambda dt: self.voltar_menu(), 2.5)
        else:
            self.lbl_info.text = f"FASE {self.fase} OK! {self.pontos} PTS"
            Clock.schedule_once(lambda dt: self.iniciar_fase(self.fase + 1), 1.5)
    def voltar_menu(self):
        if self._event_inimigo: self._event_inimigo.cancel()
        if self._event_andar: self._event_andar.cancel()
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
