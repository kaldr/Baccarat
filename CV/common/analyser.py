from .config_helper import ConfigHelper
from .screen_saver import ScreenSaver


class Analyser:
    screen_saver_config = ConfigHelper.generate_default_screen_saver_config()

    def __init__(self, screen_saver_config=None):
        if not screen_saver_config:
            screen_saver_config = self.screen_saver_config
        else:
            if ConfigHelper.check_screen_saver_config(**screen_saver_config):
                self.screen_saver_config = screen_saver_config
            else:

                screen_saver_config = self.screen_saver_config
        self.screen_saver = ScreenSaver(**screen_saver_config)
