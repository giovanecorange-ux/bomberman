from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class Menu(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=20, **kwargs)
        self.add_widget(Label(text="Bomberman Corange", font_size='32sp', color=(1,0.8,0,1), bold=True))
        self.add_widget(Label(text="☺ ● ♥ ♦ ☠", font_size='40sp'))
        b = Button(text="▶ INICIAR JOGO", font_size='28sp', background_color=(1,0.8,0,1), bold=True)
        b.bind(on_press=lambda x: print("CLICOU"))
        self.add_widget(b)
        self.add_widget(Label(text="Se apareceu isso, o app abriu!", font_size='16sp', color=(0.3,1,0.4,1)))

class MainApp(App):
    def build(self):
        return Menu()

MainApp().run()
