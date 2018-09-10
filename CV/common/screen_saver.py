import os


class ScreenSaver:
    def __init__(self, save_path, capture_interval, compress_rate=1, screen_analyzer=None):
        """
        初始化一个屏幕截取对象
        :param save_path: 截图保存目录
        :param capture_interval: 截取时间间隔
        :param compress_rate: 截图的压缩比例
        :param screen_analyzer: 截图分析器
        """
        self.save_path = self.init_save_path(save_path)
        self.capture_interval = capture_interval
        self.compress_rate = compress_rate
        self.analyzer = screen_analyzer


    def init_save_path(self, save_path):
        if os.path.isfile(save_path):
            pass
        elif os.path.isdir(save_path):
            pass
        return save_path

    def init_input(self, save_path=None, compress_rate=None, capture_interval=None):
        """
        初始化参数，如果没有赋值，则默认返回该对象的初始值
        :param save_path:
        :param compress_rate:
        :param capture_interval:
        :return:
        """
        if not save_path:
            save_path = self.save_path
        if not capture_interval:
            capture_interval = self.capture_interval
        if not compress_rate:
            compress_rate = self.compress_rate
        return save_path, compress_rate, capture_interval

    def auto_capture(self, save_path=None, capture_interval=None, compress_rate=None):
        """
        自动截获屏幕截图
        :param save_path:
        :param capture_interval:
        :param compress_rate:
        :return:
        """
        save_path, compress_rate, capture_interval = self.init_input(save_path, compress_rate, capture_interval)

    def time_out_capture(self, time_span, save_path=None, compress_rate=None):
        """
        定时截获屏幕截图
        :param time_span:
        :param save_path:
        :param compress_rate:
        :return:
        """
        save_path, compress_rate, capture_interval = self.init_input(save_path, compress_rate)

    def capture(self, save_path=None, compress_rate=None):
        """
        立即截图
        :param save_path:
        :param compress_rate:
        :return:
        """
        save_path, compress_rate, capture_interval = self.init_input(save_path, compress_rate)

    def set_screen_analyzer(self, analyze_object):
        """
        设置截图之后的解析工具
        :param analyze_object:
        :return:
        """
        self.analyzer = analyze_object
