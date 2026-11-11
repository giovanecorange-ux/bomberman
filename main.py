from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Ellipse, Line
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
import random, math, wave, struct, os
Window.clearcolor = (0,0,0,1)
PIX="51993359782"

# ===== SOM - SO ACRESCENTADO, NADA MUDADO =====
def make_beep(freq, ms, name):
    path=f"/tmp/{name}.wav"
    try:
        if os.path.exists(path): return SoundLoader.load(path)
        sr=44100; n=int(sr*ms/1000)
        with wave.open(path,'w') as wf:
            wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(sr)
            for i in range(n):
                s=int(32000*math.sin(2*math.pi*freq*i/sr)*(1-i/n*0.5))
                wf.writeframes(struct.pack('<h',s))
        return SoundLoader.load(path)
    except:
        return None
snd_move = make_beep(400,80,"mv")
snd_rot = make_beep(1200,120,"rt")
snd_down = make_beep(300,50,"dn")
snd_eat = make_beep(900,150,"eat")
snd_over = make_beep(120,500,"over")
snd_bomb = make_beep(300,80,"bomb")
snd_exp = make_beep(80,200,"exp")
snd_coin = make_beep(1000,80,"coin")
def play(s):
    try:
        if s: s.play()
    except: pass
try:
    music = SoundLoader.load('nes.mp3')
    if music: music.loop=True
except:
    music=None

class MenuScreen(Screen):
    def __init__(self,**kw):
        super().__init__(**kw)
        lay=BoxLayout(orientation='vertical',padding=15,spacing=12)
        lay.add_widget(Label(text='Bomberman Corange',font_size=30,bold=True,color=(1,0.8,0,1)))
        lay.add_widget(Label(text='Corange Sistemas',font_size=18,bold=True))
        lay.add_widget(Label(text=f'PIX {PIX}',font_size=16,bold=True,color=(0.3,1,0.22,1)))
        for txt,nome,col in [('TETRIS','tetris',(1,0,0,1)),('COBRINHA','cobra',(0,1,0.4,1)),('BOMBERMAN 6 FASES','bomber',(1,0.8,0,1))]:
            b=Button(text=txt,font_size=22,bold=True,background_color=col,size_hint_y=0.22)
            b.bind(on_press=lambda x,n=nome:setattr(self.manager,'current',n))
            lay.add_widget(b)
        lay.add_widget(Label(text=f'Corange Sistemas - PIX {PIX}',font_size=11,color=(0,1,0.4,1)))
        self.add_widget(lay)
    def on_enter(self):
        if music:
            try: music.play()
            except: pass

class BaseScreen(Screen):
    def top_bar(self):
        b=Button(text='< VOLTAR AO MENU',size_hint_y=0.07,background_color=(0.3,0.3,0.3,1))
        b.bind(on_press=lambda x:setattr(self.manager,'current','menu')); return b
    def ctrls(self, L,R,U,D, extra=None, et='BOMBA'):
        c=BoxLayout(size_hint_y=0.22,spacing=6,padding=6)
        bL=Button(text='<',font_size=32,bold=True); bR=Button(text='>',font_size=32,bold=True)
        bO=Button(text='O',font_size=28,bold=True); bV=Button(text='V',font_size=28,bold=True)
        bL.bind(on_press=lambda x:L()); bR.bind(on_press=lambda x:R()); bO.bind(on_press=lambda x:U()); bV.bind(on_press=lambda x:D())
        c.add_widget(bL); m=BoxLayout(orientation='vertical',spacing=6); m.add_widget(bO); m.add_widget(bV); c.add_widget(m); c.add_widget(bR)
        if extra:
            be=Button(text=et,bold=True,background_color=(0.4,0.2,0.8,1)); be.bind(on_press=lambda x:extra()); c.add_widget(be)
        return c
    def on_enter(self):
        if music:
            try: music.stop()
            except: pass

