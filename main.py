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

ARQ_RECORDE = "recorde_bomber.json"

def salvar_recorde(fase, pontos):
    try:
        dados = {"fase": fase, "pontos": pontos}
        if os.path.exists(ARQ_RECORDE):
            try:
                with open(ARQ_RECORDE, "r") as f:
                    antigo = json.load(f)
                    if antigo.get("fase", 1) > fase:
                        return antigo
                    if antigo.get("fase") == fase and antigo.get("pontos", 0) >= pontos:
                        return antigo
            except:
                pass
        with open(ARQ_RECORDE, "w") as f:
            json.dump(dados, f)
        return dados
    except:
        return {"fase": fase, "pontos": pontos}

def carregar_recorde():
    try:
        if os.path.exists(ARQ_RECORDE):
            with open(ARQ_RECORDE, "r") as f:
                return json.load(f)
    except:
        pass
    return {"fase": 1, "pontos": 0}

# --- BIPS RETRO ---
def criar_bip(nome, freq, duracao=0.2, volume=0.5):
    try:
        if os.path.exists(nome): return
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
    except: pass

def tocar_bip(nome):
    try:
        s = SoundLoader.load(nome)
        if s: s.play()
    except: pass

criar_bip('bip_boom.wav', 120, 0.3, 0.8)
criar_bip('bip_bicho.wav', 400, 0.15, 0.5)
criar_bip('bip_morreu.wav', 180, 0.7, 0.6)
criar_bip('bip_venceu.wav', 800, 0.25, 0.5)

