import random, math, struct, wave, os
from kivy.app import App
from kivy.config import Config
Config.set('graphics', 'resizable', '0')
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore
from kivy.core.audio import SoundLoader

def cria_som(nome, freq, dur, freq2=0):
    if os.path.exists(nome): return
    sr=44100; n=int(sr*dur)
    with wave.open(nome,'w') as f:
        f.setparams((1,2,sr,n,'NONE','not compressed'))
        for i in range(n):
            vol=0.4*(1-i/n)
            fr = freq if freq2==0 or i < n//2 else freq2
            val=int(32767*vol*math.sin(2*math.pi*fr*i/sr))
            f.writeframes(struct.pack('<h',val))

cria_som('anda.wav',800,0.05)
cria_som('come.wav',1200,0.2)
cria_som('bate.wav',150,0.4)
cria_som('tet_giro.wav',600,0.12)
cria_som('tet_lado.wav',400,0.08)
cria_som('tet_baixo.wav',250,0.08)
cria_som('tet_ponto.wav',900,0.15,1500)
cria_som('tet_fim.wav',120,0.6)
cria_som('bomb.wav',300,0.15)
cria_som('expl.wav',150,0.4)
cria_som('moeda.wav',1000,0.12)

class MenuInicial(BoxLayout):
    def __init__(self, app_ref, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=12, **kwargs)
        self.app=app_ref
        # TOCA NES.WAV NO MENU DOS 3 BOTOES
        self.som_menu = SoundLoader.load('nes.wav')
        if self.som_menu:
            self.som_menu.loop = True
            self.som_menu.play()
        self.add_widget(Label(text="Corange Software", font_size='32sp', color=(0,1,0.4,1), bold=True, size_hint_y=0.28))
        btn_cobra=Button(text="JOGAR COBRINHA", font_size='18sp', background_color=(0,0.8,0.3,1), bold=True, size_hint_y=0.11)
        btn_cobra.bind(on_press=self.app.iniciar_cobrinha)
        self.add_widget(btn_cobra)
        btn_tetris=Button(text="JOGAR TETRIS", font_size='18sp', background_color=(0,0.4,1,1), bold=True, size_hint_y=0.11)
        btn_tetris.bind(on_press=self.app.iniciar_tetris)
        self.add_widget(btn_tetris)
        btn_bomb=Button(text="JOGAR BOMBERMAN", font_size='18sp', background_color=(1,0.6,0,1), bold=True, size_hint_y=0.11)
        btn_bomb.bind(on_press=self.app.iniciar_bomberman)
        self.add_widget(btn_bomb)
        store=JsonStore('recordes.json')
        rec_c=store.get('cobra')['val'] if store.exists('cobra') else 0
        rec_t=store.get('tetris')['val'] if store.exists('tetris') else 0
        rec_b=store.get('bomber')['val'] if store.exists('bomber') else 0
        self.add_widget(Label(text=f"Cobrinha: {rec_c} | Tetris: {rec_t} | Bomber: {rec_b}", font_size='14sp', size_hint_y=0.12))
        self.add_widget(Label(text="Corange Software - PIX 51993359782", font_size='14sp', color=(0,1,0.4,1), size_hint_y=0.12))
    def parar_som(self):
        if hasattr(self, 'som_menu') and self.som_menu:
            self.som_menu.stop()