# ============ TETRIS ORIGINAL ============
C_T=[(1,0,0,1),(0,1,0,1),(0,0.47,1,1),(1,1,0,1),(1,0,1,1),(0,1,1,1),(1,0.55,0,1)]
PE=[[[1,1,1,1]],[[1,1,1],[0,1,0]],[[1,1,0],[0,1,1]],[[0,1,1],[1,1,0]],[[1,1],[1,1]],[[1,1,1],[1,0,0]],[[1,1,1],[0,0,1]]]
class TBoard(Widget):
    def __init__(self,**kw):
        super().__init__(**kw); self.cols=10; self.rows=20; self.grid=[[None]*10 for _ in range(20)]; self.score=0; self.rec=0; self.sp(); Clock.schedule_interval(self.tk,0.45); self.bind(size=self.dr,pos=self.dr)
    def sp(self): i=random.randint(0,6); self.sh=PE[i]; self.co=C_T[i]; self.x=4; self.y=0
    def col(self,dx,dy,sh=None):
        sh=sh or self.sh
        for yy,r in enumerate(sh):
            for xx,v in enumerate(r):
                if v:
                    nx=self.x+xx+dx; ny=self.y+yy+dy
                    if nx<0 or nx>=self.cols or ny>=self.rows: return True
                    if ny>=0 and self.grid[ny][nx]: return True
        return False
    def tk(self,dt):
        if not self.col(0,1): self.y+=1
        else:
            for yy,r in enumerate(self.sh):
                for xx,v in enumerate(r):
                    if v and self.y+yy<self.rows: self.grid[self.y+yy][self.x+xx]=self.co
            ng=[row for row in self.grid if any(c is None for c in row)]; cl=self.rows-len(ng)
            if cl: self.score+=cl*100; self.rec=max(self.rec,self.score); play(snd_eat)
            while len(ng)<self.rows: ng.insert(0,[None]*self.cols)
            self.grid=ng; self.sp()
            if self.col(0,0): play(snd_over); self.grid=[[None]*10 for _ in range(20)]; self.score=0
        self.dr()
    def dr(self,*a):
        self.canvas.clear()
        if self.width<10: return
        cw=self.width/self.cols; ch=self.height/self.rows
        with self.canvas:
            for y in range(self.rows):
                for x in range(self.cols):
                    Color(0.06,0.06,0.1,1); Rectangle(pos=(self.x+x*cw,self.y+(self.rows-1-y)*ch),size=(cw-1,ch-1))
                    if self.grid[y][x]: Color(*self.grid[y][x]); Rectangle(pos=(self.x+x*cw+1,self.y+(self.rows-1-y)*ch+1),size=(cw-2,ch-2))
            for yy,r in enumerate(self.sh):
                for xx,v in enumerate(r):
                    if v: Color(*self.co); Rectangle(pos=(self.x+(self.x+xx)*cw+1,self.y+(self.rows-1-(self.y+yy))*ch+1),size=(cw-2,ch-2))

class TScreen(BaseScreen):
    def __init__(self,**kw):
        super().__init__(**kw); m=BoxLayout(orientation='vertical'); m.add_widget(self.top_bar())
        self.lb=Label(text='Score: 0 Rec: 0',size_hint_y=0.07,bold=True); m.add_widget(self.lb)
        self.b=TBoard(); m.add_widget(self.b)
        m.add_widget(self.ctrls(lambda:self.mv(-1),lambda:self.mv(1),lambda:self.rt(),lambda:self.dn()))
        m.add_widget(Label(text=f'Corange Sistemas - PIX {PIX}',size_hint_y=0.05,color=(0,1,0.4,1),font_size=11))
        self.add_widget(m); Clock.schedule_interval(lambda dt:setattr(self.lb,'text',f'Score: {self.b.score} Rec: {self.b.rec}'),0.1)
    def mv(self,d): 
        if not self.b.col(d,0): self.b.x+=d; self.b.dr(); play(snd_move)
    def dn(self): 
        if not self.b.col(0,1): self.b.y+=1; self.b.dr(); play(snd_down)
    def rt(self):
        ns=[list(r) for r in zip(*self.b.sh[::-1])]
        if not self.b.col(0,0,ns): self.b.sh=ns; self.b.dr(); play(snd_rot)

