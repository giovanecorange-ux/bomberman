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
                    if antigo.get("pontos", 0) >= pontos:
                        return antigo
            except Exception:
                pass
        with open(ARQ_RECORDE, "w") as f:
            json.dump(dados, f)
        return dados
    except Exception:
        return {"fase": fase, "pontos": pontos}


def carregar_recorde():
    try:
        if os.path.exists(ARQ_RECORDE):
            with open(ARQ_RECORDE, "r") as f:
                return json.load(f)
    except Exception:
        pass
    return {"fase": 1, "pontos": 0}


def criar_bip(nome, freq, duracao=0.2, volume=0.5):
    try:
        if os.path.exists(nome):
            return
        framerate = 44100
        nframes = int(framerate * duracao)
        with wave.open(nome, 'w') as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(framerate)
            for i in range(nframes):
                v = volume * (1 - i / nframes)
                sample = int(v * 32767 * math.sin(2 * math.pi * freq * i / framerate))
                wav.writeframes(struct.pack('<h', sample))
    except Exception:
        pass


_sons_cache = {}


def tocar_bip(nome):
    try:
        if not os.path.exists(nome):
            return
        if nome not in _sons_cache:
            s = SoundLoader.load(nome)
            _sons_cache[nome] = s
        s = _sons_cache.get(nome)
        if s:
            s.stop()
            s.play()
    except Exception:
        pass


def _mapa_de_texto(linhas):
    linhas = [l[:21].ljust(21, '#') for l in linhas]
    return [[1 if ch == '#' else 2 if ch == 'P' else 0 for ch in l] for l in linhas]


# 21 colunas x 17 linhas - PAISAGEM fiel à foto com túnel vertical na coluna 10
FASES_MAPAS_TXT = [[
    "########## ##########",
    "#P........#........P#",
    "#.###.###.#.###.###.#",
    "#.#...............#.#",
    "#.#.###.#####.###.#.#",
    "#.....#...#...#.....#",
    "#####.###.#.###.#####",
    "#.........#.........#",
    "#.###.###...###.###.#",
    "#.#.......#.......#.#",
    "#.#.###.#####.###.#.#",
    "#.....#...#...#.....#",
    "#####.###.#.###.#####",
    "#.#...............#.#",
    "#.###.###.#.###.###.#",
    "#P........#........P#",
    "########## ##########",
]]

FASES_MAPAS = [_mapa_de_texto(m) for m in FASES_MAPAS_TXT] * 5

FASES_SKINS = [
    {"fixo": (1.00, 0.82, 0.10, 1), "nome": "Atari Amarelo"},
    {"fixo": (0.20, 0.90, 0.35, 1), "nome": "Atari Verde"},
    {"fixo": (1.00, 0.35, 0.65, 1), "nome": "Atari Rosa"},
    {"fixo": (0.25, 0.85, 1.00, 1), "nome": "Atari Ciano"},
    {"fixo": (1.00, 0.50, 0.15, 1), "nome": "Atari Laranja"},
]