class JogoCobrinha(BoxLayout):
    def __init__(self, app_ref, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.app=app_ref; self.cols_c,self.rows_c=30,16; self.score=0
        self.som_anda=SoundLoader.load('anda.wav'); self.som_come=SoundLoader.load('come.wav'); self.som_bate=SoundLoader.load('bate.wav')
        self.hud=Label(text=f"Score: {self.score}", font_size='20sp', size_hint_y=0.1)
        self.add_widget(self.hud)
        self.tabuleiro=GridLayout(cols=self.cols_c, rows=self.rows_c, size_hint_y=0.6, spacing=1, padding=0)
        self.blocos={}
        for r in range(self.rows_c):
            for c in range(self.cols_c):
                lbl=Label(text=' ', font_size='18sp'); self.tabuleiro.add_widget(lbl); self.blocos[(r,c)]=lbl
        self.add_widget(self.tabuleiro)
        ctrls=BoxLayout(orientation='horizontal', size_hint_y=0.3, padding=10, spacing=10)
        btn_l=Button(text="<", font_size='42sp', bold=True, background_color=(0.3,0.3,0.3,1), on_press=lambda x:self.mudar_dir(-1,0))
        btn_r=Button(text=">", font_size='42sp', bold=True, background_color=(0.3,0.3,0.3,1), on_press=lambda x:self.mudar_dir(1,0))
        v_box=BoxLayout(orientation='vertical', spacing=10)
        btn_u=Button(text="^", font_size='42sp', bold=True, background_color=(0.3,0.3,0.3,1), on_press=lambda x:self.mudar_dir(0,-1))
        btn_d=Button(text="v", font_size='42sp', bold=True, background_color=(0.3,0.3,0.3,1), on_press=lambda x:self.mudar_dir(0,1))
        v_box.add_widget(btn_u); v_box.add_widget(btn_d)
        ctrls.add_widget(btn_l); ctrls.add_widget(v_box); ctrls.add_widget(btn_r)
        self.add_widget(ctrls); self.reset_game(); self.evento=Clock.schedule_interval(self.atualizar,0.45)
    def reset_game(self):
        self.cx,self.cy=self.cols_c//2,self.rows_c//2; self.vx,self.vy=1,0; self.corpo=[(self.cx,self.cy)]
        self.mx,self.my=random.randint(0,self.cols_c-1),random.randint(0,self.rows_c-1)
    def mudar_dir(self,x,y):
        if (x!=0 and self.vx==0) or (y!=0 and self.vy==0): self.vx,self.vy=x,y
    def mostrar_game_over(self):
        self.clear_widgets()
        self.add_widget(Label(text="GAME OVER", font_size='50sp', color=(1,0,0,1), bold=True))
        self.add_widget(Label(text=f"Score: {self.score}", font_size='30sp'))
        store=JsonStore('recordes.json'); rec=store.get('cobra')['val'] if store.exists('cobra') else 0
        self.add_widget(Label(text=f"Recorde: {rec}", font_size='20sp', color=(0,1,0.4,1)))
        b1=Button(text="REINICIAR", font_size='26sp', background_color=(0,0.8,0.3,1), bold=True, size_hint_y=0.25)
        b1.bind(on_press=lambda x:self.reiniciar_jogo()); self.add_widget(b1)
        b2=Button(text="MENU", font_size='20sp', background_color=(0.3,0.3,0.3,1), size_hint_y=0.15)
        b2.bind(on_press=lambda x:self.app.voltar_menu()); self.add_widget(b2)
    def reiniciar_jogo(self): self.clear_widgets(); self.__init__(self.app)
    def atualizar(self,dt):
        self.cx+=self.vx; self.cy+=self.vy
        if self.cx<0 or self.cx>=self.cols_c or self.cy<0 or self.cy>=self.rows_c or (self.cx,self.cy) in self.corpo:
            if self.som_bate: self.som_bate.play()
            Clock.unschedule(self.evento); self.app.gravar_recorde('cobra',self.score); self.mostrar_game_over(); return
        if self.som_anda: self.som_anda.stop(); self.som_anda.play()
        self.corpo.append((self.cx,self.cy))
        if self.cx==self.mx and self.cy==self.my:
            if self.som_come: self.som_come.play()
            self.score+=10; self.hud.text=f"Score: {self.score}"
            self.mx,self.my=random.randint(0,self.cols_c-1),random.randint(0,self.rows_c-1)
        else: self.corpo.pop(0)
        for lbl in self.blocos.values(): lbl.text=' '
        for idx,(bx,by) in enumerate(self.corpo):
            if 0<=by<self.rows_c and 0<=bx<self.cols_c:
                self.blocos[(by,bx)].text='█'; self.blocos[(by,bx)].color=(0,0.5,1,1) if idx==len(self.corpo)-1 else (0,1,0.2,1)
        self.blocos[(self.my,self.mx)].text='█'; self.blocos[(self.my,self.mx)].color=(1,0.6,0,1)

class JogoTetris(BoxLayout):
    def __init__(self, app_ref, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.app=app_ref; self.COLS,self.LINHAS,self.LIMITE=10,20,17; self.score=0
        self.board=[[0]*self.COLS for _ in range(self.LINHAS)]
        self.s_giro=SoundLoader.load('tet_giro.wav'); self.s_lado=SoundLoader.load('tet_lado.wav')
        self.s_baixo=SoundLoader.load('tet_baixo.wav'); self.s_ponto=SoundLoader.load('tet_ponto.wav')
        self.s_fim=SoundLoader.load('tet_fim.wav')
        self.hud=Label(text=f"Score: 0 Alt: 0/{self.LIMITE}", font_size='18sp', size_hint_y=0.08)
        self.add_widget(self.hud)
        self.tabuleiro=GridLayout(cols=self.COLS, rows=self.LINHAS, size_hint_y=0.62, spacing=1)
        self.blocos={}
        for r in range(self.LINHAS):
            for c in range(self.COLS):
                lbl=Label(text=' ', font_size='18sp'); self.tabuleiro.add_widget(lbl); self.blocos[(r,c)]=lbl
        self.add_widget(self.tabuleiro)
        ctrls=BoxLayout(orientation='horizontal', size_hint_y=0.28, padding=8, spacing=8)
        btn_l=Button(text="<", font_size='42sp', bold=True, background_color=(0.25,0.25,0.25,1), on_press=lambda x:self.mover(-1))
        btn_r=Button(text=">", font_size='42sp', bold=True, background_color=(0.25,0.25,0.25,1), on_press=lambda x:self.mover(1))
        v_box=BoxLayout(orientation='vertical', spacing=8)
        btn_u=Button(text="O", font_size='36sp', bold=True, background_color=(0.2,0.5,0.9,1), on_press=lambda x:self.girar())
        btn_d=Button(text="v", font_size='42sp', bold=True, background_color=(0.25,0.25,0.25,1), on_press=lambda x:self.descer())
        v_box.add_widget(btn_u); v_box.add_widget(btn_d)
        ctrls.add_widget(btn_l); ctrls.add_widget(v_box); ctrls.add_widget(btn_r)
        self.add_widget(ctrls)
        self.add_widget(Label(text="Corange Software - PIX 51993359782", font_size='12sp', color=(0,1,0.4,1), size_hint_y=0.06))
        self.PECAS=[[[1,1,1,1]],[[1,1],[1,1]],[[1,1,1],[0,1,0]],[[1,1,0],[0,1,1]],[[0,1,1],[1,1,0]],[[1,1,1],[1,0,0]],[[1,1,1],[0,0,1]]]
        self.CORES=[(0,1,1,1),(1,1,0,1),(0.7,0,1,1),(0,1,0,1),(1,0,0,1),(0,0.4,1,1),(1,0.6,0,1)]
        self.nova_peca(); self.evento=Clock.schedule_interval(self.atualizar,0.5)
    def nova_peca(self):
        self.peca=random.choice(self.PECAS); self.cor=random.choice(self.CORES)
        self.px=self.COLS//2-len(self.peca[0])//2; self.py=0
    def colide(self,px,py,forma):
        for y,row in enumerate(forma):
            for x,v in enumerate(row):
                if v:
                    nx,ny=px+x,py+y
                    if nx<0 or nx>=self.COLS or ny>=self.LINHAS or (ny>=0 and self.board[ny][nx]!=0): return True
        return False
    def mover(self,dx):
        if not self.colide(self.px+dx,self.py,self.peca):
            self.px+=dx
            if self.s_lado: self.s_lado.play()
    def descer(self):
        if not self.colide(self.px,self.py+1,self.peca):
            self.py+=1
            if self.s_baixo: self.s_baixo.play()
    def girar(self):
        rot=[list(reversed(c)) for c in zip(*self.peca)]
        if not self.colide(self.px,self.py,rot):
            self.peca=rot
            if self.s_giro: self.s_giro.play()
    def altura_atual(self):
        for y in range(self.LINHAS):
            if any(self.board[y]): return self.LINHAS-y
        return 0
    def mostrar_game_over(self):
        self.clear_widgets()
        self.add_widget(Label(text="GAME OVER", font_size='50sp', color=(1,0,0,1), bold=True))
        self.add_widget(Label(text=f"Score: {self.score}", font_size='30sp'))
        b1=Button(text="REINICIAR", font_size='26sp', background_color=(0,0.4,1,1), bold=True, size_hint_y=0.25)
        b1.bind(on_press=lambda x:self.reiniciar_jogo()); self.add_widget(b1)
        b2=Button(text="MENU", font_size='20sp', background_color=(0.3,0.3,0.3,1), size_hint_y=0.15)
        b2.bind(on_press=lambda x:self.app.voltar_menu()); self.add_widget(b2)
    def reiniciar_jogo(self): self.clear_widgets(); self.__init__(self.app)
    def atualizar(self,dt):
        if not self.colide(self.px,self.py+1,self.peca): self.py+=1
        else:
            for dy,row in enumerate(self.peca):
                for dx,v in enumerate(row):
                    if v and 0<=self.py+dy<self.LINHAS: self.board[self.py+dy][self.px+dx]=self.cor
            novas=[]; limp=0
            for l in self.board:
                if all(l): limp+=1
                else: novas.append(l[:])
            while len(novas)<self.LINHAS: novas.insert(0,[0]*self.COLS)
            self.board=novas
            if limp>0:
                self.score+=limp*100
                if self.s_ponto: self.s_ponto.play()
            self.nova_peca()
            if self.colide(self.px,self.py,self.peca) or self.altura_atual()>=self.LIMITE:
                Clock.unschedule(self.evento)
                if self.s_fim: self.s_fim.play()
                self.app.gravar_recorde('tetris',self.score)
                self.mostrar_game_over(); return
        self.hud.text=f"Score: {self.score} Alt: {self.altura_atual()}/{self.LIMITE}"
        for r in range(self.LINHAS):
            for c in range(self.COLS):
                lbl=self.blocos[(r,c)]
                if self.board[r][c]: lbl.text='█'; lbl.color=self.board[r][c]
                else:
                    is_peca=False
                    for dy,row in enumerate(self.peca):
                        for dx,v in enumerate(row):
                            if v and self.py+dy==r and self.px+dx==c:
                                lbl.text='█'; lbl.color=self.cor; is_peca=True
                    if not is_peca: lbl.text=' '

# ============ BOMBERMAN 6 FASES - KIVY ============
class JogoBomberman(BoxLayout):
    def __init__(self, app_ref, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.app=app_ref
        self.GW,self.GH=13,11
        self.fase=1; self.fase_max=6; self.vidas=3; self.pontos=0
        self.invencivel=0; self.game_over=False
        self.s_bomb=SoundLoader.load('bomb.wav'); self.s_expl=SoundLoader.load('expl.wav'); self.s_moeda=SoundLoader.load('moeda.wav')
        self.hud=Label(text="VIDAS: 3 | FASE: 1/6 | PONTOS: 0", font_size='16sp', size_hint_y=0.08, bold=True)
        self.add_widget(self.hud)
        self.tabuleiro=GridLayout(cols=self.GW, rows=self.GH, size_hint_y=0.62, spacing=1)
        self.blocos={}
        for r in range(self.GH):
            for c in range(self.GW):
                lbl=Label(text=' ', font_size='20sp', bold=True); self.tabuleiro.add_widget(lbl); self.blocos[(r,c)]=lbl
        self.add_widget(self.tabuleiro)
        ctrls=BoxLayout(orientation='horizontal', size_hint_y=0.28, padding=8, spacing=8)
        btn_l=Button(text="<", font_size='42sp', bold=True, background_color=(0.25,0.25,0.25,1), on_press=lambda x:self.mover(-1,0))
        btn_r=Button(text=">", font_size='42sp', bold=True, background_color=(0.25,0.25,0.25,1), on_press=lambda x:self.mover(1,0))
        v_box=BoxLayout(orientation='vertical', spacing=8)
        btn_u=Button(text="^", font_size='42sp', bold=True, background_color=(0.25,0.25,0.25,1), on_press=lambda x:self.mover(0,-1))
        btn_d=Button(text="v", font_size='42sp', bold=True, background_color=(0.25,0.25,0.25,1), on_press=lambda x:self.mover(0,1))
        v_box.add_widget(btn_u); v_box.add_widget(btn_d)
        btn_bomba=Button(text="BOMBA", font_size='16sp', bold=True, background_color=(1,0.6,0,1), on_press=lambda x:self.colocar_bomba())
        ctrls.add_widget(btn_l); ctrls.add_widget(v_box); ctrls.add_widget(btn_r); ctrls.add_widget(btn_bomba)
        self.add_widget(ctrls)
        self.add_widget(Label(text="Corange Software - PIX 51993359782", font_size='12sp', color=(0,1,0.4,1), size_hint_y=0.05))
        self.reset(manter_pontos=False)
        self.evento=Clock.schedule_interval(self.atualizar,0.18)
    def reset(self, manter_pontos=False):
        self.grid=[]; self.player=[1,1]; self.bombas=[]; self.fogos=[]; self.moedas=[]; self.game_over=False
        if not manter_pontos:
            self.vidas=3; self.pontos=0
        self.invencivel=0
        for y in range(self.GH):
            linha=[]
            for x in range(self.GW):
                if x==0 or y==0 or x==self.GW-1 or y==self.GH-1 or (x%2==0 and y%2==0):
                    linha.append(1)
                elif (x<3 and y<3) or (x>self.GW-4 and y<3) or (x<3 and y>self.GH-4) or (x>self.GW-4 and y>self.GH-4):
                    linha.append(0)
                elif random.random()<0.30:
                    linha.append(2)
                else: linha.append(0)
            self.grid.append(linha)
        qtd=3+(self.fase-1)
        posicoes=[[self.GW-2,1],[self.GW-2,self.GH-2],[1,self.GH-2],[self.GW-2,self.GH//2],[1,self.GH//2],[self.GW//2,self.GH-2],[self.GW-2,3],[1,3]]
        self.inimigos=[]
        for i in range(min(qtd,len(posicoes))):
            self.inimigos.append([posicoes[i][0],posicoes[i][1],i%3])
        self.atualizar_hud()
    def atualizar_hud(self):
        self.hud.text=f"VIDAS: {self.vidas} | FASE: {self.fase}/6 | PONTOS: {self.pontos}"
    def mover(self,dx,dy):
        if self.game_over: return
        if len(self.inimigos)==0:
            self.avancar_fase(); return
        x,y=self.player; nx,ny=x+dx,y+dy
        if 0<=nx<self.GW and 0<=ny<self.GH and self.grid[ny][nx]==0:
            if not any(e[0]==nx and e[1]==ny for e in self.inimigos):
                self.player=[nx,ny]
                for m in self.moedas[:]:
                    if m[0]==nx and m[1]==ny:
                        self.pontos+=100; self.moedas.remove(m)
                        if self.s_moeda: self.s_moeda.play()
                        self.atualizar_hud()
    def colocar_bomba(self):
        if self.game_over: return
        x,y=self.player
        if len(self.bombas)<2 and not any(b[0]==x and b[1]==y for b in self.bombas):
            self.bombas.append([x,y,6])
            if self.s_bomb: self.s_bomb.play()
    def avancar_fase(self):
        if self.fase<self.fase_max:
            self.fase+=1; self.reset(manter_pontos=True)
        else:
            self.app.gravar_recorde('bomber',self.pontos)
            self.mostrar_zerou()
    def mostrar_zerou(self):
        Clock.unschedule(self.evento)
        self.clear_widgets()
        self.add_widget(Label(text="VOCE ZEROU!", font_size='48sp', color=(1,0.8,0,1), bold=True))
        self.add_widget(Label(text=f"Pontos: {self.pontos}", font_size='30sp'))
        b1=Button(text="JOGAR NOVAMENTE", font_size='22sp', background_color=(1,0.6,0,1), bold=True, size_hint_y=0.25)
        b1.bind(on_press=lambda x:self.reiniciar_jogo()); self.add_widget(b1)
        b2=Button(text="MENU", font_size='20sp', background_color=(0.3,0.3,0.3,1), size_hint_y=0.15)
        b2.bind(on_press=lambda x:self.app.voltar_menu()); self.add_widget(b2)
    def mostrar_game_over(self):
        Clock.unschedule(self.evento)
        self.clear_widgets()
        self.add_widget(Label(text="GAME OVER", font_size='50sp', color=(1,0,0,1), bold=True))
        self.add_widget(Label(text=f"Pontos: {self.pontos} | Fase: {self.fase}", font_size='26sp'))
        b1=Button(text="REINICIAR", font_size='26sp', background_color=(1,0.6,0,1), bold=True, size_hint_y=0.25)
        b1.bind(on_press=lambda x:self.reiniciar_jogo()); self.add_widget(b1)
        b2=Button(text="MENU", font_size='20sp', background_color=(0.3,0.3,0.3,1), size_hint_y=0.15)
        b2.bind(on_press=lambda x:self.app.voltar_menu()); self.add_widget(b2)
    def reiniciar_jogo(self):
        self.clear_widgets(); self.__init__(self.app)
        self.fase=1
    def perder_vida(self):
        self.vidas-=1; self.atualizar_hud()
        if self.vidas<=0:
            self.game_over=True
            self.app.gravar_recorde('bomber',self.pontos)
            self.mostrar_game_over()
        else:
            self.player=[1,1]; self.invencivel=5; self.bombas.clear(); self.fogos.clear()
    def explodir(self,b):
        x,y,_=b
        if self.s_expl: self.s_expl.play()
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
                        self.moedas.append([nx,ny])
                    break
        for fx,fy in pos:
            self.fogos.append([fx,fy,3])
            if fx==self.player[0] and fy==self.player[1] and self.invencivel==0:
                self.perder_vida()
            for en in self.inimigos[:]:
                if en[0]==fx and en[1]==fy:
                    self.inimigos.remove(en); self.pontos+=50; self.atualizar_hud()
    def atualizar(self,dt):
        if self.game_over: return
        if self.invencivel>0: self.invencivel-=1
        for b in self.bombas[:]:
            b[2]-=1
            if b[2]<=0:
                self.explodir(b); self.bombas.remove(b)
        for f in self.fogos[:]:
            f[2]-=1
            if f[2]<=0: self.fogos.remove(f)
        for en in self.inimigos:
            if random.random()<0.5:
                dirs=[(1,0),(-1,0),(0,1),(0,-1)]; random.shuffle(dirs)
                for dx,dy in dirs:
                    nx,ny=en[0]+dx,en[1]+dy
                    if 0<=nx<self.GW and 0<=ny<self.GH and self.grid[ny][nx]==0:
                        en[0],en[1]=nx,ny; break
            if en[0]==self.player[0] and en[1]==self.player[1] and self.invencivel==0:
                self.perder_vida(); break
        for r in range(self.GH):
            for c in range(self.GW):
                lbl=self.blocos[(r,c)]
                lbl.text=' '; lbl.color=(1,1,1,1)
                t=self.grid[r][c]
                if t==1: lbl.text='█'; lbl.color=(0.6,0.6,0.6,1)
                elif t==2: lbl.text='▓'; lbl.color=(0.8,0.8,0.5,1)
        for mx,my in self.moedas:
            self.blocos[(my,mx)].text='$'; self.blocos[(my,mx)].color=(1,0.8,0,1)
        for fx,fy,_ in self.fogos:
            self.blocos[(fy,fx)].text='*'; self.blocos[(fy,fx)].color=(1,0.3,0,1)
        for bx,by,_ in self.bombas:
            self.blocos[(by,bx)].text='●'; self.blocos[(by,bx)].color=(0.4,0,1,1)
        for en in self.inimigos:
            self.blocos[(en[1],en[0])].text='☠'; self.blocos[(en[1],en[0])].color=(1,0,0.5,1)
        px,py=self.player
        if not (self.invencivel>0 and self.invencivel%2==0):
            self.blocos[(py,px)].text='☺'; self.blocos[(py,px)].color=(0,0.5,1,1)
        if len(self.inimigos)==0 and not self.game_over:
            self.hud.text=f"FASE {self.fase} COMPLETA! Aperte qualquer seta p/ proxima"

class MainApp(App):
    def build(self):
        self.title="Corange Software"; self.root=BoxLayout(orientation='vertical'); self.voltar_menu(); return self.root
    def parar_som_menu(self):
        for w in self.root.children:
            if hasattr(w, 'parar_som'): w.parar_som()
    def voltar_menu(self): self.root.clear_widgets(); self.root.add_widget(MenuInicial(self))
    def iniciar_cobrinha(self,instance): self.parar_som_menu(); self.root.clear_widgets(); self.root.add_widget(JogoCobrinha(self))
    def iniciar_tetris(self,instance): self.parar_som_menu(); self.root.clear_widgets(); self.root.add_widget(JogoTetris(self))
    def iniciar_bomberman(self,instance): self.parar_som_menu(); self.root.clear_widgets(); self.root.add_widget(JogoBomberman(self))
    def gravar_recorde(self,tipo,valor):
        store=JsonStore('recordes.json'); atual=store.get(tipo)['val'] if store.exists(tipo) else 0
        if valor>atual: store.put(tipo,val=valor)

if __name__=='__main__': MainApp().run()