# ============ COBRINHA ORIGINAL ============
class CBoard(Widget):
    def __init__(self,**kw):
        super().__init__(**kw); self.cols=15; self.rows=20; self.rs()
        Clock.schedule_interval(self.tk,0.18); self.bind(size=self.dr,pos=self.dr)
    def rs(self): self.sn=[(7,10),(7,11),(7,12)]; self.di=(0,-1); self.sc=0; self.rec=getattr(self,'rec',0); self.nf()
    def nf(self):
        while True:
            f=(random.randint(0,self.cols-1),random.randint(0,self.rows-1))
            if f not in self.sn: self.fr=f; break
    def tk(self,dt):
        hx,hy=self.sn[0]; nx=hx+self.di[0]; ny=hy+self.di[1]
        if nx<0 or nx>=self.cols or ny<0 or ny>=self.rows or (nx,ny) in self.sn: play(snd_over); self.rs(); return
        self.sn.insert(0,(nx,ny))
        if (nx,ny)==self.fr: self.sc+=10; self.rec=max(self.rec,self.sc); self.nf(); play(snd_eat)
        else: self.sn.pop()
        self.dr()
    def dr(self,*a):
        self.canvas.clear()
        if self.width<10: return
        cw=self.width/self.cols; ch=self.height/self.rows
        with self.canvas:
            for y in range(self.rows):
                for x in range(self.cols): Color(0.06,0.06,0.1,1); Rectangle(pos=(self.x+x*cw,self.y+(self.rows-1-y)*ch),size=(cw-1,ch-1))
            Color(1,0,0,1); Ellipse(pos=(self.x+self.fr[0]*cw+2,self.y+(self.rows-1-self.fr[1])*ch+2),size=(cw-4,ch-4))
            for i,(x,y) in enumerate(self.sn):
                Color(0.2,0.47,1,1) if i==0 else Color(0,1,0.4,1)
                Rectangle(pos=(self.x+x*cw+2,self.y+(self.rows-1-y)*ch+2),size=(cw-4,ch-4))

class CScreen(BaseScreen):
    def __init__(self,**kw):
        super().__init__(**kw); m=BoxLayout(orientation='vertical'); m.add_widget(self.top_bar())
        self.lb=Label(text='Score: 0 Rec: 0',size_hint_y=0.07,bold=True); m.add_widget(self.lb)
        self.b=CBoard(); m.add_widget(self.b)
        m.add_widget(self.ctrls(lambda:self.sd((-1,0)),lambda:self.sd((1,0)),lambda:self.sd((0,-1)),lambda:self.sd((0,1))))
        m.add_widget(Label(text=f'Corange Sistemas - PIX {PIX}',size_hint_y=0.05,color=(0,1,0.4,1),font_size=11))
        self.add_widget(m); Clock.schedule_interval(lambda dt:setattr(self.lb,'text',f'Score: {self.b.sc} Rec: {self.b.rec}'),0.1)
    def sd(self,d):
        if (d[0]*-1,d[1]*-1)!=self.b.di: self.b.di=d; play(snd_move)

