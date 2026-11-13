from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Ellipse, Line
import random, os

class Celula(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tipo = 0
    def desenha(self, tipo):
        self.tipo = tipo
        self.canvas.clear()
        with self.canvas:
            # CHAO VERDE
            if tipo == 0:
                Color(0.15,0.55,0.15,1)
                Rectangle(pos=self.pos, size=self.size)
            # PAREDE CINZA - #
            elif tipo == 1:
                Color(0.35,0.35,0.35,1)
                Rectangle(pos=self.pos, size=self.size)
                Color(0.5,0.5,0.5,1)
                Line(rectangle=(self.x+2,self.y+2,self.width-4,self.height-4), width=1)
            # TIJOLO MARROM - X
            elif tipo == 2:
                Color(0.6,0.35,0.1,1)
                Rectangle(pos=self.pos, size=self.size)
                Color(0.8,0.5,0.2,1)
                Rectangle(pos=(self.x+2, self.y+self.height/2-1), size=(self.width-4,2))
            # BOMBERMAN AZUL - P
            elif tipo == 10:
                Color(0.15,0.55,0.15,1)
                Rectangle(pos=self.pos, size=self.size)
                Color(0.2,0.5,1,1)
                Ellipse(pos=(self.x+2, self.y+2), size=(self.width-4, self.height-4))
                Color(1,1,1,1)
                Ellipse(pos=(self.x+6, self.y+self.height/2), size=(4,4))
                Ellipse(pos=(self.x+self.width-12, self.y+self.height/2), size=(4,4))
            # BOMBA PRETA COM PAVIO - B
            elif tipo == 11:
                Color(0.15,0.55,0.15,1)
                Rectangle(pos=self.pos, size=self.size)
                Color(0,0,0,1)
                Ellipse(pos=(self.x+4, self.y+2), size=(self.width-8, self.height-10))
                Color(1,0.8,0,1)
                Rectangle(pos=(self.x+self.width/2-1, self.y+self.height-6), size=(2,6))
            # FOGO VERMELHO - *
            elif tipo == 12:
                Color(1,0.2,0,1)
                Rectangle(pos=self.pos, size=self.size)
                Color(1,0.8,0,1)
                Ellipse(pos=(self.x+6, self.y+6), size=(self.width-12, self.height-12))
            # INIMIGO VERMELHO - E
            elif tipo == 13:
                Color(0.15,0.55,0.15,1)
                Rectangle(pos=self.pos, size=self.size)
                Color(1,0.15,0.15,1)
                Ellipse(pos=(self.x+2, self.y+2), size=(self.width-4, self.height-4))
                Color(0,0,0,1)
                Ellipse(pos=(self.x+7, self.y+10), size=(3,3))
                Ellipse(pos=(self.x+self.width-12, self.y+10), size=(3,3))
            # VIDA VERDE - H
            elif tipo == 14:
                Color(0.15,0.55,0.15,1)
                Rectangle(pos=self.pos, size=self.size)
                Color(0.2,1,0.3,1)
                Ellipse(pos=(self.x+4, self.y+4), size=(self.width-8, self.height-8))
                Color(1,1,1,1)
                Rectangle(pos=(self.x+self.width/2-2, self.y+6), size=(4, self.height-12))
                Rectangle(pos=(self.x+6, self.y+self.height/2-2), size=(self.width-12,4))
            # MOEDA AMARELA - $
            elif tipo == 15:
                Color(0.15,0.55,0.15,1)
                Rectangle(pos=self.pos, size=self.size)
                Color(1,0.8,0,1)
                Ellipse(pos=(self.x+5, self.y+5), size=(self.width-10, self.height-10))

class MenuApresentacao(BoxLayout):
    def __init__(self, app_ref, **kwargs):
        super().__init__(orientation='vertical', padding=12, spacing=8, **kwargs)
        self.app = app_ref
        self.musica = None
        Clock.schedule_once(self.tocar_musica, 1.0)
        self.add_widget(Label(text="Bomberman Corange", font_size='32sp', color=(1,0.8,0,1), bold=True, size_hint_y=0.18))
        self.add_widget(Label(text="Corange Sistemas", font_size='16sp', bold=True, size_hint_y=0.06))
        # AQUI O DESENHO NA ABERTURA - 3 INIMIGOS DESENHADOS
        self.add_widget(Label(text="P = VOCE  B = BOMBA  H = VIDA  E E E = 3 INIMIGOS  X = TIJOLO", font_size='11sp', bold=True, size_hint_y=0.08))
        self.add_widget(Label(text=f"RECORDE: {app_ref.recorde}", font_size='18sp', color=(1,0.8,0,1), bold=True, size_hint_y=0.07))
        b = Button(text="INICIAR JOGO", font_size='26sp', background_color=(1,0.8,0,1), bold=True, size_hint_y=0.20)
        b.bind(on_press=self.iniciar)
        self.add_widget(b)
        self.add_widget(Label(text="PIX 51993359782", font_size='16sp', color=(0.3,1,0.4,1), bold=True, size_hint_y=0.06))
    def tocar_musica(self, dt):
        try:
            from kivy.core.audio import SoundLoader
            if os.path.exists('nes.mp3'):
                self.musica = SoundLoader.load('nes.mp3')
                if self.musica:
                    self.musica.loop = True
                    self.musica.play()
        except:
            pass
    def iniciar(self, *a):
        try:
            if self.musica: self.musica.stop()
        except:
            pass
        self.app.iniciar_jogo()

class JogoBomberman(BoxLayout):
    def __init__(self, app_ref, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.app = app_ref
        self.GW, self.GH = 13, 11
        self.fase = 1
        self.fase_max = 6
        self.vidas = 3
        self.pontos = 0
        self.invencivel = 0
        self.game_over = False
        self.recorde = app_ref.recorde
        self.hud = Label(text="VIDAS: 3 | FASE: 1 | RECORDE: 0 | PONTOS: 0", font_size='13sp', size_hint_y=0.08, bold=True)
        self.add_widget(self.hud)
        self.tabuleiro = GridLayout(cols=self.GW, rows=self.GH, size_hint_y=0.65, spacing=1)
        self.blocos = {}
        for r in range(self.GH):
            for c in range(self.GW):
                cel = Celula()
                self.tabuleiro.add_widget(cel)
                self.blocos[(r, c)] = cel
        self.add_widget(self.tabuleiro)
        ctrls = BoxLayout(orientation='horizontal', size_hint_y=0.25, padding=6, spacing=6)
        btn_l = Button(text="<", font_size='36sp', bold=True, background_color=(0.25,0.25,0.25,1), on_press=lambda x:self.mover(-1,0))
        btn_r = Button(text=">", font_size='36sp', bold=True, background_color=(0.25,0.25,0.25,1), on_press=lambda x:self.mover(1,0))
        v_box = BoxLayout(orientation='vertical', spacing=6)
        btn_u = Button(text="^", font_size='36sp', bold=True, background_color=(0.25,0.25,0.25,1), on_press=lambda x:self.mover(0,-1))
        btn_d = Button(text="v", font_size='36sp', bold=True, background_color=(0.25,0.25,0.25,1), on_press=lambda x:self.mover(0,1))
        v_box.add_widget(btn_u); v_box.add_widget(btn_d)
        btn_bomba = Button(text="BOMBA", font_size='14sp', bold=True, background_color=(1,0.6,0,1), on_press=lambda x:self.colocar_bomba())
        ctrls.add_widget(btn_l); ctrls.add_widget(v_box); ctrls.add_widget(btn_r); ctrls.add_widget(btn_bomba)
        self.add_widget(ctrls)
        btn_menu = Button(text="MENU", font_size='12sp', bold=True, background_color=(0.6,0.2,0.2,1), size_hint_y=0.06, on_press=lambda x:self.parar_e_voltar())
        self.add_widget(btn_menu)
        self.reset(manter_pontos=False)
        self.evento = Clock.schedule_interval(self.atualizar, 0.18)

    def parar_e_voltar(self):
        try:
            self.evento.cancel()
        except:
            pass
        self.app.voltar_menu()
    def atualizar_hud(self):
        self.hud.text = f"VIDAS: {self.vidas} | FASE: {self.fase} | RECORDE: {self.recorde} | PONTOS: {self.pontos}"
        if self.pontos > self.recorde:
            self.recorde = self.pontos
            self.app.recorde = self.pontos
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
            if self.invencivel==0: self.perder_vida()
            return
        if any(e[0]==nx and e[1]==ny for e in self.inimigos): return
        self.player = [nx,ny]
        for m in self.moedas[:]:
            if m[0]==nx and m[1]==ny:
                if m[2]==1:
                    if self.vidas<3: self.vidas+=1
                    else: self.pontos+=200
                else: self.pontos+=100
                self.moedas.remove(m)
                self.atualizar_hud()
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
        pegou=False
        for fx,fy in pos:
            self.fogos.append([fx,fy,3])
            if fx==self.player[0] and fy==self.player[1] and self.invencivel==0: pegou=True
            for en in self.inimigos[:]:
                if en[0]==fx and en[1]==fy: self.inimigos.remove(en); self.pontos+=50; self.atualizar_hud()
        if pegou: self.perder_vida()
    def atualizar(self,dt):
        if self.game_over: self.desenhar(); return
        if self.invencivel>0: self.invencivel-=1
        for b in self.bombas[:]:
            b[2]-=1
            if b[2]<=0: self.explodir(b); self.bombas.remove(b)
        for f in self.fogos[:]:
            f[2]-=1
            if f[2]<=0: self.fogos.remove(f)
        for en in self.inimigos[:]:
            if any(f[0]==en[0] and f[1]==en[1] for f in self.fogos):
                self.inimigos.remove(en); self.pontos+=50; self.atualizar_hud()
        if any(f[0]==self.player[0] and f[1]==self.player[1] for f in self.fogos) and self.invencivel==0:
            self.perder_vida(); self.desenhar(); return
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
    def desenhar(self):
        for r in range(self.GH):
            for c in range(self.GW):
                cel=self.blocos[(r,c)]; t=self.grid[r][c]
                if t==1: cel.desenha(1)
                elif t==2: cel.desenha(2)
                else: cel.desenha(0)
        for mx,my,tipo in self.moedas:
            self.blocos[(my,mx)].desenha(14 if tipo==1 else 15)
        for fx,fy,_ in self.fogos:
            self.blocos[(fy,fx)].desenha(12)
        for bx,by,t in self.bombas:
            self.blocos[(by,bx)].desenha(11)
        for en in self.inimigos:
            self.blocos[(en[1],en[0])].desenha(13)
        px,py=self.player
        if not (self.invencivel>0 and self.invencivel%2==0):
            self.blocos[(py,px)].desenha(10)
        if self.game_over:
            self.hud.text="GAME OVER! Volte ao menu"
        elif len(self.inimigos)==0:
            if self.fase==self.fase_max:
                self.hud.text="ZEROU! Aperte BOMBA"
            else:
                self.hud.text=f"FASE {self.fase} OK! Aperte BOMBA"

class MainApp(App):
    recorde = 0
    def build(self):
        self.title="Bomberman Corange"
        self.root=BoxLayout()
        self.voltar_menu()
        return self.root
    def voltar_menu(self):
        for child in self.root.children[:]:
            if hasattr(child, 'evento'):
                try:
                    child.evento.cancel()
                except:
                    pass
        self.root.clear_widgets()
        self.root.add_widget(MenuApresentacao(self))
    def iniciar_jogo(self):
        self.voltar_menu()
        self.root.clear_widgets()
        self.root.add_widget(JogoBomberman(self))

if __name__=='__main__':
    MainApp().run()
