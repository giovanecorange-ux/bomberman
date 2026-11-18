import os, json, random, math, wave, struct, copy
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

ARQ_RECORDE = "recorde_pacman.json"
PIX_KEY = "51993359782"

def salvar_recorde(fase, pontos):
    try:
        antigo = carregar_recorde()
        if antigo.get("pontos", 0) >= pontos:
            return antigo
        dados = {"fase": fase, "pontos": pontos}
        with open(ARQ_RECORDE, "w") as f:
            json.dump(dados, f)
        return dados
    except Exception:
        return {"fase": fase, "pontos": pontos}

def carregar_recorde():
    try:
        if os.path.exists(ARQ_RECORDE):
            with open(ARQ_RECORDE, "r") as f:
                return json.load(f)
    except Exception:
        pass
    return {"fase": 1, "pontos": 0}

def criar_bip(nome, freq, duracao=0.2, volume=0.5):
    try:
        if os.path.exists(nome):
            return
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
    except Exception:
        pass

_sons_cache = {}
def tocar_bip(nome):
    try:
        if not os.path.exists(nome):
            return
        if nome not in _sons_cache:
            _sons_cache[nome] = SoundLoader.load(nome)
        s = _sons_cache.get(nome)
        if s:
            s.stop()
            s.play()
    except Exception:
        pass

MAPA_TXT = [
    "########## ##########",
    "#P........#........P#",
    "#.###.###.#.###.###.#",
    "#.#...............#.#",
    "#.#.###.#####.###.#.#",
    "#.....#...#...#.....#",
    "#####.###...###.#####",
    "#.........#.........#",
    "#.###.###...###.###.#",
    "#.#.......#.......#.#",
    "#.#.###.#####.###.#.#",
    "#.....#...#...#.....#",
    "#####.###.#.###.#####",
    "#.#...............#.#",
    "#.###.###.#.###.###.#",
    "#P........#........P#",
    "########## ##########",
]

def mapa_de_texto(linhas):
    out = []
    for l in linhas:
        l = l[:21].ljust(21, '#')
        linha = []
        for ch in l:
            if ch == '#': linha.append(1)
            elif ch == 'P': linha.append(2)
            else: linha.append(0)
        out.append(linha)
    return out

FASES_SKINS = [
    {"fixo": (1.00, 0.82, 0.10, 1), "nome": "Atari Amarelo"},
    {"fixo": (0.20, 0.90, 0.35, 1), "nome": "Atari Verde"},
    {"fixo": (1.00, 0.35, 0.65, 1), "nome": "Atari Rosa"},
    {"fixo": (0.25, 0.85, 1.00, 1), "nome": "Atari Ciano"},
    {"fixo": (1.00, 0.50, 0.15, 1), "nome": "Atari Laranja"},
]

