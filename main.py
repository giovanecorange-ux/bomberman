from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle, Ellipse, Line, Triangle
from kivy.clock import Clock
from kivy.core.window import Window

Window.size = (360, 640)

def _mapa_de_texto(linhas):
    mapa = []
    for l in linhas:
        l = l.ljust(17, '#')[:17]  # CORRIGIDO: trava pra 17 colunas, nunca mais fecha
        row = []
        for c in l:
            if c == '#': row.append('fixo')
            elif c == '.': row.append('pastilha')
            elif c == 'P': row.append('poder')
            elif c == 'T': row.append('porta')
            else: row.append('chao')
        mapa.append(row)
    return mapa

def _criar_mapas_simples():
    m1 = [
        "#################",
        "#P....##.##...P#",
        "#.##.##...##.##.#",
        "#.....##.##.....#",
        "#.##.##TTT##.##.#",
        "#....##...##....#",
        "##.#.##...##.#.##",
        "#....##...##....#",
        "#.##.##TTT##.##.#",
        "#.##.##...##.##.#",
        "#....##...##....#",
        "#.##.##...##.##.#",
        "#.##.#######.##.#",
        "#....##.T.##....#",
        "#.##.##.###.##.##",
        "#....##.....##..#",
        "#.##.##.###.##.##",
        "#.##........#.##.#",
        "#.##.##TTT##.##.#",
        "#P...##...##..P#",
        "#################",
    ]
    m2 = [
        "#################",
        "#P.............P#",
        "#.##.##.###.##.##",
        "#...............#",
        "#.##.##.###.##.##",
        "#....##...##....#",
        "##.#.##...##.#.##",
        "#....##...##....#",
        "#.##.##TTT##.##.#",
        "#.##.##...##.##.#",
        "#....##...##....#",
        "#.##.##...##.##.#",
        "#.##.#######.##.#",
        "#....##.T.##....#",
        "#.##.##.###.##.##",
        "#....##.....##..#",
        "#.##.##.###.##.##",
        "#.##........#.##.#",
        "#.##.##TTT##.##.#",
        "#P...##...##...P#",
        "#################",
    ]
    m3 = m1[:]
    m4 = [
        "#################",
        "#PL.##.###.##.LP#",
        "#...##.....##...#",
        "#.##.##.T.##.##.#",
        "#.##.#.....#.##.#",
        "#....+.....+....#",
        "##.#.##...##.#.##",
        "#....##...##....#",
        "#.##.##TTT##.##.#",
        "#....##...##....#",
        "#.##.##...##.##.#",
        "#.##.##...##.##.#",
        "#.##..#####..##.#",
        "#....##.T.##....#",
        "#.##.##...##.##.#",
        "#....##...##....#",
        "#.##.#######.##.#",
        "#.##...T...#.##.#",
        "#P..##.T.T.##..P#",
        "#P...##...##...P#",
        "#################",
    ]
    m5 = m1[:]
    m6 = [
        "#################",
        "#P...#.......#..P#",
        "#.##.#.#####.#.##.#",
        "#....#.......#....#",
        "#.##.##.....##.##.#",
        "#....##.....##....#",
        "##.#.##.....##.#.##",
        "#....##.....##....#",
        "#.##.##.....##.##.#",
        "#....##.....##....#",
        "#.##.##.....##.##.#",
        "#....##.....##....#",
        "#.##.##.....##.##.#",
        "#....##.....##....#",
        "#.##.##.....##.##.#",
        "#P...##.....##..P#",
        "#.##.##.....##.##.#",
        "#....##.....##....#",
        "#P..###.....###.P#",
        "#P...##.....##..P#",
        "#################",
    ]
    m7 = m6[:]
    # FASE 8 - CORRIGIDA - 17 em todas as linhas
    m8 = [
        "#################",
        "#PL.##.TTT.##.LP#",
        "#.L.##..T..##.L.#",
        "#.L.##.....##.L.#",
        "#....##...##....#",
        "#.##.##...##.##.#",
        "#.L..##...##..L.#",
        "##.#.#######.#.##",
        "#....##.T.##....#",
        "#.##.##...##.##.#",
        "#.##..#####..##.#",
        "#.L..##.T.##..L.#",
        "#....##...##....#",
        "#.##.##...##.##.#",
        "#.##.##...##.##.#",
        "#P..##.....##..P#",
        "#.##.##...##.##.#",
        "#P..###...###..P#",
        "#P...##...##...P#",
        "#P...#######...P#",
        "#################",
    ]
    m9 = m8[:]
    m10 = m7[:]

    todos = [m1,m2,m3,m4,m5,m6,m7,m8,m9,m10]
    return [_mapa_de_texto(f) for f in todos]

FASES_MAPAS = _criar_mapas_simples()
FASES_SKINS = [
    {"fixo": (1, 0.8, 0.4, 1), "nome": "Fase 1 Stage 1/20"},
    {"fixo": (0.2, 1, 0.2, 1), "nome": "Fase 2 Ghost AI"},
    {"fixo": (1, 0.8, 0.6, 1), "nome": "Fase 3 Ms (3)"},
    {"fixo": (0.2, 0.4, 1, 1), "nome": "Fase 4 Ms (4)"},
    {"fixo": (1, 0.4, 0.6, 1), "nome": "Fase 5 Rosa 1UP"},
    {"fixo": (0.2, 0.6, 1, 1), "nome": "Fase 6 Azul L"},
    {"fixo": (0.2, 0.4, 1, 1), "nome": "Fase 7 Reinforced"},
    {"fixo": (0.2, 0.6, 1, 1), "nome": "Fase 8 Pac Chaves"},
    {"fixo": (0, 1, 1, 1), "nome": "Fase 9"},
    {"fixo": (1, 0.84, 0, 1), "nome": "Boss Final"},
]

