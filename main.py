import random, os, math, struct, wave
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore
from kivy.core.audio import SoundLoader

# SOM DO JOGO EM CODIGO
def cria_som(nome, freq, dur):
    if os.path.exists(nome): return
    sr=44100; n=int(sr*dur)
    with wave.open(nome,'w') as f:
        f.setparams((1,2,sr,n,'NONE','not compressed'))
        for i in range(n):
            val=int(32767*0.4*(1-i/n)*math.sin(2*math.pi*freq*i/sr))
            f.writeframes(struct.pack('<h',val))
cria_som('bomb.wav',300,0.15); cria_som('expl.wav',150,0.4); cria_som('moeda.wav',1000,0.12)

class MenuApresentacao(BoxLayout):
    def __init__(self, app_ref, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=12, **kwargs)
        self.app=app_ref
        self.musica=None
        # MUSICA DA PRIMEIRA TELA = nes.mp3
        if os.path.exists('nes.mp3'):
            self.musica=SoundLoader.load('nes.mp3')
            if self.musica:
                self.musica.loop=True
                self.musica.play()
        if os.path.exists('icon.png'):
            self.add_widget(Image(source='icon.png', size_hint_y=0.45))
        else:
            self.add_widget(Label(text="Bomberman Corange", font_size='36sp', color=(1,0.8,0,1), bold=True, size_hint_y=0.25))
        self.add_widget(Label(text="Corange Sistemas", font_size='18sp', color=(1,1,1,1), bold=True, size_hint_y=0.08))
        self.add_widget(Label(text="☺  ●  ♥  ♦  ☠", font_size='42sp', size_hint_y=0.18))
        store=JsonStore('recordes.json')
        rec=store.get('bomber')['val'] if store.exists('bomber') else 0
        self.add_widget(Label(text=f"RECORDE: {rec}", font_size='18sp', color=(1,0.8,0,1), bold=True, size_hint_y=0.08))
        b=Button(text="▶  INICIAR JOGO", font_size='26sp', background_color=(1,0.8,0,1), bold=True, size_hint_y=0.18)
        b.bind(on_press=self.iniciar); self.add_widget(b)
        self.add_widget(Label(text="PIX 51993359782", font_size='18sp', color=(0.3,1,0.4,1), bold=True, size_hint_y=0.12))
    def iniciar(self,*a):
        if self.musica: self.musica.stop()
        self.app.iniciar_jogo()