class Bloco(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tipo = 'chao'; self.l=0; self.c=0
        self.bind(pos=self._redesenhar, size=self._redesenhar)
    def _redesenhar(self, *args): self.desenhar(self.tipo, None, None)
    def desenhar(self, tipo, cor_fase=None, skin=None, inimigo_tipo='vermelho', casa_set=None, porta=None, parede_set=None):
        self.tipo = tipo; self.canvas.clear()
        x, y = self.pos; w, h = self.size
        if w <= 1 or h <= 1: return
        fixo = skin["fixo"] if skin else (1, 0.82, 0.1, 1)
        with self.canvas:
            Color(0, 0, 0.7, 1); Rectangle(pos=(x, y), size=(w, h))
            if tipo == 'fixo':
                Color(*fixo); Line(rectangle=(x+1,y+1,w-2,h-2), width=1.6); return
            elif tipo == 'pastilha':
                m=min(w,h); Color(0.85,0.65,0.2,1); Rectangle(pos=(x+(w-m*0.45)/2, y+(h-m*0.18)/2), size=(m*0.45, m*0.18)); return
            elif tipo == 'poder':
                m=min(w,h); Color(0.2,1,0.3,1); Rectangle(pos=(x+(w-m*0.65)/2, y+(h-m*0.65)/2), size=(m*0.65, m*0.65)); return
            elif tipo == 'player':
                Color(1,1,0,1); Ellipse(pos=(x+w*0.10, y+h*0.10), size=(w*0.80, h*0.80)); Color(0,0,0,1); Triangle(points=[x+w*0.55,y+h*0.5,x+w*0.95,y+h*0.70,x+w*0.95,y+h*0.30]); return
            elif tipo == 'assustado':
                Color(0,0,1,1); Ellipse(pos=(x+w*0.10, y+h*0.20), size=(w*0.80, h*0.60)); Rectangle(pos=(x+w*0.10, y+h*0.05), size=(w*0.80, h*0.30)); Color(1,1,1,1); Ellipse(pos=(x+w*0.24, y+h*0.50), size=(w*0.20, h*0.24)); Ellipse(pos=(x+w*0.56, y+h*0.50), size=(w*0.20, h*0.24)); return
            elif tipo == 'inimigo':
                cores={'vermelho':(1,0,0,1),'rosa':(1,0.6,0.8,1),'ciano':(0,1,1,1),'laranja':(1,0.6,0,1)}; c=cores.get(inimigo_tipo,(1,0,0,1)); Color(*c); Ellipse(pos=(x+w*0.10, y+h*0.20), size=(w*0.80, h*0.60)); Rectangle(pos=(x+w*0.10, y+h*0.05), size=(w*0.80, h*0.30)); Color(1,1,1,1); Ellipse(pos=(x+w*0.24, y+h*0.50), size=(w*0.20, h*0.24)); Ellipse(pos=(x+w*0.56, y+h*0.50), size=(w*0.20, h*0.24)); Color(0,0,0,1); Ellipse(pos=(x+w*0.30, y+h*0.54), size=(w*0.09, h*0.14)); Ellipse(pos=(x+w*0.62, y+h*0.54), size=(w*0.09, h*0.14)); return

class DesenhoCapa(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs); self.bind(pos=self._desenhar, size=self._desenhar)
    def _desenhar(self, *args):
        self.canvas.clear(); x,y=self.pos; w,h=self.size
        if w<=10 or h<=10: return
        lado=min(w/4.5, h*0.75); espaco=(w-(lado*4))/5.0; cy=y+(h-lado)/2.0
        with self.canvas:
            Color(0,0,0.7,1); Rectangle(pos=(x,y), size=(w,h)); bx=x+espaco
            Color(1,1,0,1); Ellipse(pos=(bx,cy), size=(lado,lado)); Color(0,0,0,1); Triangle(points=[bx+lado*0.5,cy+lado*0.5,bx+lado*1.05,cy+lado*0.75,bx+lado*1.05,cy+lado*0.25])
            cores=[(1,0,0,1),(1,0.6,0.8,1),(0,1,1,1),(1,0.6,0,1)]
            for i,cor in enumerate(cores):
                fx=bx+(lado+espaco)*(i+1); Color(*cor); Ellipse(pos=(fx,cy+lado*0.2), size=(lado*0.8,lado*0.6)); Rectangle(pos=(fx,cy), size=(lado*0.8,lado*0.3)); Color(1,1,1,1); Ellipse(pos=(fx+lado*0.15,cy+lado*0.5), size=(lado*0.18,lado*0.2)); Ellipse(pos=(fx+lado*0.45,cy+lado*0.5), size=(lado*0.18,lado*0.2))

class TelaInicial(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.musica = None
        layout = BoxLayout(orientation='vertical', padding=16, spacing=8)
        layout.add_widget(Label(text="CORANGE SOFTWARE", font_size='18sp', color=(0.4, 0.85, 1, 1), bold=True, size_hint_y=0.08))
        layout.add_widget(Label(text="PACMAN CLASSICO", font_size='34sp', color=(1, 0.85, 0.1, 1), bold=True, size_hint_y=0.12))
        self.lbl_recorde = Label(text="", font_size='16sp', color=(1, 1, 0.4, 1), bold=True, size_hint_y=0.08)
        layout.add_widget(self.lbl_recorde)
        layout.add_widget(DesenhoCapa(size_hint_y=0.28))
        self.lbl_pix = Label(text=f"PIX: {PIX_KEY}\nAjude a Corange Software!", font_size='14sp', color=(0.7, 1, 0.7, 1), bold=True, size_hint_y=0.12)
        layout.add_widget(self.lbl_pix)
        btn = Button(text="INICIAR JOGO", font_size='24sp', bold=True, background_color=(0.15, 0.75, 0.25, 1), size_hint_y=0.14)
        btn.bind(on_release=self.iniciar)
        layout.add_widget(btn)
        self.add_widget(layout)

    def on_pre_enter(self, *args):
        r = carregar_recorde()
        self.lbl_recorde.text = f"RECORDE: Fase {r.get('fase',1)} - {r.get('pontos',0)} pts"
        try:
            if os.path.exists("nes.mp3"):
                if self.musica: self.musica.stop()
                self.musica = SoundLoader.load("nes.mp3")
                if self.musica:
                    self.musica.loop = True
                    self.musica.volume = 0.7
                    self.musica.play()
        except Exception as e:
            print(f"Erro musica: {e}")

    def on_leave(self, *args):
        try:
            if self.musica: self.musica.stop()
        except: pass

    def iniciar(self, *args):
        criar_bip("bip.wav", 880, 0.15); tocar_bip("bip.wav")
        self.manager.current = "jogo"

class TelaJogo(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fase=1; self.pontos=0; self.vidas=3; self.mapa=[]; self.blocos=[]; self.player=[1,1]; self.direcao=(0,0); self.prox_direcao=(0,0); self.fantasmas=[]; self.assustado=0; self.pastilhas_restantes=0; self.evento=None
        layout=BoxLayout(orientation='vertical', spacing=4, padding=4)
        topo=BoxLayout(size_hint_y=0.08, spacing=8)
        self.lbl_pontos=Label(text="PONTOS: 0", bold=True); self.lbl_fase=Label(text="FASE: 1", bold=True); self.lbl_vidas=Label(text="VIDAS: 3", bold=True)
        topo.add_widget(self.lbl_pontos); topo.add_widget(self.lbl_fase); topo.add_widget(self.lbl_vidas); layout.add_widget(topo)
        self.grid=GridLayout(cols=21, rows=17, spacing=0, size_hint_y=0.78); layout.add_widget(self.grid)
        controles=GridLayout(cols=3, rows=3, size_hint_y=0.22, spacing=4)
        controles.add_widget(Widget()); b_cima=Button(text="▲", font_size='28sp'); b_cima.bind(on_release=lambda x:self.mudar_dir(-1,0)); controles.add_widget(b_cima); controles.add_widget(Widget())
        b_esq=Button(text="◀", font_size='28sp'); b_esq.bind(on_release=lambda x:self.mudar_dir(0,-1)); controles.add_widget(b_esq); b_baixo=Button(text="▼", font_size='28sp'); b_baixo.bind(on_release=lambda x:self.mudar_dir(1,0)); controles.add_widget(b_baixo); b_dir=Button(text="▶", font_size='28sp'); b_dir.bind(on_release=lambda x:self.mudar_dir(0,1)); controles.add_widget(b_dir)
        layout.add_widget(controles)
        btn_voltar=Button(text="VOLTAR", size_hint_y=0.06, background_color=(0.8,0.2,0.2,1)); btn_voltar.bind(on_release=self.voltar); layout.add_widget(btn_voltar)
        self.add_widget(layout); Window.bind(on_key_down=self.tecla)

    def tecla(self, win, key, *args):
        mapa_teclas={273:(-1,0),274:(1,0),276:(0,-1),275:(0,1)}
        if key in mapa_teclas: self.mudar_dir(*mapa_teclas[key])
        return True
    def mudar_dir(self, dl, dc): self.prox_direcao=(dl,dc)
    def voltar(self, *args):
        if self.evento: self.evento.cancel()
        self.manager.current="inicio"
    def on_pre_enter(self, *args): self.iniciar_fase(1,0,3)
    def iniciar_fase(self, fase, pontos, vidas):
        self.fase=fase; self.pontos=pontos; self.vidas=vidas
        self.mapa=copy.deepcopy(mapa_de_texto(MAPA_TXT))
        self.player=[1,1]; self.direcao=(0,0); self.prox_direcao=(0,0); self.assustado=0
        self.fantasmas=[{"pos":[8,10],"tipo":"vermelho","dir":(0,1)},{"pos":[8,9],"tipo":"rosa","dir":(0,-1)},{"pos":[9,10],"tipo":"ciano","dir":(0,1)},{"pos":[9,9],"tipo":"laranja","dir":(0,-1)},]
        self.pastilhas_restantes=sum(row.count(0) for row in self.mapa)
        self.construir_grid(); self.atualizar_labels()
        if self.evento: self.evento.cancel()
        self.evento=Clock.schedule_interval(self.update, 0.18)
    def construir_grid(self):
        self.grid.clear_widgets(); self.blocos=[]
        for l in range(17):
            linha_blocos=[]
            for c in range(21):
                b=Bloco(); b.l,b.c=l,c; self.grid.add_widget(b); linha_blocos.append(b)
            self.blocos.append(linha_blocos)
        self.desenhar_tudo()
    def pode_andar(self, l, c):
        if c<0 or c>=21 or l<0 or l>=17: return False
        return self.mapa[l][c]!=1
    def desenhar_tudo(self, skin=None):
        if skin is None: skin=FASES_SKINS[(self.fase-1)%len(FASES_SKINS)]
        for l in range(17):
            for c in range(21):
                b=self.blocos[l][c]
                if [l,c]==self.player: b.desenhar('player', skin=skin)
                elif any(f["pos"]==[l,c] for f in self.fantasmas):
                    f=next(x for x in self.fantasmas if x["pos"]==[l,c])
                    if self.assustado>0: b.desenhar('assustado', skin=skin)
                    else: b.desenhar('inimigo', skin=skin, inimigo_tipo=f["tipo"])
                else:
                    v=self.mapa[l][c]
                    if v==1: b.desenhar('fixo', skin=skin)
                    elif v==2: b.desenhar('poder', skin=skin)
                    elif v==0: b.desenhar('pastilha', skin=skin)
                    else: b.desenhar('chao', skin=skin)
    def atualizar_labels(self):
        self.lbl_pontos.text=f"PONTOS: {self.pontos}"
        self.lbl_fase.text=f"FASE: {self.fase} - {FASES_SKINS[(self.fase-1)%len(FASES_SKINS)]['nome']}"
        self.lbl_vidas.text=f"VIDAS: {self.vidas}"
    def update(self, dt):
        dl,dc=self.prox_direcao; nl,nc=self.player[0]+dl,self.player[1]+dc
        if nc==10 and (nl<0 or nl>=17): nl=16 if nl<0 else 0
        if self.pode_andar(nl,nc) or (nc==10 and nl in (0,16)): self.direcao=self.prox_direcao
        dl,dc=self.direcao
        if dl!=0 or dc!=0:
            nl,nc=self.player[0]+dl,self.player[1]+dc
            if nc==10 and (nl<0 or nl>=17): nl=16 if nl<0 else 0
            if self.pode_andar(nl,nc):
                self.player=[nl,nc]
                if self.mapa[nl][nc]==0: self.mapa[nl][nc]=3; self.pontos+=10; self.pastilhas_restantes-=1; tocar_bip("bip.wav")
                elif self.mapa[nl][nc]==2: self.mapa[nl][nc]=3; self.pontos+=50; self.assustado=25; tocar_bip("bip.wav")
        for f in self.fantasmas:
            opcoes=[]
            for dl,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                nl,nc=f["pos"][0]+dl,f["pos"][1]+dc
                if self.pode_andar(nl,nc): opcoes.append((dl,dc))
            if opcoes:
                if (-f["dir"][0],-f["dir"][1]) in opcoes and len(opcoes)>1: opcoes.remove((-f["dir"][0],-f["dir"][1]))
                f["dir"]=random.choice(opcoes); f["pos"][0]+=f["dir"][0]; f["pos"][1]+=f["dir"][1]
        if self.assustado>0: self.assustado-=1
        for f in self.fantasmas:
            if f["pos"]==self.player:
                if self.assustado>0: self.pontos+=200; f["pos"]=[8,10]
                else:
                    self.vidas-=1
                    if self.vidas<=0:
                        salvar_recorde(self.fase,self.pontos)
                        if self.evento: self.evento.cancel()
                        self.lbl_pontos.text=f"FIM! {self.pontos} pts"
                        Clock.schedule_once(lambda x:setattr(self.manager,'current','inicio'),1.5); return
                    else: self.player=[1,1]; self.direcao=(0,0); self.prox_direcao=(0,0)
        self.atualizar_labels(); self.desenhar_tudo()
        if self.pastilhas_restantes<=0:
            salvar_recorde(self.fase,self.pontos); self.iniciar_fase(self.fase+1,self.pontos,self.vidas)

class PacmanApp(App):
    def build(self):
        criar_bip("bip.wav", 880, 0.12)
        sm=ScreenManager(); sm.add_widget(TelaInicial(name="inicio")); sm.add_widget(TelaJogo(name="jogo")); return sm

if __name__ == "__main__":
    PacmanApp().run()
