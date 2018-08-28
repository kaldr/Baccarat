from kivy.app import App
from kivy.core.text import LabelBase, DEFAULT_FONT
# from kivy.uix.button import ButtonBase
from kivy.uix.screenmanager import Screen
from os.path import dirname, join
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty, BooleanProperty, ListProperty
from kivy.config import Config
from kivy.resources import resource_add_path
resource_add_path('./assets')
Config.set("kivy", "keyboard_mode", 'system')
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '926')
Config.set('graphics', 'height', '600')
Config.set('kivy', 'window_icon', 'assets/icon.png')
# Config.setdefault('graphics', 'default_font', ['Roboto', 'PingFang.ttc'])

LabelBase.register(DEFAULT_FONT, 'PingFang.ttc')

from BaccaratPlayerScreen import BaccaratPlayerScreen


class BaccaratPlayerApp(App):
    title = '百家乐模拟'

    def build(self):
        return BaccaratPlayerScreen()

    def on_pause(self):
        return True

    def on_resume(self):
        pass

    def on_current_title(self, instance, value):
        self.root.ids.spnr.text = value

    def _update_clock(self, dt):
        self.time = time()

    def load_screen(self, index):
        if index in self.screens:
            return self.screens[index]
        screen = Builder.load_file(self.available_screens[index])
        self.screens[index] = screen
        return screen

    def update_sourcecode(self):
        if not self.show_sourcecode:
            self.root.ids.sourcecode.focus = False
            return
        self.root.ids.sourcecode.text = self.read_sourcecode()
        self.root.ids.sv.scroll_y = 1

    def read_sourcecode(self):
        fn = self.available_screens[self.index]
        with open(fn) as fd:
            return fd.read()

    def go_screen(self, idx):
        self.index = idx
        self.root.ids.sm.switch_to(self.load_screen(idx), direction='left')
        self.update_sourcecode()

    def go_next_screen(self):
        self.index = (self.index + 1) % len(self.available_screens)
        screen = self.load_screen(self.index)
        sm = self.root.ids.sm
        sm.switch_to(screen, direction='left')
        self.current_title = screen.name
        self.update_sourcecode()

    def go_previous_screen(self):
        self.index = (self.index - 1) % len(self.available_screens)
        screen = self.load_screen(self.index)
        sm = self.root.ids.sm
        sm.switch_to(screen, direction='right')
        self.current_title = screen.name
        self.update_sourcecode()


BaccaratPlayerApp().run()