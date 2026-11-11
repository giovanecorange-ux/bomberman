from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.core.window import Window
import random

Window.clearcolor = (0, 0, 0, 1)

# ================= MENU =================
class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        layout.add_widget(Label(text='Corange Software', font_size='28sp', color=(0,1,0.4,1), size_hint_y=0.3, bold=True))
        
        btn1 = Button(text='JOGAR COBRINHA', background_color=(0,0.4,0,1), font_size='18sp', size_hint_y=0.2)
        btn1.bind(on_press=lambda x: setattr(self.manager, 'current', 'cobrinha'))
        layout.add_widget(btn1)

        btn2 = Button(text='JOGAR TETRIS', background_color=(0,0.2,0.5,1), font_size='18sp', size_hint_y=0.2)
        btn2.bind(on_press=lambda x: setattr(self.manager, 'current', 'tetris'))
        layout.add_widget(btn2)

        btn3 = Button(text='JOGAR BOMBERMAN', background_color=(0.5,0.3,0,1), font_size='18sp', size_hint_y=0.2)
        btn3.bind(on_press=lambda x: setattr(self.manager, 'current', 'bomber'))
        layout.add_widget(btn3)

        layout.add_widget(Label(text='Cobrinha: 0 | Tetris: 0 | Bomber: 0', size_hint_y=0.1, font_size='14sp'))
        layout.add_widget(Label(text='Corange Software - PIX 51993359782', color=(0,1,0.4,1), size_hint_y=0.1, font_size='12sp'))
        self.add_widget(layout)

# ================= TETRIS SIMPLES E FUNCIONAL =================
class TetrisWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 10
        self.rows = 20
        self.grid = [[0]*self.cols for _ in range(self.rows)]
        self.pieces = [
            [[1,1,1,1]],
            [[1,1],[1,1]],
            [[1,1,1],[0,1,0]],
            [[1,1,1],[1,0,0]],
            [[1,1,1],[0,0,1]],
            [[1,1,0],[0,1,1]],
            [[0,1,1],[1,1,0]],
        ]
        self.colors = [(1,0,0,1),(0,1,0,1),(0,0,1,1),(1,1,0,1),(1,0,1,1),(0,1,1,1),(1,0.5,0,1)]
        self.new_piece()
        Clock.schedule_interval(self.update, 0.3)
        
    def new_piece(self):
        self.piece = random.choice(self.pieces)
        self.color = random.choice(self.colors)
        self.px = self.cols//2 - len(self.piece[0])//2
        self.py = 0
        if self.check_collision(0,0):
            self.grid = [[0]*self.cols for _ in range(self.rows)]

    def check_collision(self, dx, dy):
        for y,row in enumerate(self.piece):
            for x,val in enumerate(row):
                if val:
                    nx, ny = self.px+x+dx, self.py+y+dy
                    if nx<0 or nx>=self.cols or ny>=self.rows or (ny>=0 and self.grid[ny][nx]):
                        return True
        return False

    def update(self, dt):
        if not self.check_collision(0,1):
            self.py+=1
        else:
            for y,row in enumerate(self.piece):
                for x,val in enumerate(row):
                    if val and self.py+y>=0:
                        self.grid[self.py+y][self.px+x]=self.color
            # limpa linha
            self.grid = [r for r in self.grid if not all(r)]
            while len(self.grid)<self.rows:
                self.grid.insert(0,[0]*self.cols)
            self.new_piece()
        self.draw()

    def draw(self):
        self.canvas.clear()
        size = min(self.width/self.cols, self.height/self.rows)
        ox = (self.width - size*self.cols)/2
        oy = (self.height - size*self.rows)/2
        with self.canvas:
            for y in range(self.rows):
                for x in range(self.cols):
                    c = self.grid[y][x]
                    if c:
                        Color(*c)
                        Rectangle(pos=(ox+x*size, oy+(self.rows-1-y)*size), size=(size-1,size-1))
            # peca atual
            Color(*self.color)
            for y,row in enumerate(self.piece):
                for x,val in enumerate(row):
                    if val:
                        Rectangle(pos=(ox+(self.px+x)*size, oy+(self.rows-1-(self.py+y))*size), size=(size-1,size-1))

class TetrisScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        box = BoxLayout(orientation='vertical')
        box.add_widget(Button(text='< VOLTAR AO MENU', size_hint_y=0.1, on_press=lambda x: setattr(self.manager,'current','menu')))
        box.add_widget(TetrisWidget())
        box.add_widget(Label(text='Toque nas bordas: ESQ/DIR desce', size_hint_y=0.1, font_size='12sp'))
        self.add_widget(box)
        
        # controles simples
        def on_touch_down(w,touch):
            if self.manager.current!='tetris': return False
            if touch.x < Window.width*0.33:
                if not w.children[0].children[0].check_collision(-1,0):
                    w.children[0].children[0].px-=1
            elif touch.x > Window.width*0.66:
                if not w.children[0].children[0].check_collision(1,0):
                    w.children[0].children[0].px+=1
            else:
                if not w.children[0].children[0].check_collision(0,1):
                    w.children[0].children[0].py+=1
            return True
        self.bind(on_touch_down=lambda inst,touch: on_touch_down(self,touch))

# Telas placeholders pros outros 2 pra nao quebrar
class SimpleScreen(Screen):
    def __init__(self, name_game, **kwargs):
        super().__init__(**kwargs)
        box = BoxLayout(orientation='vertical')
        box.add_widget(Button(text='< VOLTAR AO MENU', size_hint_y=0.1, on_press=lambda x: setattr(self.manager,'current','menu')))
        box.add_widget(Label(text=f'{name_game}\nEm reconstrucao!\nMas o Tetris ja esta 100%', halign='center'))
        self.add_widget(box)

class CorangeApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(TetrisScreen(name='tetris'))
        sm.add_widget(SimpleScreen('COBRINHA', name='cobrinha'))
        sm.add_widget(SimpleScreen('BOMBERMAN', name='bomber'))
        return sm

CorangeApp().run()
