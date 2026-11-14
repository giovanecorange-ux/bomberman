import os
import random
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


class Bloco(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tipo = 'chao'
        self.bind(pos=self._redesenhar, size=self._redesenhar)

    def _redesenhar(self, *args):
        self.desenhar(self.tipo)

    def desenhar(self, tipo):
        self.tipo = tipo
        self.canvas.clear()
        x, y = self.pos
        w, h = self.size
        if w <= 1 or h <= 1:
            return

        chao = (0.20, 0.68, 0.22, 1)
        fixo = (0.45, 0.48, 0.52, 1)
        dest = (0.76, 0.42, 0.20, 1)

        with self.canvas:
            if tipo == 'fixo':
                Color(*fixo)
                Rectangle(pos=(x, y), size=(w, h))
                Color(0.25, 0.27, 0.30, 1)
                Line(rectangle=(x + 1, y + 1, w - 2, h - 2), width=1.2)
                Line(points=[x, y + h * 0.5, x + w, y + h * 0.5], width=1)
                Line(points=[x + w * 0.5, y, x + w * 0.5, y + h], width=1)
                return
            elif tipo == 'dest':
                Color(*dest)
                Rectangle(pos=(x, y), size=(w, h))
                Color(0.45, 0.22, 0.08, 1)
                Line(points=[x, y + h * 0.5, x + w, y + h * 0.5], width=1)
                Line(points=[x + w * 0.5, y + h * 0.5, x + w * 0.5, y + h], width=1)
                Line(points=[x + w * 0.25, y, x + w * 0.25, y + h * 0.5], width=1)
                Line(points=[x + w * 0.75, y, x + w * 0.75, y + h * 0.5], width=1)
                return
            elif tipo == 'fogo':
                Color(1, 0.35, 0, 1)
                Rectangle(pos=(x, y), size=(w, h))
                Color(1, 0.95, 0.2, 1)
                Triangle(points=[x + w * 0.5, y + h * 0.92, x + w * 0.12, y + h * 0.08, x + w * 0.88, y + h * 0.08])
                return

            Color(*chao)
            Rectangle(pos=(x, y), size=(w, h))

            if tipo == 'player':
                Color(0.15, 0.45, 0.95, 1)
                Ellipse(pos=(x + w * 0.22, y + h * 0.08), size=(w * 0.56, h * 0.45))
                Color(1, 1, 1, 1)
                Ellipse(pos=(x + w * 0.16, y + h * 0.32), size=(w * 0.68, h * 0.58))
                Color(1, 0.3, 0.6, 1)
                Ellipse(pos=(x + w * 0.42, y + h * 0.86), size=(w * 0.16, h * 0.14))
                Color(1, 0.85, 0.70, 1)
                Rectangle(pos=(x + w * 0.28, y + h * 0.42), size=(w * 0.44, h * 0.32))
                Color(0, 0, 0, 1)
                Ellipse(pos=(x + w * 0.34, y + h * 0.52), size=(w * 0.09, h * 0.14))
                Ellipse(pos=(x + w * 0.57, y + h * 0.52), size=(w * 0.09, h * 0.14))

            elif tipo == 'bomba':
                Color(0.08, 0.08, 0.10, 1)
                Ellipse(pos=(x + w * 0.18, y + h * 0.08), size=(w * 0.64, h * 0.64))
                Color(1, 1, 1, 0.8)
                Ellipse(pos=(x + w * 0.28, y + h * 0.46), size=(w * 0.14, h * 0.14))
                Color(1, 0.8, 0, 1)
                Line(points=[x + w * 0.5, y + h * 0.70, x + w * 0.76, y + h * 0.92], width=2)
                Color(1, 0.2, 0, 1)
                Ellipse(pos=(x + w * 0.68, y + h * 0.84), size=(w * 0.18, h * 0.18))

            elif tipo == 'inimigo':
                Color(0.95, 0.22, 0.35, 1)
                Ellipse(pos=(x + w * 0.14, y + h * 0.12), size=(w * 0.72, h * 0.76))
                Color(1, 1, 1, 1)
                Ellipse(pos=(x + w * 0.25, y + h * 0.48), size=(w * 0.20, h * 0.22))
                Ellipse(pos=(x + w * 0.55, y + h * 0.48), size=(w * 0.20, h * 0.22))
                Color(0, 0, 0, 1)
                Ellipse(pos=(x + w * 0.31, y + h * 0.52), size=(w * 0.09, h * 0.12))
                Ellipse(pos=(x + w * 0.61, y + h * 0.52), size=(w * 0.09, h * 0.12))
                Line(points=[x + w * 0.28, y + h * 0.28, x + w * 0.72, y + h * 0.28], width=1.5)


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
            Color(0.12, 0.14, 0.20, 1)
            Rectangle(pos=(x, y), size=(w, h))

            # 1. Bomberman
            bx = x + espaco
            Color(0.15, 0.45, 0.95, 1)
            Ellipse(pos=(bx + lado * 0.2, cy + lado * 0.05), size=(lado * 0.6, lado * 0.45))
            Color(1, 1, 1, 1)
            Ellipse(pos=(bx + lado * 0.12, cy + lado * 0.30), size=(lado * 0.76, lado * 0.62))
            Color(1, 0.3, 0.6, 1)
            Ellipse(pos=(bx + lado * 0.42, cy + lado * 0.88), size=(lado * 0.16, lado * 0.15))
            Color(1, 0.85, 0.70, 1)
            Rectangle(pos=(bx + lado * 0.25, cy + lado * 0.42), size=(lado * 0.50, lado * 0.34))
            Color(0, 0, 0, 1)
            Ellipse(pos=(bx + lado * 0.32, cy + lado * 0.52), size=(lado * 0.10, lado * 0.16))
            Ellipse(pos=(bx + lado * 0.58, cy + lado * 0.52), size=(lado * 0.10, lado * 0.16))

            # 2. Bomba
            bmx = bx + lado + espaco
            Color(0.05, 0.05, 0.07, 1)
            Ellipse(pos=(bmx + lado * 0.12, cy + lado * 0.08), size=(lado * 0.76, lado * 0.76))
            Color(1, 1, 1, 0.85)
            Ellipse(pos=(bmx + lado * 0.25, cy + lado * 0.54), size=(lado * 0.16, lado * 0.16))
            Color(1, 0.85, 0, 1)
            Line(points=[bmx + lado * 0.5, cy + lado * 0.82, bmx + lado * 0.80, cy + lado * 1.02], width=2.5)
            Color(1, 0.25, 0, 1)
            Ellipse(pos=(bmx + lado * 0.72, cy + lado * 0.94), size=(lado * 0.18, lado * 0.18))

            # 3. Inimigo Rosa
            i1x = bmx + lado + espaco
            Color(1, 0.35, 0.55, 1)
            Ellipse(pos=(i1x + lado * 0.10, cy + lado * 0.10), size=(lado * 0.80, lado * 0.80))
            Color(1, 1, 1, 1)
            Ellipse(pos=(i1x + lado * 0.24, cy + lado * 0.50), size=(lado * 0.20, lado * 0.24))
            Ellipse(pos=(i1x + lado * 0.56, cy + lado * 0.50), size=(lado * 0.20, lado * 0.24))
            Color(0, 0, 0, 1)
            Ellipse(pos=(i1x + lado * 0.30, cy + lado * 0.54), size=(lado * 0.09, lado * 0.14))
            Ellipse(pos=(i1x + lado * 0.62, cy + lado * 0.54), size=(lado * 0.09, lado * 0.14))
            Line(points=[i1x + lado * 0.28, cy + lado * 0.28, i1x + lado * 0.72, cy + lado * 0.28], width=2)

            # 4. Inimigo Azul
            i2x = i1x + lado + espaco
            Color(0.25, 0.65, 1, 1)
            Rectangle(pos=(i2x + lado * 0.12, cy + lado * 0.12), size=(lado * 0.76, lado * 0.76))
            Color(1, 1, 1, 1)
            Ellipse(pos=(i2x + lado * 0.24, cy + lado * 0.50), size=(lado * 0.20, lado * 0.22))
            Ellipse(pos=(i2x + lado * 0.56, cy + lado * 0.50), size=(lado * 0.20, lado * 0.22))
            Color(0, 0, 0, 1)
            Ellipse(pos=(i2x + lado * 0.30, cy + lado * 0.54), size=(lado * 0.09, lado * 0.12))
            Ellipse(pos=(i2x + lado * 0.62, cy + lado * 0.54), size=(lado * 0.09, lado * 0.12))
            Line(points=[i2x + lado * 0.25, cy + lado * 0.30, i2x + lado * 0.75, cy + lado * 0.30], width=2)


class TelaInicial(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.musica = None

        layout = BoxLayout(orientation='vertical', padding=16, spacing=10)

        layout.add_widget(Label(
            text="CORANGE SOFTWARE",
            font_size='18sp',
            color=(0.4, 0.85, 1, 1),
            bold=True,
            size_hint_y=0.08
        ))

        layout.add_widget(Label(
            text="BOMBERMAN",
            font_size='34sp',
            color=(1, 0.85, 0.1, 1),
            bold=True,
            size_hint_y=0.14
        ))

        layout.add_widget(DesenhoCapa(size_hint_y=0.38))

        btn_iniciar = Button(
            text="INICIAR JOGO",
            font_size='24sp',
            bold=True,
            background_color=(0.15, 0.75, 0.25, 1),
            size_hint_y=0.18
        )
        btn_iniciar.bind(on_release=self.ir_para_jogo)
        layout.add_widget(btn_iniciar)

        layout.add_widget(Label(
            text="PIX: 51993359782",
            font_size='16sp',
            color=(0.3, 1, 0.45, 1),
            bold=True,
            size_hint_y=0.10
        ))

        self.add_widget(layout)

    def on_enter(self):
        self.tocar_musica()

    def on_leave(self):
        self.parar_musica()

    def tocar_musica(self):
        try:
            if self.musica is None:
                caminho = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nes.mp3")
                if os.path.exists(caminho):
                    self.musica = SoundLoader.load(caminho)
            if self.musica:
                self.musica.loop = True
                self.musica.play()
        except Exception:
            pass

    def parar_musica(self):
        try:
            if self.musica:
                self.musica.stop()
        except Exception:
            pass

    def ir_para_jogo(self, *args):
        self.parar_musica()
        self.manager.get_screen('jogo').iniciar_fase(1)
        self.manager.current = 'jogo'


class TelaJogo(Screen):
    LINHAS = 11
    COLUNAS = 11

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fase = 1
        self.player = [1, 1]
        self.inimigos = []