class Bloco(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tipo = 'chao'
        self.l = 0
        self.c = 0
        self.bind(pos=self._redesenhar, size=self._redesenhar)

    def _redesenhar(self, *args):
        self.desenhar(self.tipo, None, None)

    def desenhar(self, tipo, cor_fase=None, skin=None, inimigo_tipo='vermelho', casa_set=None, porta=None, parede_set=None):
        self.tipo = tipo
        self.canvas.clear()
        x, y = self.pos
        w, h = self.size
        if w <= 1 or h <= 1:
            return
        fixo = skin["fixo"] if skin else (1, 0.82, 0.1, 1)
        with self.canvas:
            Color(0, 0, 0.7, 1)
            Rectangle(pos=(x, y), size=(w, h))
            if tipo == 'fixo':
                Color(*fixo)
                Line(rectangle=(x + 1, y + 1, w - 2, h - 2), width=1.6)
                return
            elif tipo == 'pastilha':
                m = min(w, h)
                Color(0.85, 0.65, 0.2, 1)
                Rectangle(pos=(x + (w - m * 0.45) / 2, y + (h - m * 0.18) / 2), size=(m * 0.45, m * 0.18))
                return
            elif tipo == 'poder':
                m = min(w, h)
                Color(0.2, 1, 0.3, 1)
                Rectangle(pos=(x + (w - m * 0.65) / 2, y + (h - m * 0.65) / 2), size=(m * 0.65, m * 0.65))
                return
            elif tipo == 'player':
                Color(1, 1, 0, 1)
                Ellipse(pos=(x + w * 0.10, y + h * 0.10), size=(w * 0.80, h * 0.80))
                Color(0, 0, 0, 1)
                Triangle(points=[x + w * 0.55, y + h * 0.5, x + w * 0.95, y + h * 0.70, x + w * 0.95, y + h * 0.30])
                return
            elif tipo == 'assustado':
                Color(0, 0, 1, 1)
                Ellipse(pos=(x + w * 0.10, y + h * 0.20), size=(w * 0.80, h * 0.60))
                Rectangle(pos=(x + w * 0.10, y + h * 0.05), size=(w * 0.80, h * 0.30))
                Color(1, 1, 1, 1)
                Ellipse(pos=(x + w * 0.24, y + h * 0.50), size=(w * 0.20, h * 0.24))
                Ellipse(pos=(x + w * 0.56, y + h * 0.50), size=(w * 0.20, h * 0.24))
                return
            elif tipo == 'inimigo':
                cores = {'vermelho': (1, 0, 0, 1), 'rosa': (1, 0.6, 0.8, 1), 'ciano': (0, 1, 1, 1), 'laranja': (1, 0.6, 0, 1)}
                c = cores.get(inimigo_tipo, (1, 0, 0, 1))
                Color(*c)
                Ellipse(pos=(x + w * 0.10, y + h * 0.20), size=(w * 0.80, h * 0.60))
                Rectangle(pos=(x + w * 0.10, y + h * 0.05), size=(w * 0.80, h * 0.30))
                Color(1, 1, 1, 1)
                Ellipse(pos=(x + w * 0.24, y + h * 0.50), size=(w * 0.20, h * 0.24))
                Ellipse(pos=(x + w * 0.56, y + h * 0.50), size=(w * 0.20, h * 0.24))
                Color(0, 0, 0, 1)
                Ellipse(pos=(x + w * 0.30, y + h * 0.54), size=(w * 0.09, h * 0.14))
                Ellipse(pos=(x + w * 0.62, y + h * 0.54), size=(w * 0.09, h * 0.14))
                return
            elif tipo == 'casinha':
                Color(0, 0, 0.7, 1)
                Rectangle(pos=(x, y), size=(w, h))
                Color(*fixo)
                if (self.l - 1, self.c) not in (casa_set or set()) and (self.l - 1, self.c) != porta:
                    Line(points=[x, y + h, x + w, y + h], width=2.2)
                if (self.l + 1, self.c) not in (casa_set or set()):
                    Line(points=[x, y, x + w, y], width=2.2)
                if (self.l, self.c - 1) not in (casa_set or set()):
                    Line(points=[x, y, x, y + h], width=2.2)
                if (self.l, self.c + 1) not in (casa_set or set()):
                    Line(points=[x + w, y, x + w, y + h], width=2.2)
                return
            elif tipo == 'porta':
                Color(0, 0, 0.7, 1)
                Rectangle(pos=(x, y), size=(w, h))
                Color(1, 1, 1, 0.95)
                Rectangle(pos=(x, y + h * 0.38), size=(w, h * 0.24))
                return
            elif tipo == 'vitamina':
                m = min(w, h)
                Color(1, 0.85, 0.1, 1)
                Ellipse(pos=(x + (w - m * 0.55) / 2, y + (h - m * 0.55) / 2), size=(m * 0.55, m * 0.55))
                return


class DesenhoCapa(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self._desenhar, size=self._desenhar)

    def _desenhar(self, *args):
        self.canvas.clear()
        x, y = self.pos
        w, h = self.size
        if w <= 10 or h <= 10:
            return
        lado = min(w / 4.5, h * 0.75)
        espaco = (w - (lado * 4)) / 5.0
        cy = y + (h - lado) / 2.0
        with self.canvas:
            Color(0, 0, 0.7, 1)
            Rectangle(pos=(x, y), size=(w, h))
            bx = x + espaco
            Color(1, 1, 0, 1)
            Ellipse(pos=(bx, cy), size=(lado, lado))
            Color(0, 0, 0, 1)
            Triangle(points=[bx + lado * 0.5, cy + lado * 0.5, bx + lado * 1.05, cy + lado * 0.75, bx + lado * 1.05, cy + lado * 0.25])
            cores = [(1, 0, 0, 1), (1, 0.6, 0.8, 1), (0, 1, 1, 1), (1, 0.6, 0, 1)]
            for i, cor in enumerate(cores):
                fx = bx + (lado + espaco) * (i + 1)
                Color(*cor)
                Ellipse(pos=(fx, cy + lado * 0.2), size=(lado * 0.8, lado * 0.6))
                Rectangle(pos=(fx, cy), size=(lado * 0.8, lado * 0.3))
                Color(1, 1, 1, 1)
                Ellipse(pos=(fx + lado * 0.15, cy + lado * 0.5), size=(lado * 0.18, lado * 0.2))
                Ellipse(pos=(fx + lado * 0.45, cy + lado * 0.5), size=(lado * 0.18, lado * 0.2))


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
        btn = Button(text="INICIAR JOGO", font_size='24sp', bold=True, background_color=(0.15, 0.75, 0.25, 1), size_hint_y=0.14)
        btn.bind(on_release=self.iniciar)
        layout.add_widget(btn)
