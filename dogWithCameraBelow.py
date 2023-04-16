from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.videoplayer import VideoPlayer

class MainApp(MDApp):
    title = "DOG"
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"

        player = VideoPlayer(source = "funny_dog.mp4")

        player.state = "play"

        player.options = {'eos': 'loop'}

        player.allow_stretch = True

        return player

MainApp().run()