# ============ BOMBERMAN 6 FASES ORIGINAL ============
class BBoard(Widget):
    def __init__(self,**kw):
        super().__init__(**kw); self.cols=13; self.rows=11; self.reset(); Clock.schedule_interval(self.tk,0.11); self.bind(size=self.dr,pos=self.dr)
    def reset(self): self.vidas=3; self.pontos=0; self.fase=1; self.setup()
    def setup(self):
        self.pl=[1,1]; self.bombs=[]; self.fires=[]; self.coins=[]; self.grid=[]
        for y in range(self.rows):
            row=[]
            for x in range(self.cols):
                if x==0 or y==0 or x==self.cols-1 or y==self.rows-1 or (x%2==0 and y%2==0): row.append(1)
                elif (x<3 and y<3) or (x>self.cols-4 and y<3) or (x<3 and y>self.rows-4) or (x>self.cols-4 and y>self.rows-4): row.append(0)
                elif random.random()<0.30: row.append(2)
                else: row.append(0)
            self.grid.append(row)
        qtd=3+(self.fase-1); ps=[[11,1],[11,9],[1,9],[11,5],[1,5],[6,9],[11,3],[1,3]]
        self.ens=[[ps[i][0],ps[i][1],i%3] for i in range(min(qtd,len(ps)))]
    def move(self,dx,dy):
        nx=self.pl[0]+dx; ny=self.pl[1]+dy
        if 0<=nx<self.cols and 0<=ny<self.rows and self.grid[ny][nx]==0:
            self.pl=[nx,ny]; play(snd_move)
            for c in self.coins[:]:
                if c[0]==nx and c[1]==ny: self.pontos+=100; self.coins.remove(c); play(snd_coin)
        self.dr()
    def bomb(self):
        x,y=self.pl
        if len(self.bombs)<2 and not any(b[0]==x and b[1]==y for b in self.bombs): self.bombs.append([x,y,18]); play(snd_bomb)
    def tk(self,dt):
        for b in self.bombs[:]:
            b[2]-=1
            if b[2]<=0:
                x,y,_=b; pts=[[x,y]]
                for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                    for i in range(1,3):
                        nx,ny=x+dx*i,y+dy*i
                        if not (0<=nx<self.cols and 0<=ny<self.rows): break
                        if self.grid[ny][nx]==1: break
                        pts.append([nx,ny])
                        if self.grid[ny][nx]==2:
                            self.grid[ny][nx]=0
                            if random.random()<0.4: self.coins.append([nx,ny,0])
                            break
                play(snd_exp)
                for fx,fy in pts:
                    self.fires.append([fx,fy,10])
                    if fx==self.pl[0] and fy==self.pl[1]: self.vidas-=1; self.pl=[1,1]; play(snd_over)
                    self.ens=[e for e in self.ens if not (e[0]==fx and e[1]==fy)]
                self.bombs.remove(b)
                if self.vidas<=0: self.reset()
        for f in self.fires[:]:
            f[2]-=1
            if f[2]<=0: self.fires.remove(f)
        for e in self.ens:
            if random.random()<0.25:
                dx,dy=random.choice([(1,0),(-1,0),(0,1),(0,-1)]); nx,ny=e[0]+dx,e[1]+dy
                if 0<=nx<self.cols and 0<=ny<self.rows and self.grid[ny][nx]==0: e[0],e[1]=nx,ny
                if e[0]==self.pl[0] and e[1]==self.pl[1]: self.vidas-=1; self.pl=[1,1]; play(snd_over)
                if self.vidas<=0: self.reset()
        if len(self.ens)==0:
            if self.fase<6: self.fase+=1
            else: self.fase=1
            self.setup()
        self.dr()
    def dr(self,*a):
        self.canvas.clear()
        if self.width<10: return
        cw=self.width/self.cols; ch=self.height/self.rows
        with self.canvas:
            for y in range(self.rows):
                for x in range(self.cols):
                    if self.fase==1: Color(0.24,0.76,0.20,1) if (x+y)%2==0 else Color(0.29,0.88,0.23,1)
                    elif self.fase==2: Color(0.85,0.76,0.84,1) if (x+y)%2==0 else Color(0.78,0.66,0.77,1)
                    elif self.fase==3: Color(0.18,0.77,0.69,1) if (x+y)%2==0 else Color(0.23,0.84,0.76,1)
                    elif self.fase==4: Color(0.24,0.76,0.2,1) if (x+y)%2==0 else Color(0.42,0.91,0.35,1)
                    elif self.fase==5: Color(0.10,0.54,0.91,1) if (x+y)%2==0 else Color(0.16,0.60,1,1)
                    else: Color(0.23,0.77,0.63,1) if (x+y)%2==0 else Color(0.29,0.85,0.69,1)
                    Rectangle(pos=(self.x+x*cw,self.y+(self.rows-1-y)*ch),size=(cw,ch))
                    t=self.grid[y][x]
                    if t==1:
                        if self.fase==1: Color(0.63,0.63,0.63,1)
                        elif self.fase==2: Color(0.42,0.18,0.35,1)
                        elif self.fase==3: Color(0.29,0.29,0.42,1)
                        elif self.fase==5: Color(0.47,0.47,0.54,1)
                        else: Color(0.63,0.85,0.75,1)
                        Rectangle(pos=(self.x+x*cw,self.y+(self.rows-1-y)*ch),size=(cw-1,ch-1))
                    elif t==2:
                        Color(0.78,0.78,0.78,1) if self.fase==1 else Color(0.91,0.88,0.85,1) if self.fase==2 else Color(0.91,0.76,0.29,1) if self.fase==3 else Color(0.78,0.60,0.35,1) if self.fase==4 else Color(0.31,0.31,0.38,1) if self.fase==5 else Color(0.94,0.85,0.69,1)
                        Rectangle(pos=(self.x+x*cw+3,self.y+(self.rows-1-y)*ch+3),size=(cw-6,ch-6))
            for mx,my,_ in self.coins: Color(1,0.8,0,1); Ellipse(pos=(self.x+mx*cw+5,self.y+(self.rows-1-my)*ch+5),size=(cw-10,ch-10))
            for fx,fy,_ in self.fires: Color(1,0.4,0,1); Rectangle(pos=(self.x+fx*cw+1,self.y+(self.rows-1-fy)*ch+1),size=(cw-2,ch-2))
            for bx,by,_ in self.bombs: Color(0.42,0.23,0.82,1); Ellipse(pos=(self.x+bx*cw+4,self.y+(self.rows-1-by)*ch+4),size=(cw-8,ch-8))
            for ex,ey,tipo in self.ens:
                Color(1,0.48,0.75,1) if tipo==0 else Color(0.3,0.65,1,1) if tipo==1 else Color(1,0.23,0.23,1)
                Ellipse(pos=(self.x+ex*cw+4,self.y+(self.rows-1-ey)*ch+4),size=(cw-8,ch-8))
            Color(0.16,0.49,1,1); Rectangle(pos=(self.x+self.pl[0]*cw+4,self.y+(self.rows-1-self.pl[1])*ch+4),size=(cw-8,ch-8))

