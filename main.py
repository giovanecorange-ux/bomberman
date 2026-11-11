from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.clock import Clock
from kivy.core.window import Window
import random, math, struct, wave, os, tempfile
Window.clearcolor = (0, 0, 0, 1)
PIX = "51993359782"

def carregar(arq):
    try:
        if os.path.exists(arq):
            with open(arq, "r") as f:
                return int(f.read().strip())
    except:
        pass
    return 0

def salvar(arq, v):
    try:
        with open(arq, "w") as f:
            f.write(str(v))
    except:
        pass

music = None
music_on = False
beeps = {}

def get_beep(freq, ms, name):
    try:
        from kivy.core.audio import SoundLoader
        if name in beeps:
            return beeps[name]
        path = os.path.join(tempfile.gettempdir(), name + ".wav")
        if not os.path.exists(path):
            sr = 8000
            n = int(sr * ms / 1000)
            d = bytearray()
            for i in range(n):
                d += struct.pack('<h', int(8000 * math.sin(2 * math.pi * freq * i / sr)))
            with wave.open(path, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(sr)
                wf.writeframes(bytes(d))
        s = SoundLoader.load(path)
        beeps[name] = s
        return s
    except:
        return None

def play_music(dt=None):
    global music, music_on
    if music_on:
        return
    try:
        from kivy.core.audio import SoundLoader
        m = SoundLoader.load('nes.mp3')
        if m is None:
            m = SoundLoader.load('nes.wav')
        if m:
            m.volume = 0.7
            m.play()
            music = m
            music_on = True
    except:
        pass

def stop_music():
    global music_on
    try:
        if music:
            music.stop()
        music_on = False
    except:
        pass

def beep(name):
    try:
        s = beeps.get(name)
        if s:
            s.play()
    except:
        pass

def init_beeps():
    get_beep(400, 80, "mv")
    get_beep(1200, 120, "rot")
    get_beep(300, 50, "down")
    get_beep(900, 150, "eat")
    get_beep(800, 100, "eat2")
    get_beep(120, 500, "over")
    get_beep(300, 80, "bomb")
    get_beep(1000, 80, "coin")

class MenuScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        lay = BoxLayout(orientation='vertical', padding=15, spacing=10)
        lay.add_widget(Label(text='Bomberman Corange', font_size=30, bold=True, color=(1, 0.8, 0, 1)))
        lay.add_widget(Label(text='Corange Sistemas', font_size=18, bold=True))
        lay.add_widget(Label(text='PIX ' + PIX, font_size=16, bold=True, color=(0.3, 1, 0.22, 1)))
        for txt, nome, col in [('TETRIS', 'tetris', (1, 0, 0, 1)), ('COBRINHA', 'cobra', (0, 1, 0.4, 1)), ('BOMBERMAN 6 FASES', 'bomber', (1, 0.8, 0, 1))]:
            b = Button(text=txt, font_size=22, bold=True, background_color=col, size_hint_y=0.22)
            b.bind(on_press=lambda x, n=nome: setattr(self.manager, 'current', n))
            lay.add_widget(b)
        self.lb_rec = Label(text='', font_size=14, bold=True, color=(1, 0.8, 0, 1))
        lay.add_widget(self.lb_rec)
        lay.add_widget(Label(text='Corange Sistemas - PIX ' + PIX, font_size=11, color=(0, 1, 0.4, 1)))
        self.add_widget(lay)
    def on_enter(self):
        self.lb_rec.text = "REC Tetris: %s  |  REC Cobrinha: %s  |  REC Bomber: %s" % (carregar('recorde_tetris.txt'), carregar('recorde_cobrinha.txt'), carregar('recorde.txt'))
        Clock.schedule_once(play_music, 0.2)
        Clock.schedule_once(lambda dt: init_beeps(), 1.0)

class BaseScreen(Screen):
    def top_bar(self):
        b = Button(text='< VOLTAR AO MENU', size_hint_y=0.07, background_color=(0.3, 0.3, 0.3, 1))
        b.bind(on_press=lambda x: setattr(self.manager, 'current', 'menu'))
        return b
    def ctrls(self, L, R, U, D, extra=None, et='BOMBA'):
        c = BoxLayout(size_hint_y=0.22, spacing=6, padding=6)
        bL = Button(text='<', font_size=32, bold=True)
        bR = Button(text='>', font_size=32, bold=True)
        bO = Button(text='O', font_size=28, bold=True)
        bV = Button(text='V', font_size=28, bold=True)
        bL.bind(on_press=lambda x: L())
        bR.bind(on_press=lambda x: R())
        bO.bind(on_press=lambda x: U())
        bV.bind(on_press=lambda x: D())
        c.add_widget(bL)
        m = BoxLayout(orientation='vertical', spacing=6)
        m.add_widget(bO)
        m.add_widget(bV)
        c.add_widget(m)
        c.add_widget(bR)
        if extra:
            be = Button(text=et, bold=True, background_color=(0.4, 0.2, 0.8, 1))
            be.bind(on_press=lambda x: extra())
            c.add_widget(be)
        return c
    def on_enter(self):
        stop_music()

PECAS = [[[1, 1, 1, 1]], [[1, 1, 1], [0, 1, 0]], [[1, 1, 0], [0, 1, 1]], [[0, 1, 1], [1, 1, 0]], [[1, 1], [1, 1]], [[1, 1, 1], [1, 0, 0]], [[1, 1, 1], [0, 0, 1]]]
CORES = [(1, 0, 0, 1), (0, 1, 0, 1), (0, 0.47, 1, 1), (1, 1, 0, 1), (1, 0, 1, 1), (0, 1, 1, 1), (1, 0.55, 0, 1)]

class TBoard(Widget):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.cols = 10
        self.rows = 20
        self.grid = [[None] * 10 for _ in range(20)]
        self.score = 0
        self.recorde = carregar('recorde_tetris.txt')
        self.timer = 0
        self.sp()
        Clock.schedule_interval(self.tk, 1 / 30)
        self.bind(size=self.dr, pos=self.dr)
    def sp(self):
        i = random.randint(0, 6)
        self.sh = PECAS[i]
        self.co = CORES[i]
        self.x = 4
        self.y = 0
    def col(self, dx, dy, sh=None):
        if sh is None:
            sh = self.sh
        for yy, r in enumerate(sh):
            for xx, v in enumerate(r):
                if v:
                    nx = self.x + xx + dx
                    ny = self.y + yy + dy
                    if nx < 0 or nx >= self.cols or ny >= self.rows:
                        return True
                    if ny >= 0 and self.grid[ny][nx]:
                        return True
        return False
    def tk(self, dt):
        self.timer += 1
        if self.timer > 18:
            self.timer = 0
            if not self.col(0, 1):
                self.y += 1
            else:
                for yy, r in enumerate(self.sh):
                    for xx, v in enumerate(r):
                        if v and self.y + yy < self.rows:
                            self.grid[self.y + yy][self.x + xx] = self.co
                ng = [row for row in self.grid if any(c is None for c in row)]
                cl = self.rows - len(ng)
                if cl:
                    self.score += cl * 100
                    beep("eat")
                while len(ng) < self.rows:
                    ng.insert(0, [None] * self.cols)
                self.grid = ng
                self.sp()
                if self.col(0, 0):
                    beep("over")
                    if self.score > self.recorde:
                        self.recorde = self.score
                        salvar('recorde_tetris.txt', self.recorde)
                    self.grid = [[None] * 10 for _ in range(20)]
                    self.score = 0
        self.dr()
    def dr(self, *a):
        self.canvas.clear()
        if self.width < 10:
            return
        cw = self.width / self.cols
        ch = self.height / self.rows
        with self.canvas:
            for y in range(self.rows):
                for x in range(self.cols):
                    Color(0.06, 0.06, 0.1, 1)
                    Rectangle(pos=(self.x + x * cw, self.y + (self.rows - 1 - y) * ch), size=(cw - 1, ch - 1))
                    if self.grid[y][x]:
                        Color(*self.grid[y][x])
                        Rectangle(pos=(self.x + x * cw + 1, self.y + (self.rows - 1 - y) * ch + 1), size=(cw - 2, ch - 2))
            for yy, r in enumerate(self.sh):
                for xx, v in enumerate(r):
                    if v:
                        Color(*self.co)
                        Rectangle(pos=(self.x + (self.x + xx) * cw + 1, self.y + (self.rows - 1 - (self.y + yy)) * ch + 1), size=(cw - 2, ch - 2))

class TScreen(BaseScreen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.main = BoxLayout(orientation='vertical')
        self.main.add_widget(self.top_bar())
        self.lb = Label(text='Score: 0 Rec: 0', size_hint_y=0.07, bold=True)
        self.main.add_widget(self.lb)
        self.add_widget(self.main)
        self.board = None
    def on_enter(self):
        super().on_enter()
        if not self.board:
            self.board = TBoard()
            self.main.add_widget(self.board, index=1)
            ctrl = self.ctrls(lambda: self.mv(-1), lambda: self.mv(1), lambda: self.rt(), lambda: self.dn())
            self.main.add_widget(ctrl, index=0)
            self.main.add_widget(Label(text='Corange Sistemas - PIX ' + PIX, size_hint_y=0.05, color=(0, 1, 0.4, 1), font_size=11), index=0)
            Clock.schedule_interval(self.upd, 0.1)
    def upd(self, dt):
        self.lb.text = 'Score: %s Rec: %s' % (self.board.score, self.board.recorde)
    def mv(self, d):
        if not self.board.col(d, 0):
            self.board.x += d
            self.board.dr()
            beep("mv")
    def dn(self):
        if not self.board.col(0, 1):
            self.board.y += 1
            self.board.dr()
            beep("down")
    def rt(self):
        beep("rot")
        ns = [list(r) for r in zip(*self.board.sh[::-1])]
        if not self.board.col(0, 0, ns):
            self.board.sh = ns
            self.board.dr()

class CBoard(Widget):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.cols = 30
        self.rows = 20
        self.rs()
        Clock.schedule_interval(self.tk, 0.10)
        self.bind(size=self.dr, pos=self.dr)
    def rs(self):
        self.sn = [(15, 10), (14, 10), (13, 10)]
        self.di = (1, 0)
        self.sc = 0
        self.recorde = carregar('recorde_cobrinha.txt')
        self.nf()
    def nf(self):
        while True:
            f = (random.randint(0, self.cols - 1), random.randint(0, self.rows - 1))
            if f not in self.sn:
                self.fr = f
                break
    def tk(self, dt):
        hx, hy = self.sn[0]
        nx = hx + self.di[0]
        ny = hy + self.di[1]
        if nx < 0 or nx >= self.cols or ny < 0 or ny >= self.rows or (nx, ny) in self.sn:
            beep("over")
            if self.sc > self.recorde:
                self.recorde = self.sc
                salvar('recorde_cobrinha.txt', self.recorde)
            self.rs()
            return
        self.sn.insert(0, (nx, ny))
        if (nx, ny) == self.fr:
            self.sc += 10
            beep("eat2")
            self.nf()
        else:
            self.sn.pop()
        self.dr()
    def dr(self, *a):
        self.canvas.clear()
        if self.width < 10:
            return
        cw = self.width / self.cols
        ch = self.height / self.rows
        with self.canvas:
            for y in range(self.rows):
                for x in range(self.cols):
                    Color(0.06, 0.06, 0.1, 1)
                    Rectangle(pos=(self.x + x * cw, self.y + (self.rows - 1 - y) * ch), size=(cw - 1, ch - 1))
            Color(1, 0, 0, 1)
            Ellipse(pos=(self.x + self.fr[0] * cw + 2, self.y + (self.rows - 1 - self.fr[1]) * ch + 2), size=(cw - 4, ch - 4))
            for i, (x, y) in enumerate(self.sn):
                if i == 0:
                    Color(0.2, 0.47, 1, 1)
                else:
                    Color(0, 1, 0.4, 1)
                Rectangle(pos=(self.x + x * cw + 2, self.y + (self.rows - 1 - y) * ch + 2), size=(cw - 4, ch - 4))

class CScreen(BaseScreen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.main = BoxLayout(orientation='vertical')
        self.main.add_widget(self.top_bar())
        self.lb = Label(text='Score: 0 Rec: 0', size_hint_y=0.07, bold=True)
        self.main.add_widget(self.lb)
        self.add_widget(self.main)
        self.board = None
    def on_enter(self):
        super().on_enter()
        if not self.board:
            self.board = CBoard()
            self.main.add_widget(self.board, index=1)
            ctrl = self.ctrls(lambda: self.sd((-1, 0)), lambda: self.sd((1, 0)), lambda: self.sd((0, -1)), lambda: self.sd((0, 1)))
            self.main.add_widget(ctrl, index=0)
            self.main.add_widget(Label(text='Corange Sistemas - PIX ' + PIX, size_hint_y=0.05, color=(0, 1, 0.4, 1), font_size=11), index=0)
            Clock.schedule_interval(self.upd, 0.1)
    def upd(self, dt):
        self.lb.text = 'Score: %s Rec: %s' % (self.board.sc, self.board.recorde)
    def sd(self, d):
        if (d[0] * -1, d[1] * -1) != self.board.di:
            self.board.di = d

class BBoard(Widget):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.cols = 13
        self.rows = 11
        self.vidas = 3
        self.pontos = 0
        self.fase = 1
        self.recorde = carregar('recorde.txt')
        self.invencivel = 0
        self.setup()
        Clock.schedule_interval(self.tk, 0.085)
        self.bind(size=self.dr, pos=self.dr)
    def setup(self):
        self.pl = [1, 1]
        self.bombs = []
        self.fires = []
        self.coins = []
        self.grid = []
        for y in range(self.rows):
            row = []
            for x in range(self.cols):
                if x == 0 or y == 0 or x == self.cols - 1 or y == self.rows - 1 or (x % 2 == 0 and y % 2 == 0):
                    row.append(1)
                elif (x < 3 and y < 3) or (x > self.cols - 4 and y < 3) or (x < 3 and y > self.rows - 4) or (x > self.cols - 4 and y > self.rows - 4):
                    row.append(0)
                elif random.random() < 0.30:
                    row.append(2)
                else:
                    row.append(0)
            self.grid.append(row)
        qtd = 3 + (self.fase - 1)
        ps = [[11, 1], [11, 9], [1, 9], [11, 5], [1, 5], [6, 9], [11, 3], [1, 3]]
        self.ens = [[ps[i][0], ps[i][1], i % 3, -1, 0, 0] for i in range(min(qtd, len(ps)))]
    def perder_vida(self):
        beep("over")
        self.vidas -= 1
        if self.vidas <= 0:
            if self.pontos > self.recorde:
                self.recorde = self.pontos
                salvar('recorde.txt', self.recorde)
            self.vidas = 3
            self.pontos = 0
            self.fase = 1
            self.setup()
        else:
            self.pl = [1, 1]
            self.invencivel = 25
            self.bombs.clear()
            self.fires.clear()
    def move(self, dx, dy):
        nx = self.pl[0] + dx
        ny = self.pl[1] + dy
        if 0 <= nx < self.cols and 0 <= ny < self.rows and self.grid[ny][nx] == 0 and not any(e[0] == nx and e[1] == ny for e in self.ens):
            self.pl = [nx, ny]
            beep("mv")
            for c in self.coins[:]:
                if c[0] == nx and c[1] == ny:
                    self.pontos += 100
                    self.coins.remove(c)
                    beep("coin")
                if self.pontos > self.recorde:
                    self.recorde = self.pontos
                    salvar('recorde.txt', self.recorde)
        self.dr()
    def bomb(self):
        x, y = self.pl
        if len(self.bombs) < 2 and not any(b[0] == x and b[1] == y for b in self.bombs):
            self.bombs.append([x, y, 28])
            beep("bomb")
    def tk(self, dt):
        if self.invencivel > 0:
            self.invencivel -= 1
        for b in self.bombs[:]:
            b[2] -= 1
            if b[2] <= 0:
                x, y, _ = b
                pts = [[x, y]]
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    for i in range(1, 3):
                        nx = x + dx * i
                        ny = y + dy * i
                        if not (0 <= nx < self.cols and 0 <= ny < self.rows):
                            break
                        if self.grid[ny][nx] == 1:
                            break
                        pts.append([nx, ny])
                        if self.grid[ny][nx] == 2:
                            self.grid[ny][nx] = 0
                            if random.random() < 0.40:
                                tipo = 1 if random.random() < 0.30 else 0
                                if not any(m[0] == nx and m[1] == ny for m in self.coins):
                                    self.coins.append([nx, ny, tipo])
                            break
                beep("bomb")
                for fx, fy in pts:
                    self.fires.append([fx, fy, 12])
                    if fx == self.pl[0] and fy == self.pl[1] and self.invencivel == 0:
                        self.perder_vida()
                    self.ens = [e for e in self.ens if not (e[0] == fx and e[1] == fy)]
                self.bombs.remove(b)
        for f in self.fires[:]:
            f[2] -= 1
            if f[2] <= 0:
                self.fires.remove(f)
        if self.invencivel == 0:
            for fx, fy, _ in self.fires:
                if fx == self.pl[0] and fy == self.pl[1]:
                    self.perder_vida()
                    break
        for en in self.ens:
            en[5] -= 1
            if en[5] > 0:
                continue
            en[5] = 9 if en[2] == 0 else 6 if en[2] == 1 else 3
            px, py = self.pl
            x, y, tipo, dx, dy, _ = en
            if tipo == 2 and random.random() < 0.7:
                if abs(px - x) > abs(py - y):
                    dx = 1 if px > x else -1
                    dy = 0
                else:
                    dx = 0
                    dy = 1 if py > y else -1
            nx = x + dx
            ny = y + dy
            pode = 0 <= nx < self.cols and 0 <= ny < self.rows and self.grid[ny][nx] == 0 and not any(b[0] == nx and b[1] == ny for b in self.bombs)
            if pode:
                en[0], en[1] = nx, ny
            else:
                dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
                random.shuffle(dirs)
                for ndx, ndy in dirs:
                    nnx = x + ndx
                    nny = y + ndy
                    if 0 <= nnx < self.cols and 0 <= nny < self.rows and self.grid[nny][nnx] == 0:
                        en[3], en[4] = ndx, ndy
                        break
            if en[0] == self.pl[0] and en[1] == self.pl[1] and self.invencivel == 0:
                self.perder_vida()
        if len(self.ens) == 0:
            if self.fase < 6:
                self.fase += 1
            else:
                self.fase = 1
            self.setup()
        self.dr()
    def dr(self, *a):
        self.canvas.clear()
        if self.width < 10:
            return
        cw = self.width / self.cols
        ch = self.height / self.rows
        with self.canvas:
            for y in range(self.rows):
                for x in range(self.cols):
                    if self.fase == 1:
                        if (x + y) % 2 == 0:
                            Color(0.24, 0.76, 0.20, 1)
                        else:
                            Color(0.29, 0.88, 0.23, 1)
                    elif self.fase == 2:
                        if (x + y) % 2 == 0:
                            Color(0.85, 0.76, 0.84, 1)
                        else:
                            Color(0.78, 0.66, 0.77, 1)
                    elif self.fase == 3:
                        if (x + y) % 2 == 0:
                            Color(0.18, 0.77, 0.69, 1)
                        else:
                            Color(0.23, 0.84, 0.76, 1)
                    elif self.fase == 4:
                        if (x + y) % 2 == 0:
                            Color(0.24, 0.76, 0.2, 1)
                        else:
                            Color(0.42, 0.91, 0.35, 1)
                    elif self.fase == 5:
                        if (x + y) % 2 == 0:
                            Color(0.10, 0.54, 0.91, 1)
                        else:
                            Color(0.16, 0.60, 1, 1)
                    else:
                        if (x + y) % 2 == 0:
                            Color(0.23, 0.77, 0.63, 1)
                        else:
                            Color(0.29, 0.85, 0.69, 1)
                    Rectangle(pos=(self.x + x * cw, self.y + (self.rows - 1 - y) * ch), size=(cw, ch))
                    t = self.grid[y][x]
                    if t == 1:
                        if self.fase == 1:
                            Color(0.63, 0.63, 0.63, 1)
                        elif self.fase == 2:
                            Color(0.42, 0.18, 0.35, 1)
                        elif self.fase == 3:
                            Color(0.29, 0.29, 0.42, 1)
                        elif self.fase == 5:
                            Color(0.47, 0.47, 0.54, 1)
                        else:
                            Color(0.63, 0.85, 0.75, 1)
                        Rectangle(pos=(self.x + x * cw, self.y + (self.rows - 1 - y) * ch), size=(cw - 1, ch - 1))
                    elif t == 2:
                        if self.fase == 1:
                            Color(0.78, 0.78, 0.78, 1)
                        elif self.fase == 2:
                            Color(0.91, 0.88, 0.85, 1)
                        elif self.fase == 3:
                            Color(0.91, 0.76, 0.29, 1)
                        elif self.fase == 4:
                            Color(0.78, 0.60, 0.35, 1)
                        elif self.fase == 5:
                            Color(0.31, 0.31, 0.38, 1)
                        else:
                            Color(0.94, 0.85, 0.69, 1)
                        Rectangle(pos=(self.x + x * cw + 3, self.y + (self.rows - 1 - y) * ch + 3), size=(cw - 6, ch - 6))
            for mx, my, tipo in self.coins:
                if tipo == 0:
                    Color(1, 0.8, 0, 1)
                else:
                    Color(0.82, 0.71, 0.55, 1)
                Ellipse(pos=(self.x + mx * cw + 5, self.y + (self.rows - 1 - my) * ch + 5), size=(cw - 10, ch - 10))
            for fx, fy, _ in self.fires:
                Color(1, 0.4, 0, 1)
                Rectangle(pos=(self.x + fx * cw + 1, self.y + (self.rows - 1 - fy) * ch + 1), size=(cw - 2, ch - 2))
            for bx, by, _ in self.bombs:
                Color(0.42, 0.23, 0.82, 1)
                Ellipse(pos=(self.x + bx * cw + 4, self.y + (self.rows - 1 - by) * ch + 4), size=(cw - 8, ch - 8))
            for ex, ey, tipo, _, _, _ in self.ens:
                if tipo == 0:
                    Color(1, 0.48, 0.75, 1)
                elif tipo == 1:
                    Color(0.3, 0.65, 1, 1)
                else:
                    Color(1, 0.23, 0.23, 1)
                Ellipse(pos=(self.x + ex * cw + 4, self.y + (self.rows - 1 - ey) * ch + 4), size=(cw - 8, ch - 8))
            if not (self.invencivel > 0 and self.invencivel % 4 < 2):
                Color(0.16, 0.49, 1, 1)
                Rectangle(pos=(self.x + self.pl[0] * cw + 4, self.y + (self.rows - 1 - self.pl[1]) * ch + 4), size=(cw - 8, ch - 8))

class BScreen(BaseScreen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.main = BoxLayout(orientation='vertical')
        self.main.add_widget(self.top_bar())
        self.lb = Label(text='VIDAS: 3 FASE: 1 PONTOS: 0', size_hint_y=0.07, bold=True, font_size=12)
        self.main.add_widget(self.lb)
        self.add_widget(self.main)
        self.board = None
    def on_enter(self):
        super().on_enter()
        if not self.board:
            self.board = BBoard()
            self.main.add_widget(self.board, index=1)
            ctrl = self.ctrls(lambda: self.board.move(-1, 0), lambda: self.board.move(1, 0), lambda: self.board.move(0, -1), lambda: self.board.move(0, 1), extra=lambda: self.board.bomb(), et='BOMBA')
            self.main.add_widget(ctrl, index=0)
            self.main.add_widget(Label(text='Corange Sistemas - PIX ' + PIX, size_hint_y=0.05, color=(0, 1, 0.4, 1), font_size=11), index=0)
            Clock.schedule_interval(self.upd, 0.1)
    def upd(self, dt):
        self.lb.text = 'VIDAS: %s FASE: %s PONTOS: %s REC: %s' % (self.board.vidas, self.board.fase, self.board.pontos, self.board.recorde)

class GameApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(TScreen(name='tetris'))
        sm.add_widget(CScreen(name='cobra'))
        sm.add_widget(BScreen(name='bomber'))
        sm.current = 'menu'
        return sm

GameApp().run()
