from kivy.app import App
from kivy.uix.button import Button


class BaccaratPlayer(App):
    def build(self):
        return Button(text="hello")


BaccaratPlayer().run()