class BScreen(BaseScreen):
    def __init__(self,**kw):
        super().__init__(**kw); m=BoxLayout(orientation='vertical'); m.add_widget(self.top_bar())
        self.lb=Label(text='VIDAS: ❤️❤️❤️ FASE: 1 PONTOS: 0',size_hint_y=0.07,bold=True,font_size=12); m.add_widget(self.lb)
        self.b=BBoard(); m.add_widget(self.b)
        m.add_widget(self.ctrls(lambda:self.b.move(-1,0),lambda:self.b.move(1,0),lambda:self.b.move(0,-1),lambda:self.b.move(0,1),extra=lambda:self.b.bomb(),et='BOMBA'))
        m.add_widget(Label(text=f'Corange Sistemas - PIX {PIX}',size_hint_y=0.05,color=(0,1,0.4,1),font_size=11))
        self.add_widget(m); Clock.schedule_interval(lambda dt:setattr(self.lb,'text',f"VIDAS: {'❤️'*self.b.vidas} FASE: {self.b.fase} PONTOS: {self.b.pontos} REC: {self.b.pontos}"),0.1)

class GameApp(App):
    def build(self):
        sm=ScreenManager(); sm.add_widget(MenuScreen(name='menu')); sm.add_widget(TScreen(name='tetris')); sm.add_widget(CScreen(name='cobra')); sm.add_widget(BScreen(name='bomber')); return sm
GameApp().run()