class Bloco(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tipo = 'chao'
        self.bind(pos=self._redesenhar, size=self._redesenhar)
    def _redesenhar(self, *args): self.desenhar(self.tipo)
    def desenhar(self, tipo):
        self.tipo = tipo
        self.canvas.clear()
        x, y = self.pos
        w, h = self.size
        if w <= 1 or h <= 1: return
        chao = (0.20, 0.68, 0.22, 1)
        fixo = (0.45, 0.48, 0.52, 1)
        dest = (0.76, 0.42, 0.20, 1)
        with self.canvas:
            if tipo == 'fixo':
                Color(*fixo); Rectangle(pos=(x, y), size=(w, h))
                Color(0.25, 0.27, 0.30, 1)
                Line(rectangle=(x + 1, y + 1, w - 2, h - 2), width=1.2)
                Line(points=[x, y + h * 0.5, x + w, y + h * 0.5], width=1)
                Line(points=[x + w * 0.5, y, x + w * 0.5, y + h], width=1)
                return
            elif tipo == 'dest':
                Color(*dest); Rectangle(pos=(x, y), size=(w, h))
                Color(0.45, 0.22, 0.08, 1)
                Line(points=[x, y + h * 0.5, x + w, y + h * 0.5], width=1)
                Line(points=[x + w * 0.5, y + h * 0.5, x + w * 0.5, y + h], width=1)
                return
            elif tipo == 'fogo':
                Color(1, 0.35, 0, 1); Rectangle(pos=(x, y), size=(w, h))
                Color(1, 0.95, 0.2, 1)
                Triangle(points=[x + w * 0.5, y + h * 0.92, x + w * 0.12, y + h * 0.08, x + w * 0.88, y + h * 0.08])
                return
            Color(*chao); Rectangle(pos=(x, y), size=(w, h))
            if tipo == 'player':
                Color(0.15, 0.45, 0.95, 1); Ellipse(pos=(x + w * 0.22, y + h * 0.08), size=(w * 0.56, h * 0.45))
                Color(1, 1, 1, 1); Ellipse(pos=(x + w * 0.16, y + h * 0.32), size=(w * 0.68, h * 0.58))
                Color(1, 0.3, 0.6, 1); Ellipse(pos=(x + w * 0.42, y + h * 0.86), size=(w * 0.16, h * 0.14))
                Color(1, 0.85, 0.70, 1); Rectangle(pos=(x + w * 0.28, y + h * 0.42), size=(w * 0.44, h * 0.32))
                Color(0, 0, 0, 1); Ellipse(pos=(x + w * 0.34, y + h * 0.52), size=(w * 0.09, h * 0.14)); Ellipse(pos=(x + w * 0.57, y + h * 0.52), size=(w * 0.09, h * 0.14))
            elif tipo == 'bomba':
                Color(0.08, 0.08, 0.10, 1); Ellipse(pos=(x + w * 0.18, y + h * 0.08), size=(w * 0.64, h * 0.64))
                Color(1, 1, 1, 0.8); Ellipse(pos=(x + w * 0.28, y + h * 0.46), size=(w * 0.14, h * 0.14))
                Color(1, 0.8, 0, 1); Line(points=[x + w * 0.5, y + h * 0.70, x + w * 0.76, y + h * 0.92], width=2)
                Color(1, 0.2, 0, 1); Ellipse(pos=(x + w * 0.68, y + h * 0.84), size=(w * 0.18, h * 0.18))
            elif tipo == 'inimigo':
                Color(0.95, 0.22, 0.35, 1); Ellipse(pos=(x + w * 0.14, y + h * 0.12), size=(w * 0.72, h * 0.76))
                Color(1, 1, 1, 1); Ellipse(pos=(x + w * 0.25, y + h * 0.48), size=(w * 0.20, h * 0.22)); Ellipse(pos=(x + w * 0.55, y + h * 0.48), size=(w * 0.20, h * 0.22))
                Color(0, 0, 0, 1); Ellipse(pos=(x + w * 0.31, y + h * 0.52), size=(w * 0.09, h * 0.12)); Ellipse(pos=(x + w * 0.61, y + h * 0.52), size=(w * 0.09, h * 0.12))
                Line(points=[x + w * 0.28, y + h * 0.28, x + w * 0.72, y + h * 0.28], width=1.5)

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
            Color(0.12, 0.14, 0.20, 1); Rectangle(pos=(x, y), size=(w, h))
            bx = x + espaco
            Color(0.15, 0.45, 0.95, 1); Ellipse(pos=(bx + lado * 0.2, cy + lado * 0.05), size=(lado * 0.6, lado * 0.45))
            Color(1, 1, 1, 1); Ellipse(pos=(bx + lado * 0.12, cy + lado * 0.30), size=(lado * 0.76, lado * 0.62))
            Color(1, 0.3, 0.6, 1); Ellipse(pos=(bx + lado * 0.42, cy + lado * 0.88), size=(lado * 0.16, lado * 0.15))
            Color(1, 0.85, 0.70, 1); Rectangle(pos=(bx + lado * 0.25, cy + lado * 0.42), size=(lado * 0.50, lado * 0.34))
            Color(0, 0, 0, 1); Ellipse(pos=(bx + lado * 0.32, cy + lado * 0.52), size=(lado * 0.10, lado * 0.16)); Ellipse(pos=(bx + lado * 0.58, cy + lado * 0.52), size=(lado * 0.10, lado * 0.16))
            bmx = bx + lado + espaco
            Color(0.05, 0.05, 0.07, 1); Ellipse(pos=(bmx + lado * 0.12, cy + lado * 0.08), size=(lado * 0.76, lado * 0.76))
            Color(1, 1, 1, 0.85); Ellipse(pos=(bmx + lado * 0.25, cy + lado * 0.54), size=(lado * 0.16, lado * 0.16))
            Color(1, 0.85, 0, 1); Line(points=[bmx + lado * 0.5, cy + lado * 0.82, bmx + lado * 0.80, cy + lado * 1.02], width=2.5)
            Color(1, 0.25, 0, 1); Ellipse(pos=(bmx + lado * 0.72, cy + lado * 0.94), size=(lado * 0.18, lado * 0.18))
            i1x = bmx + lado + espaco
            Color(1, 0.35, 0.55, 1); Ellipse(pos=(i1x + lado * 0.10, cy + lado * 0.10), size=(lado * 0.80, lado * 0.80))
            Color(1, 1, 1, 1); Ellipse(pos=(i1x + lado * 0.24, cy + lado * 0.50), size=(lado * 0.20, lado * 0.24)); Ellipse(pos=(i1x + lado * 0.56, cy + lado * 0.50), size=(lado * 0.20, lado * 0.24))
            Color(0, 0, 0, 1); Ellipse(pos=(i1x + lado * 0.30, cy + lado * 0.54), size=(lado * 0.09, lado * 0.14)); Ellipse(pos=(i1x + lado * 0.62, cy + lado * 0.54), size=(lado * 0.09, lado * 0.14))
            Line(points=[i1x + lado * 0.28, cy + lado * 0.28, i1x + lado * 0.72, cy + lado * 0.28], width=2)
            i2x = i1x + lado + espaco
            Color(0.25, 0.65, 1, 1); Rectangle(pos=(i2x + lado * 0.12, cy + lado * 0.12), size=(lado * 0.76, lado * 0.76))
            Color(1, 1, 1, 1); Ellipse(pos=(i2x + lado * 0.24, cy + lado * 0.50), size=(lado * 0.20, lado * 0.22)); Ellipse(pos=(i2x + lado * 0.56, cy + lado * 0.50), size=(lado * 0.20, lado * 0.22))
            Color(0, 0, 0, 1); Ellipse(pos=(i2x + lado * 0.30, cy + lado * 0.54), size=(lado * 0.09, lado * 0.12)); Ellipse(pos=(i2x + lado * 0.62, cy + lado * 0.54), size=(lado * 0.09, lado * 0.12))
            Line(points=[i2x + lado * 0.25, cy + lado * 0.30, i2x + lado * 0.75, cy + lado * 0.30], width=2)

class TelaInicial(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.musica = None
        layout = BoxLayout(orientation='vertical', padding=16, spacing=8)
        layout.add_widget(Label(text="CORANGE SOFTWARE", font_size='18sp', color=(0.4, 0.85, 1, 1), bold=True, size_hint_y=0.08))
        layout.add_widget(Label(text="BOMBERMAN", font_size='34sp', color=(1, 0.85, 0.1, 1), bold=True, size_hint_y=0.12))
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
            if self.musica is None:
                caminho = resource_find("nes.mp3")
                if not caminho: caminho = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nes.mp3")
                if os.path.exists(caminho): self.musica = SoundLoader.load(caminho)
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
        self.fase = 1
        self.pontos = 0
        self.vidas = 3
        self.player = [1, 1]; self.inimigos = []; self.bombas = []; self.fogos = []; self.mapa = []; self.blocos = []; self.game_over = False; self._event_inimigo = None
        root = BoxLayout(orientation='vertical', spacing=4, padding=4)
        self.lbl_info = Label(text="VIDAS: 3 - FASE 1/6", font_size='16sp', bold=True, size_hint_y=0.08, color=(1, 1, 1, 1))
        root.add_widget(self.lbl_info)
        self.grid = GridLayout(cols=self.COLUNAS, rows=self.LINHAS, spacing=1, size_hint_y=0.68)
        root.add_widget(self.grid)
        # --- CONTROLES CORRIGIDOS ---
        controles = BoxLayout(orientation='horizontal', spacing=8, size_hint_y=0.24)
        dpad = GridLayout(cols=3, rows=3, spacing=6)
        dpad.add_widget(Widget())
        b_cima = Button(text="CIMA", font_size='16sp', bold=True, background_color=(0.25, 0.25, 0.28, 1))
        b_cima.bind(on_release=lambda x: self.mover(-1, 0))
        dpad.add_widget(b_cima)
        dpad.add_widget(Widget())
        b_esq = Button(text="ESQ", font_size='16sp', bold=True, background_color=(0.25, 0.25, 0.28, 1))
        b_esq.bind(on_release=lambda x: self.mover(0, -1))
        dpad.add_widget(b_esq)
        dpad.add_widget(Widget())
        b_dir = Button(text="DIR", font_size='16sp', bold=True, background_color=(0.25, 0.25, 0.28, 1))
        b_dir.bind(on_release=lambda x: self.mover(0, 1))
        dpad.add_widget(b_dir)
        dpad.add_widget(Widget())
        b_baixo = Button(text="BAIXO", font_size='16sp', bold=True, background_color=(0.25, 0.25, 0.28, 1))
        b_baixo.bind(on_release=lambda x: self.mover(1, 0))
        dpad.add_widget(b_baixo)
        dpad.add_widget(Widget())
        controles.add_widget(dpad)
        acoes = BoxLayout(orientation='vertical', spacing=8)
        b_bomba = Button(text="BOMBA", font_size='28sp', bold=True, background_color=(0.95, 0.15, 0.15, 1), size_hint_y=0.7)
        b_bomba.bind(on_release=lambda x: self.colocar_bomba())
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
        elif key == 32: self.colocar_bomba()
        return True
    def iniciar_fase(self, fase):
        self.fase = fase
        self.game_over = False
        if fase == 1:
            self.vidas = 3
            self.pontos = 0
        self.player = [1, 1]; self.bombas = []; self.fogos = []; self.inimigos = []; self.mapa = []
        for l in range(self.LINHAS):
            linha = []
            for c in range(self.COLUNAS):
                if l == 0 or l == self.LINHAS-1 or c == 0 or c == self.COLUNAS-1: linha.append('fixo')
                elif l % 2 == 0 and c % 2 == 0: linha.append('fixo')
                elif random.random() < 0.45 and not (l < 3 and c < 3): linha.append('dest')
                else: linha.append('chao')
            self.mapa.append(linha)
        self.mapa[1][1] = 'chao'; self.mapa[1][2] = 'chao'; self.mapa[2][1] = 'chao'
        pos_livres = [(l, c) for l in range(1, self.LINHAS-1) for c in range(1, self.COLUNAS-1) if self.mapa[l][c] == 'chao' and not (l < 3 and c < 3)]
        random.shuffle(pos_livres)
        qtd = min(3 + fase, 6)
        for l, c in pos_livres[:qtd]: self.inimigos.append([l, c, random.choice([(1,0),(-1,0),(0,1),(0,-1)])])
        self.grid.clear_widgets(); self.blocos = []
        for l in range(self.LINHAS):
            linha_blocos = []
            for c in range(self.COLUNAS):
                b = Bloco(); self.grid.add_widget(b); linha_blocos.append(b)
            self.blocos.append(linha_blocos)
        self.atualizar_info()
        self.desenhar_mapa()
        if self._event_inimigo: self._event_inimigo.cancel()
        self._event_inimigo = Clock.schedule_interval(lambda dt: self.atualizar_inimigos(), 0.6)
    def atualizar_info(self):
        self.lbl_info.text = f"VIDAS: {self.vidas} - FASE {self.fase}/6 - {self.pontos} PTS"
    def desenhar_mapa(self):
        for l in range(self.LINHAS):
            for c in range(self.COLUNAS):
                tipo = self.mapa[l][c]
                for bl, bc, _ in self.bombas:
                    if bl == l and bc == c: tipo = 'bomba'
                for fl, fc in self.fogos:
                    if fl == l and fc == c: tipo = 'fogo'
                if [l, c] == self.player: tipo = 'player'
                for e in self.inimigos:
                    if e[0] == l and e[1] == c: tipo = 'inimigo'
                self.blocos[l][c].desenhar(tipo)
    def pode_andar(self, l, c):
        if l < 0 or l >= self.LINHAS or c < 0 or c >= self.COLUNAS: return False
        if self.mapa[l][c] in ('fixo', 'dest'): return False
        for bl, bc, _ in self.bombas:
            if bl == l and bc == c: return False
        return True
    def mover(self, dl, dc):
        if self.game_over: return
        nl, nc = self.player[0] + dl, self.player[1] + dc
        if not self.pode_andar(nl, nc): return
        self.player = [nl, nc]
        if [nl, nc] in self.fogos: self.perdeu(); return
        for e in self.inimigos:
            if e[0] == nl and e[1] == nc: self.perdeu(); return
        self.desenhar_mapa()
    def colocar_bomba(self):
        if self.game_over: return
        l, c = self.player
        for bl, bc, _ in self.bombas:
            if bl == l and bc == c: return
        self.bombas.append([l, c, 1.5]); self.desenhar_mapa()
        Clock.schedule_once(lambda dt: self.explodir(l, c), 1.5)
    def explodir(self, l, c):
        if self.game_over: return
        tocar_bip('bip_boom.wav')
        self.bombas = [b for b in self.bombas if not (b[0] == l and b[1] == c)]
        novos_fogos = [(l, c)]
        for dl, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            for i in [1, 2]:
                nl, nc = l + dl*i, c + dc*i
                if nl < 0 or nl >= self.LINHAS or nc < 0 or nc >= self.COLUNAS: break
                if self.mapa[nl][nc] == 'fixo': break
                novos_fogos.append((nl, nc))
                if self.mapa[nl][nc] == 'dest': self.mapa[nl][nc] = 'chao'; break
        self.fogos.extend(novos_fogos)
        antes = len(self.inimigos)
        self.inimigos = [e for e in self.inimigos if (e[0], e[1]) not in novos_fogos]
        mortos = antes - len(self.inimigos)
        if mortos > 0:
            tocar_bip('bip_bicho.wav')
            self.pontos += mortos * 100
            self.atualizar_info()
        self.desenhar_mapa()
        if tuple(self.player) in novos_fogos:
            Clock.schedule_once(lambda dt: self.perdeu(), 0.3)
        elif len(self.inimigos) == 0:
            Clock.schedule_once(lambda dt: self.venceu_fase(), 0.6)
        Clock.schedule_once(lambda dt: self.limpar_fogo(novos_fogos), 0.7)
    def limpar_fogo(self, lista):
        for f in lista:
            if f in self.fogos: self.fogos.remove(f)
        if not self.game_over: self.desenhar_mapa()
    def atualizar_inimigos(self):
        if self.game_over or self.manager.current != 'jogo': return
        for e in self.inimigos:
            dl, dc = e[2]
            nl, nc = e[0] + dl, e[1] + dc
            if not self.pode_andar(nl, nc) or [nl, nc] in self.fogos: e[2] = random.choice([(1,0),(-1,0),(0,1),(0,-1)])
            else: e[0], e[1] = nl, nc
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
            self.lbl_info.text = f"VOCE PERDEU! {self.pontos} PTS - Aperte VOLTAR"
            self.desenhar_mapa()
        else:
            self.player = [1, 1]
            self.bombas = []
            self.fogos = []
            self.atualizar_info()
            self.desenhar_mapa()
    def venceu_fase(self):
        if self.game_over: return
        self.game_over = True; tocar_bip('bip_venceu.wav')
        self.pontos += 200
        salvar_recorde(self.fase, self.pontos)
        if self._event_inimigo: self._event_inimigo.cancel()
        if self.fase >= 6:
            self.lbl_info.text = f"ZEROU! {self.pontos} PTS!"
            Clock.schedule_once(lambda dt: self.voltar_menu(), 2.5)
        else:
            self.lbl_info.text = f"FASE {self.fase} OK! {self.pontos} PTS"
            Clock.schedule_once(lambda dt: self.iniciar_fase(self.fase + 1), 1.5)
    def voltar_menu(self):
        if self._event_inimigo: self._event_inimigo.cancel()
        self.manager.current = 'inicio'

class BombermanApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(TelaInicial(name='inicio'))
        sm.add_widget(TelaJogo(name='jogo'))
        return sm

if __name__ == '__main__':
    BombermanApp().run()
