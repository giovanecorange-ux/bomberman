from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Rectangle, Line, Triangle
from kivy.clock import Clock
import random, traceback, os, json

# ---------- DESENHO ----------
class Bloco(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tipo = 'chao'
        self.chao = (0.24,0.76,0.19,1)
        self.fixo = (0.62,0.62,0.62,1)
        self.dest = (0.6,0.6,0.6,1)
        self.bind(pos=self._redesenhar, size=self._redesenhar)
    def _redesenhar(self, *a):
        self.desenhar(self.tipo, self.chao, self.fixo, self.dest)
    def desenhar(self, tipo, chao=(0.24,0.76,0.19,1), fixo=(0.62,0.62,0.62,1), dest=(0.6,0.6,0.6,1)):
        self.tipo = tipo
        self.chao = chao
        self.fixo = fixo
        self.dest = dest
        self.canvas.clear()
        x, y = self.pos
        w, h = self.size
        if w <= 1 or h <= 1:
            return
        with self.canvas:
            if tipo == 'player':
                Color(*chao)
                Rectangle(pos=(x,y), size=(w,h))
                Color(1, 1, 0.4, 1)
                Ellipse(pos=(x+w*0.15, y+h*0.15), size=(w*0.7, h*0.7))
                Color(0,0,0,1)
                Ellipse(pos=(x+w*0.30, y+h*0.55), size=(w*0.12, h*0.12))
                Ellipse(pos=(x+w*0.58, y+h*0.55), size=(w*0.12, h*0.12))
                Color(0,0,0,1)
                Line(points=[x+w*0.35, y+h*0.35, x+w*0.65, y+h*0.35], width=1)
            elif tipo == 'bomba':
                Color(*chao)
                Rectangle(pos=(x,y), size=(w,h))
                Color(0,0,0,1)
                Ellipse(pos=(x+w*0.2, y+h*0.08), size=(w*0.6, h*0.6))
                Color(1,1,1,1)
                Ellipse(pos=(x+w*0.30, y+h*0.45), size=(w*0.12, h*0.12))
                Color(1, 0.8, 0, 1)
                Line(points=[x+w*0.5, y+h*0.68, x+w*0.75, y+h*0.92], width=2)
                Color(1, 0.3, 0, 1)
                Ellipse(pos=(x+w*0.68, y+h*0.85), size=(w*0.15, h*0.15))
            elif tipo == 'inimigo0':
                Color(*chao)
                Rectangle(pos=(x,y), size=(w,h))
                Color(1, 0.48, 0.75, 1)
                Rectangle(pos=(x+w*0.1, y+h*0.1), size=(w*0.8, h*0.8))
                Color(0,0,0,1)
                Ellipse(pos=(x+w*0.28, y+h*0.50), size=(w*0.15, h*0.15))
                Ellipse(pos=(x+w*0.57, y+h*0.50), size=(w*0.15, h*0.15))
                Line(points=[x+w*0.30, y+h*0.30, x+w*0.70, y+h*0.30], width=1)
            elif tipo == 'inimigo1':
                Color(*chao)
                Rectangle(pos=(x,y), size=(w,h))
                Color(0.30, 0.65, 1, 1)
                Rectangle(pos=(x+w*0.1, y+h*0.1), size=(w*0.8, h*0.8))
                Color(0,0,0,1)
                Ellipse(pos=(x+w*0.28, y+h*0.50), size=(w*0.15, h*0.15))
                Ellipse(pos=(x+w*0.57, y+h*0.50), size=(w*0.15, h*0.15))
                Line(points=[x+w*0.30, y+h*0.30, x+w*0.70, y+h*0.30], width=1)
            elif tipo == 'inimigo2':
                Color(*chao)
                Rectangle(pos=(x,y), size=(w,h))
                Color(1, 0.23, 0.23, 1)
                Rectangle(pos=(x+w*0.1, y+h*0.1), size=(w*0.8, h*0.8))
                Color(0,0,0,1)
                Ellipse(pos=(x+w*0.28, y+h*0.50), size=(w*0.15, h*0.15))
                Ellipse(pos=(x+w*0.57, y+h*0.50), size=(w*0.15, h*0.15))
                Line(points=[x+w*0.30, y+h*0.30, x+w*0.70, y+h*0.30], width=1)
            elif tipo == 'fogo':
                Color(1, 0.4, 0, 1)
                Rectangle(pos=(x,y), size=(w,h))
                Color(1, 1, 0, 1)
                Triangle(points=[x+w*0.5, y+h*0.92, x+w*0.15, y+h*0.08, x+w*0.85, y+h*0.08])
                Color(1, 0.4, 0, 1)
                Triangle(points=[x+w*0.5, y+h*0.65, x+w*0.30, y+h*0.08, x+w*0.70, y+h*0.08])
            elif tipo == 'moeda':
                Color(*chao)
                Rectangle(pos=(x,y), size=(w,h))
                Color(1, 0.8, 0, 1)
                Ellipse(pos=(x+w*0.25, y+h*0.20), size=(w*0.5, h*0.6))
                Color(0.7, 0.52, 0, 1)
                Line(points=[x+w*0.5, y+h*0.25, x+w*0.5, y+h*0.75], width=1)
            elif tipo == 'moeda_vida':
                Color(*chao)
                Rectangle(pos=(x,y), size=(w,h))
                Color(0.82, 0.70, 0.54, 1)
                Ellipse(pos=(x+w*0.25, y+h*0.20), size=(w*0.5, h*0.6))
                Color(0, 0.4, 0, 1)
                Line(points=[x+w*0.5, y+h*0.25, x+w*0.5, y+h*0.75], width=1)
            elif tipo == 'fixo':
                Color(*fixo)
                Rectangle(pos=(x,y), size=(w,h))
                Color(0,0,0,1)
                Line(points=[x, y+h*0.5, x+w, y+h*0.5], width=1)
                Line(points=[x+w*0.5, y, x+w*0.5, y+h*0.5], width=1)
                Line(points=[x+w*0.25, y+h*0.5, x+w*0.25, y+h], width=1)
                Line(points=[x+w*0.75, y+h*0.5, x+w*0.75, y+h], width=1)
            elif tipo == 'dest':
                Color(*dest)
                Rectangle(pos=(x,y), size=(w,h))
                Color(0,0,0,1)
                Line(points=[x, y+h*0.5, x+w, y+h*0.5], width=1)
                Line(points=[x+w*0.5, y, x+w*0.5, y+h], width=1)
                Line(points=[x+w*0.25, y+h*0.5, x+w*0.25, y+h], width=1)
            else: # chao
                Color(*chao)
                Rectangle(pos=(x,y), size=(w,h))
                Color(0.15, 0.55, 0.15, 1)
                Ellipse(pos=(x+w*0.20, y+h*0.20), size=(w*0.15, h*0.15))
                Ellipse(pos=(x+w*0.65, y+h*0.60), size=(w*0.15, h*0.15))

class DesenhoMenu(Widget):
    def __init__(self, tipo='player', cor=(0.16,0.49,1,1), **kwargs):
        super().__init__(**kwargs)
        self.tipo = tipo
        self.cor = cor
        self.bind(pos=self._des, size=self._des)
    def _des(self, *a):
        self.canvas.clear()
        x, y = self.pos
        w, h = self.size
        if w <= 1 or h <= 1:
            return
        with self.canvas:
            Color(*self.cor)
            Rectangle(pos=(x,y), size=(w,h))
            if self.tipo == 'player':
                Color(1, 1, 0.4, 1)
                Ellipse(pos=(x+w*0.15, y+h*0.15), size=(w*0.7, h*0.7))
                Color(0,0,0,1)
                Ellipse(pos=(x+w*0.30, y+h*0.55), size=(w*0.12, h*0.12))
                Ellipse(pos=(x+w*0.58, y+h*0.55), size=(w*0.12, h*0.12))
                Line(points=[x+w*0.35, y+h*0.35, x+w*0.65, y+h*0.35], width=1)
            elif self.tipo == 'bomba':
                Color(0,0,0,1)
                Ellipse(pos=(x+w*0.2, y+h*0.08), size=(w*0.6, h*0.6))
                Color(1, 0.8, 0, 1)
                Line(points=[x+w*0.5, y+h*0.68, x+w*0.75, y+h*0.92], width=2)
            else: # inimigo
                Color(1,1,1,1)
                Rectangle(pos=(x+w*0.1, y+h*0.1), size=(w*0.8, h*0.8))
                Color(0,0,0,1)
                Ellipse(pos=(x+w*0.28, y+h*0.50), size=(w*0.15, h*0.15))
                Ellipse(pos=(x+w*0.57, y+h*0.50), size=(w*0.15, h*0.15))
                Line(points=[x+w*0.30, y+h*0.30, x+w*0.70, y+h*0.30], width=1)

class MenuApresentacao(BoxLayout):
    def __init__(self, app_ref, **kwargs):
        super().__init__(orientation='vertical', padding=12, spacing=8, **kwargs)
        self.app = app_ref
        self.add_widget(Label(text="Bomberman Corange", font_size='32sp', color=(1,0.8,0,1), bold=True, size_hint_y=0.18))
        self.add_widget(Label(text="Corange Sistemas", font_size='16sp', bold=True, size_hint_y=0.06))
        self.add_widget(Label(text="PIX 51993359782", font_size='15sp', color=(0.3,1,0.4,1), bold=True, size_hint_y=0.08))
        desenhos = BoxLayout(orientation='horizontal', size_hint_y=0.28, spacing=8, padding=[20,0,20,0])
        desenhos.add_widget(DesenhoMenu(tipo='player', cor=(0.16,0.49,1,1)))
        desenhos.add_widget(DesenhoMenu(tipo='bomba', cor=(0.41,0.22,0.81,1)))
        desenhos.add_widget(DesenhoMenu(tipo='inimigo', cor=(1,0.48,0.75,1)))
        desenhos.add_widget(DesenhoMenu(tipo='inimigo', cor=(0.30,0.65,1,1)))
        desenhos.add_widget(DesenhoMenu(tipo='inimigo', cor=(1,0.23,0.23,1)))
        self.add_widget(desenhos)
        self.add_widget(Label(text=f"RECORDE: {app_ref.recorde}", font_size='20sp', color=(1,0.8,0,1), bold=True, size_hint_y=0.09))
        self.add_widget(Label(text="Seu maior score fica salvo aqui!", font_size='12sp', color=(0.8,0.8,0.8,1), size_hint_y=0.05))
        b = Button(text="INICIAR JOGO", font_size='26sp', background_color=(1,0.8,0,1), background_normal='', bold=True, size_hint_y=0.20, color=(0,0,0,1))
        b.bind(on_press=self.iniciar)
        self.add_widget(b)
    def iniciar(self, *a):
        self.app.iniciar_jogo()

class JogoBomberman(BoxLayout):
    def __init__(self, app_ref, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.app = app_ref
        self.GW, self.GH = 13, 11
        self.fase = 1; self.fase_max = 6
        self.vidas = 3; self.pontos = 0
        self.invencivel = 0; self.game_over = False
        self.recorde = app_ref.recorde
        self.hud = Label(text=f"VIDAS: 3 | FASE: 1 | RECORDE: {self.recorde} | PONTOS: 0", font_size='13sp', size_hint_y=0.08, bold=True)
        self.add_widget(self.hud)
        self.tabuleiro = GridLayout(cols=self.GW, size_hint_y=0.65, spacing=1)
        self.blocos = {}
        for r in range(self.GH):
            for c in range(self.GW):
                btn = Bloco()
                self.tabuleiro.add_widget(btn)
                self.blocos[(r, c)] = btn
        self.add_widget(self.tabuleiro)
        ctrls = BoxLayout(orientation='horizontal', size_hint_y=0.25, padding=6, spacing=6)
        btn_l = Button(text="<", font_size='36sp', bold=True, background_color=(0.25,0.25,0.25,1), background_normal='', on_press=lambda x:self.mover(-1,0))
        btn_r = Button(text=">", font_size='36sp', bold=True, background_color=(0.25,0.25,0.25,1), background_normal='', on_press=lambda x:self.mover(1,0))
        v_box = BoxLayout(orientation='vertical', spacing=6)
        btn_u = Button(text="^", font_size='36sp', bold=True, background_color=(0.25,0.25,0.25,1), background_normal='', on_press=lambda x:self.mover(0,-1))
        btn_d = Button(text="v", font_size='36sp', bold=True, background_color=(0.25,0.25,0.25,1), background_normal='', on_press=lambda x:self.mover(0,1))
        v_box.add_widget(btn_u); v_box.add_widget(btn_d)
        btn_bomba = Button(text="BOMBA", font_size='14sp', bold=True, background_color=(1,0.6,0,1), background_normal='', on_press=lambda x:self.colocar_bomba())
        btn_r2 = Button(text="R", font_size='20sp', bold=True, background_color=(0.6,0.2,0.2,1), background_normal='', on_press=lambda x:self.reiniciar())
        ctrls.add_widget(btn_l); ctrls.add_widget(v_box); ctrls.add_widget(btn_r); ctrls.add_widget(btn_bomba); ctrls.add_widget(btn_r2)
        self.add_widget(ctrls)
        btn_menu = Button(text="MENU", font_size='12sp', bold=True, background_color=(0.6,0.2,0.2,1), background_normal='', size_hint_y=0.06, on_press=lambda x:self.parar_e_voltar())
        self.add_widget(btn_menu)
        self.reset(manter_pontos=False)
        self.evento = Clock.schedule_interval(self.atualizar, 0.18)
    def reiniciar(self):
        if self.game_over: self.fase=1; self.reset(manter_pontos=False)
        elif len(self.inimigos)==0: self.avancar_fase()
    def parar_e_voltar(self):
        try: self.evento.cancel()
        except: pass
        self.app.voltar_menu()
    def atualizar_hud(self):
        if self.pontos > self.recorde:
            self.recorde = self.pontos
            self.app.recorde = self.pontos
            self.app.save_recorde()
        self.hud.text = f"VIDAS: {self.vidas} | FASE: {self.fase} | RECORDE: {self.recorde} | PONTOS: {self.pontos}"
    def reset(self, manter_pontos=False):
        self.grid = []; self.player = [1,1]; self.bombas = []; self.fogos = []; self.moedas = []; self.game_over = False
        if not manter_pontos: self.vidas = 3; self.pontos = 0
        self.invencivel = 0; self.atualizar_hud()
        for y in range(self.GH):
            linha = []
            for x in range(self.GW):
                if x==0 or y==0 or x==self.GW-1 or y==self.GH-1 or (x%2==0 and y%2==0): linha.append(1)
                elif (x<3 and y<3) or (x>self.GW-4 and y<3) or (x<3 and y>self.GH-4) or (x>self.GW-4 and y>self.GH-4): linha.append(0)
                elif random.random()<0.30: linha.append(2)
                else: linha.append(0)
            self.grid.append(linha)
        qtd = 3 + (self.fase-1)
        posicoes = [[self.GW-2,1],[self.GW-2,self.GH-2],[1,self.GH-2],[self.GW-2,self.GH//2],[1,self.GH//2],[self.GW//2,self.GH-2],[self.GW-2,3],[1,3]]
        self.inimigos = []
        for i in range(min(qtd,len(posicoes))): self.inimigos.append([posicoes[i][0],posicoes[i][1],i%3])
    def mover(self,dx,dy):
        if self.game_over: return
        if len(self.inimigos)==0: self.avancar_fase(); return
        x,y = self.player; nx,ny = x+dx, y+dy
        if not (0<=nx<self.GW and 0<=ny<self.GH): return
        if self.grid[ny][nx]!=0: return
        if any(b[0]==nx and b[1]==ny for b in self.bombas): return
        if any(f[0]==nx and f[1]==ny for f in self.fogos):
            self.perder_vida(); return
        if any(e[0]==nx and e[1]==ny for e in self.inimigos): return
        self.player = [nx,ny]
        for m in self.moedas[:]:
            if m[0]==nx and m[1]==ny:
                if m[2]==1:
                    if self.vidas<3: self.vidas+=1
                    else: self.pontos+=200
                else: self.pontos+=100
                self.moedas.remove(m); self.atualizar_hud()
    def colocar_bomba(self):
        if self.game_over: return
        if len(self.inimigos)==0: self.avancar_fase(); return
        x,y = self.player
        if len(self.bombas)<2 and not any(b[0]==x and b[1]==y for b in self.bombas):
            self.bombas.append([x,y,6])
    def avancar_fase(self):
        if self.fase<self.fase_max: self.fase+=1; self.reset(manter_pontos=True)
        else: self.fase=1; self.reset(manter_pontos=True)
    def perder_vida(self):
        self.vidas-=1; self.atualizar_hud()
        if self.vidas<=0: self.game_over=True; self.bombas.clear(); self.fogos.clear()
        else: self.player=[1,1]; self.invencivel=5; self.bombas.clear(); self.fogos.clear()
    def explodir(self,b):
        x,y,_=b
        pos=[[x,y]]
        for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            for i in range(1,3):
                nx,ny=x+dx*i,y+dy*i
                if not (0<=nx<self.GW and 0<=ny<self.GH): break
                if self.grid[ny][nx]==1: break
                pos.append([nx,ny])
                if self.grid[ny][nx]==2:
                    self.grid[ny][nx]=0
                    if random.random()<0.40:
                        tipo=1 if random.random()<0.30 else 0
                        if not any(mm[0]==nx and mm[1]==ny for mm in self.moedas): self.moedas.append([nx,ny,tipo])
                    break
        for fx,fy in pos:
            self.fogos.append([fx,fy,3])
            if fx==self.player[0] and fy==self.player[1]:
                self.perder_vida()
            for en in self.inimigos[:]:
                if en[0]==fx and en[1]==fy: self.inimigos.remove(en); self.pontos+=50; self.atualizar_hud()
    def atualizar(self,dt):
        try:
            if self.game_over: self.desenhar(); return
            if self.invencivel>0: self.invencivel-=1
            for b in self.bombas[:]:
                b[2]-=1
                if b[2]<=0: self.explodir(b); self.bombas.remove(b)
            for f in self.fogos[:]:
                f[2]-=1
                if f[2]<=0: self.fogos.remove(f)
            if any(f[0]==self.player[0] and f[1]==self.player[1] for f in self.fogos):
                self.perder_vida(); self.desenhar(); return
            for en in self.inimigos[:]:
                if any(f[0]==en[0] and f[1]==en[1] for f in self.fogos):
                    self.inimigos.remove(en); self.pontos+=50; self.atualizar_hud()
            if not self.inimigos: self.desenhar(); return
            for en in self.inimigos[:]:
                if random.random()<0.5:
                    dirs=[(1,0),(-1,0),(0,1),(0,-1)]; random.shuffle(dirs)
                    for dx,dy in dirs:
                        nx,ny=en[0]+dx,en[1]+dy
                        if not (0<=nx<self.GW and 0<=ny<self.GH): continue
                        if self.grid[ny][nx]!=0: continue
                        if any(b[0]==nx and b[1]==ny for b in self.bombas): continue
                        if any(f[0]==nx and f[1]==ny for f in self.fogos): continue
                        if nx==self.player[0] and ny==self.player[1]: continue
                        en[0],en[1]=nx,ny; break
                if en not in self.inimigos: continue
                if en[0]==self.player[0] and en[1]==self.player[1] and self.invencivel==0: self.perder_vida(); break
            self.desenhar()
        except: traceback.print_exc()
    def desenhar(self):
        if self.fase==1: chao=(0.24,0.76,0.19,1); fixo=(0.62,0.62,0.62,1); dest=(0.6,0.6,0.6,1)
        elif self.fase==2: chao=(0.85,0.76,0.83,1); fixo=(0.41,0.17,0.35,1); dest=(0.91,0.87,0.84,1)
        elif self.fase==3: chao=(0.18,0.76,0.69,1); fixo=(0.29,0.29,0.41,1); dest=(0.91,0.76,0.29,1)
        elif self.fase==4: chao=(0.24,0.76,0.19,1); fixo=(0.53,0.60,0.69,1); dest=(0.78,0.60,0.35,1)
        elif self.fase==5: chao=(0.10,0.54,0.91,1); fixo=(0.47,0.47,0.53,1); dest=(0.31,0.31,0.37,1)
        else: chao=(0.22,0.76,0.62,1); fixo=(0.62,0.84,0.75,1); dest=(0.94,0.84,0.69,1)
        for r in range(self.GH):
            for c in range(self.GW):
                btn=self.blocos[(r,c)]; t=self.grid[r][c]
                if t==1: btn.desenhar('fixo', chao, fixo, dest)
                elif t==2: btn.desenhar('dest', chao, fixo, dest)
                else: btn.desenhar('chao', chao, fixo, dest)
        for mx,my,tipo in self.moedas:
            b=self.blocos[(my,mx)]
            if tipo==1: b.desenhar('moeda_vida', chao, fixo, dest)
            else: b.desenhar('moeda', chao, fixo, dest)
        for fx,fy,_ in self.fogos:
            b=self.blocos[(fy,fx)]; b.desenhar('fogo', chao, fixo, dest)
        for bx,by,_ in self.bombas:
            b=self.blocos[(by,bx)]; b.desenhar('bomba', chao, fixo, dest)
        for en in self.inimigos:
            b=self.blocos[(en[1],en[0])]
            if en[2]==0: b.desenhar('inimigo0', chao, fixo, dest)
            elif en[2]==1: b.desenhar('inimigo1', chao, fixo, dest)
            else: b.desenhar('inimigo2', chao, fixo, dest)
        px,py=self.player
        if not (self.invencivel>0 and self.invencivel%2==0):
            b=self.blocos[(py,px)]; b.desenhar('player', chao, fixo, dest)
        if self.game_over: self.hud.text=f"GAME OVER! RECORDE: {self.recorde} | Aperte R"
        elif len(self.inimigos)==0:
            if self.fase==self.fase_max: self.hud.text=f"ZEROU! RECORDE: {self.recorde} | Aperte R"
            else: self.hud.text=f"FASE {self.fase} OK! RECORDE: {self.recorde} | Aperte R"

class MainApp(App):
    recorde = 0
    def get_rec_path(self):
        try:
            return os.path.join(self.user_data_dir, 'recorde.json')
        except:
            return 'recorde.json'
    def load_recorde(self):
        try:
            p = self.get_rec_path()
            if os.path.exists(p):
                with open(p, 'r') as f:
                    data = json.load(f)
                    self.recorde = data.get('recorde', 0)
        except:
            self.recorde = 0
    def save_recorde(self):
        try:
            p = self.get_rec_path()
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, 'w') as f:
                json.dump({'recorde': self.recorde}, f)
        except:
            pass
    def build(self):
        self.load_recorde()
        self.title="Bomberman Corange"
        self.root=BoxLayout()
        self.root.add_widget(Label(text="Carregando..."))
        Clock.schedule_once(self.carregar_menu, 0.3)
        return self.root
    def carregar_menu(self, dt):
        self.root.clear_widgets()
        self.root.add_widget(MenuApresentacao(self))
    def voltar_menu(self):
        for child in self.root.children[:]:
            if hasattr(child, 'evento'):
                try: child.evento.cancel()
                except: pass
        self.root.clear_widgets()
        self.root.add_widget(MenuApresentacao(self))
    def iniciar_jogo(self):
        for child in self.root.children[:]:
            if hasattr(child, 'evento'):
                try: child.evento.cancel()
                except: pass
        self.root.clear_widgets()
        self.root.add_widget(JogoBomberman(self))

if __name__=='__main__':
    MainApp().run()