class JogoBomberman(BoxLayout):
    def __init__(self, app_ref, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.app=app_ref; self.GW,self.GH=13,11
        self.fase=1; self.fase_max=6; self.vidas=3; self.pontos=0
        self.invencivel=0; self.game_over=False
        self.s_bomb=SoundLoader.load('bomb.wav'); self.s_expl=SoundLoader.load('expl.wav'); self.s_moeda=SoundLoader.load('moeda.wav')
        store=JsonStore('recordes.json'); self.recorde=store.get('bomber')['val'] if store.exists('bomber') else 0
        self.hud=Label(text="VIDAS: ❤️❤️❤️ | FASE: 1 | RECORDE: 0 | PONTOS: 0", font_size='13sp', size_hint_y=0.08, bold=True); self.add_widget(self.hud)
        self.tabuleiro=GridLayout(cols=self.GW, rows=self.GH, size_hint_y=0.62, spacing=1)
        self.blocos={}
        for r in range(self.GH):
            for c in range(self.GW):
                lbl=Label(text=' ', font_size='22sp', bold=True); self.tabuleiro.add_widget(lbl); self.blocos[(r,c)]=lbl
        self.add_widget(self.tabuleiro)
        ctrls=BoxLayout(orientation='horizontal', size_hint_y=0.28, padding=8, spacing=8)
        btn_l=Button(text="<", font_size='42sp', bold=True, background_color=(0.25,0.25,0.25,1), on_press=lambda x:self.mover(-1,0))
        btn_r=Button(text=">", font_size='42sp', bold=True, background_color=(0.25,0.25,0.25,1), on_press=lambda x:self.mover(1,0))
        v_box=BoxLayout(orientation='vertical', spacing=8)
        btn_u=Button(text="^", font_size='42sp', bold=True, background_color=(0.25,0.25,0.25,1), on_press=lambda x:self.mover(0,-1))
        btn_d=Button(text="v", font_size='42sp', bold=True, background_color=(0.25,0.25,0.25,1), on_press=lambda x:self.mover(0,1))
        v_box.add_widget(btn_u); v_box.add_widget(btn_d)
        btn_bomba=Button(text="BOMBA", font_size='16sp', bold=True, background_color=(1,0.6,0,1), on_press=lambda x:self.colocar_bomba())
        btn_menu=Button(text="MENU", font_size='14sp', bold=True, background_color=(0.6,0.2,0.2,1), on_press=lambda x:self.app.voltar_menu())
        ctrls.add_widget(btn_l); ctrls.add_widget(v_box); ctrls.add_widget(btn_r); ctrls.add_widget(btn_bomba); self.add_widget(ctrls)
        self.add_widget(btn_menu)
        self.reset(manter_pontos=False); self.evento=Clock.schedule_interval(self.atualizar,0.18)
    def atualizar_hud(self):
        coracoes="❤️"*self.vidas+"🖤"*(3-self.vidas)
        self.hud.text=f"VIDAS: {coracoes} | FASE: {self.fase} | RECORDE: {self.recorde} | PONTOS: {self.pontos}"
        if self.pontos>self.recorde: self.recorde=self.pontos; JsonStore('recordes.json').put('bomber',val=self.recorde)
    def reset(self, manter_pontos=False):
        self.grid=[]; self.player=[1,1]; self.bombas=[]; self.fogos=[]; self.moedas=[]; self.game_over=False
        if not manter_pontos: self.vidas=3; self.pontos=0
        self.invencivel=0; self.atualizar_hud()
        for y in range(self.GH):
            linha=[]
            for x in range(self.GW):
                if x==0 or y==0 or x==self.GW-1 or y==self.GH-1 or (x%2==0 and y%2==0): linha.append(1)
                elif (x<3 and y<3) or (x>self.GW-4 and y<3) or (x<3 and y>self.GH-4) or (x>self.GW-4 and y>self.GH-4): linha.append(0)
                elif random.random()<0.30: linha.append(2)
                else: linha.append(0)
            self.grid.append(linha)
        qtd=3+(self.fase-1)
        posicoes=[[self.GW-2,1],[self.GW-2,self.GH-2],[1,self.GH-2],[self.GW-2,self.GH//2],[1,self.GH//2],[self.GW//2,self.GH-2],[self.GW-2,3],[1,3]]
        self.inimigos=[]
        for i in range(min(qtd,len(posicoes))): self.inimigos.append([posicoes[i][0],posicoes[i][1],i%3])
    def mover(self,dx,dy):
        if self.game_over: return
        if len(self.inimigos)==0: self.avancar_fase(); return
        x,y=self.player; nx,ny=x+dx,y+dy
        if not (0<=nx<self.GW and 0<=ny<self.GH): return
        if self.grid[ny][nx]!=0: return
        if any(b[0]==nx and b[1]==ny for b in self.bombas): return
        if any(f[0]==nx and f[1]==ny for f in self.fogos):
            if self.invencivel==0: self.perder_vida()
            return
        if any(e[0]==nx and e[1]==ny for e in self.inimigos): return
        self.player=[nx,ny]
        for m in self.moedas[:]:
            if m[0]==nx and m[1]==ny:
                if m[2]==1:
                    if self.vidas<3: self.vidas+=1
                    else: self.pontos+=200
                else: self.pontos+=100
                self.moedas.remove(m)
                if self.s_moeda: self.s_moeda.play()
                self.atualizar_hud()
    def colocar_bomba(self):
        if self.game_over: return
        if len(self.inimigos)==0: self.avancar_fase(); return
        x,y=self.player
        if len(self.bombas)<2 and not any(b[0]==x and b[1]==y for b in self.bombas):
            self.bombas.append([x,y,6])
            if self.s_bomb: self.s_bomb.play()
    def avancar_fase(self):
        if self.fase<self.fase_max: self.fase+=1; self.reset(manter_pontos=True)
        else: self.fase=1; self.reset(manter_pontos=True)
    def perder_vida(self):
        self.vidas-=1; self.atualizar_hud()
        if self.vidas<=0: self.game_over=True; self.bombas.clear(); self.fogos.clear()
        else: self.player=[1,1]; self.invencivel=5; self.bombas.clear(); self.fogos.clear()
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
                    if any(f[0]==nx and f[1]==ny for f in self.fogos):
                        if en in self.inimigos:
                            self.inimigos.remove(en); self.pontos+=50; self.atualizar_hud()
                        break
                    if nx==self.player[0] and ny==self.player[1]: continue
                    en[0],en[1]=nx,ny; break
            if en not in self.inimigos: continue
            if en[0]==self.player[0] and en[1]==self.player[1] and self.invencivel==0: self.perder_vida(); break
        self.desenhar()
    def desenhar(self):
        for r in range(self.GH):
            for c in range(self.GW):
                lbl=self.blocos[(r,c)]; t=self.grid[r][c]
                if self.fase==1: cor_chao=(0.24,0.76,0.2,1)
                elif self.fase==2: cor_chao=(0.85,0.76,0.84,1)
                elif self.fase==3: cor_chao=(0.18,0.77,0.69,1)
                elif self.fase==4: cor_chao=(0.24,0.76,0.2,1)
                elif self.fase==5: cor_chao=(0.1,0.54,0.91,1)
                else: cor_chao=(0.23,0.77,0.63,1)
                if t==1:
                    if self.fase==1: lbl.text='█'; lbl.color=(0.63,0.63,0.63,1)
                    elif self.fase==2: lbl.text='█'; lbl.color=(0.42,0.18,0.35,1)
                    elif self.fase==3: lbl.text='◉'; lbl.color=(0.61,0.30,0.80,1)
                    elif self.fase==4: lbl.text='▓'; lbl.color=(0.54,0.61,0.69,1)
                    elif self.fase==5: lbl.text='⬣'; lbl.color=(0.31,0.31,0.35,1)
                    else: lbl.text='█'; lbl.color=(0.63,0.85,0.75,1)
                elif t==2:
                    if self.fase==3: lbl.text='☺'; lbl.color=(1,0.9,0.3,1)
                    elif self.fase==5: lbl.text='■'; lbl.color=(0.31,0.31,0.38,1)
                    else: lbl.text='▓'; lbl.color=(0.8,0.8,0.5,1)
                else: lbl.text='·'; lbl.color=cor_chao
        for mx,my,tipo in self.moedas:
            self.blocos[(my,mx)].text='♥' if tipo==1 else '$'
            self.blocos[(my,mx)].color=(0.2,1,0.3,1) if tipo==1 else (1,0.8,0,1)
        for fx,fy,_ in self.fogos: self.blocos[(fy,fx)].text='*'; self.blocos[(fy,fx)].color=(1,0.4,0,1)
        for bx,by,t in self.bombas: self.blocos[(by,bx)].text='●'; self.blocos[(by,bx)].color=(0.42,0.23,0.82,1)
        for en in self.inimigos:
            if en[2]==0: self.blocos[(en[1],en[0])].text='♥'; self.blocos[(en[1],en[0])].color=(1,0.48,0.75,1)
            elif en[2]==1: self.blocos[(en[1],en[0])].text='♦'; self.blocos[(en[1],en[0])].color=(0.3,0.65,1,1)
            else: self.blocos[(en[1],en[0])].text='☠'; self.blocos[(en[1],en[0])].color=(1,0.23,0.23,1)
        px,py=self.player
        if not (self.invencivel>0 and self.invencivel%2==0): self.blocos[(py,px)].text='☺'; self.blocos[(py,px)].color=(0.16,0.49,1,1)
        if self.game_over: self.hud.text="GAME OVER! Volte ao menu"
        elif len(self.inimigos)==0:
            if self.fase==self.fase_max: self.hud.text="VOCE ZEROU! Aperte BOMBA p/ jogar de novo"
            else: self.hud.text=f"FASE {self.fase} COMPLETA! Aperte BOMBA p/ proxima"

class MainApp(App):
    icon = 'icon.png'
    def build(self):
        self.title="Bomberman Corange"
        self.root=BoxLayout()
        self.voltar_menu()
        return self.root
    def voltar_menu(self):
        self.root.clear_widgets(); self.root.add_widget(MenuApresentacao(self))
    def iniciar_jogo(self):
        self.root.clear_widgets(); self.root.add_widget(JogoBomberman(self))

if __name__=='__main__': MainApp().run()
