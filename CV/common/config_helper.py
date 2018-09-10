class ConfigHelper:
    @staticmethod
    def generate_default_screen_saver_config():
        return {
            "save_path": "",
            "capture_interval": 5,
            "compress_rate": 1
        }

    @staticmethod
    def check_screen_saver_config(save_path, capture_interval, compress_rate=1, screen_analyzer=None):
        """
        检查
        :param save_path:
        :param capture_interval:
        :param compress_rate:
        :param screen_analyzer:
        :return: boolean
        """
        return True