class Bloco(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tipo = 'chao'; self.l = 0; self.c = 0
        self.bind(pos=self._redesenhar, size=self._redesenhar)
    def _redesenhar(self, *args): 
        self.desenhar(self.tipo, None, self.skin if hasattr(self,'skin') else None, parede_set=self.parede_set if hasattr(self,'parede_set') else set())
    def desenhar(self, tipo, cor_fase=None, skin=None, inimigo_tipo='vermelho', casa_set=None, porta=None, parede_set=None):
        self.tipo = tipo
        self.skin = skin
        self.parede_set = parede_set or set()
        self.canvas.clear()
        x, y = self.pos; w, h = self.size
        if w <= 1 or h <= 1: return
        fixo = skin["fixo"] if skin else (0.2, 0.6, 1, 1)
        with self.canvas:
            Color(0,0,0,1); Rectangle(pos=(x, y), size=(w, h))
            if tipo == 'fixo':
                Color(*fixo)
                tem_cima = (self.l-1, self.c) in (parede_set or set())
                tem_baixo = (self.l+1, self.c) in (parede_set or set())
                tem_esq = (self.l, self.c-1) in (parede_set or set())
                tem_dir = (self.l, self.c+1) in (parede_set or set())
                if not tem_cima: Line(points=[x, y+h, x+w, y+h], width=1.8)
                if not tem_baixo: Line(points=[x, y, x+w, y], width=1.8)
                if not tem_esq: Line(points=[x, y, x, y+h], width=1.8)
                if not tem_dir: Line(points=[x+w, y, x+w, y+h], width=1.8)
                return
            elif tipo == 'pastilha':
                m = min(w,h); Color(1,1,0.8,1); Ellipse(pos=(x + (w-m*0.22)/2, y + (h-m*0.22)/2), size=(m*0.22, m*0.22)); return
            elif tipo == 'poder':
                m = min(w,h); Color(1,1,0.6,1); Ellipse(pos=(x + (w-m*0.60)/2, y + (h-m*0.60)/2), size=(m*0.60, m*0.60)); return
            elif tipo == 'player':
                Color(1,1,0,1); Ellipse(pos=(x + w*0.10, y + h*0.10), size=(w*0.80, h*0.80))
                Color(0,0,0,1); Triangle(points=[x+w*0.55, y+h*0.5, x+w*0.95, y+h*0.70, x+w*0.95, y+h*0.30]); return
            elif tipo == 'inimigo':
                cores = {'vermelho': (1,0,0,1), 'rosa': (1,0.6,0.8,1), 'ciano': (0,1,1,1), 'laranja': (1,0.6,0,1)}
                c = cores.get(inimigo_tipo, (1,0,0,1))
                Color(*c); Ellipse(pos=(x + w*0.10, y + h*0.20), size=(w*0.80, h*0.60)); Rectangle(pos=(x + w*0.10, y + h*0.05), size=(w*0.80, h*0.30))
                Color(1,1,1,1); Ellipse(pos=(x + w*0.24, y + h*0.50), size=(w*0.20, h*0.24)); Ellipse(pos=(x + w*0.56, y + h*0.50), size=(w*0.20, h*0.24))
                Color(0,0,0,1); Ellipse(pos=(x + w*0.30, y + h*0.54), size=(w*0.09, h*0.14)); Ellipse(pos=(x + w*0.62, y + h*0.54), size=(w*0.09, h*0.14)); return
            elif tipo == 'porta':
                Color(0,0,0,1); Rectangle(pos=(x, y), size=(w, h))
                Color(1,1,1,0.95); Rectangle(pos=(x, y + h*0.38), size=(w, h*0.24)); return
            elif tipo == 'casinha':
                Color(0,0,0,1); Rectangle(pos=(x, y), size=(w, h)); return

class Labirinto(GridLayout):
    def __init__(self, fase=0, **kwargs):
        super().__init__(**kwargs)
        self.cols = 17
        self.fase = fase
        self.mapa = FASES_MAPAS[fase]
        self.skin = FASES_SKINS[fase]
        self.blocos = []
        self.parede_set = set()
        for l in range(len(self.mapa)):
            for c in range(len(self.mapa[0])):
                if self.mapa[l][c] == 'fixo':
                    self.parede_set.add((l,c))
        for l in range(len(self.mapa)):
            row = []
            for c in range(len(self.mapa[0])):
                b = Bloco()
                b.l = l; b.c = c
                b.desenhar(self.mapa[l][c], skin=self.skin, parede_set=self.parede_set)
                self.add_widget(b)
                row.append(b)
            self.blocos.append(row)

class PacmanApp(App):
    def build(self):
        self.fase_atual = 7  # Pac Chaves
        root = Labirinto(fase=self.fase_atual)
        return root

if __name__ == '__main__':
    PacmanApp().run()
