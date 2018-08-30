from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty, StringProperty, ObjectProperty, BooleanProperty, ListProperty, OptionProperty
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from Baccarat.Game import Game, ruleFifteen30000, ruleDropThree, Play
from kivy.uix.spinner import Spinner
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import *
from kivy.app import App
from kivy.uix.progressbar import ProgressBar
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from functools import partial

from kivy.lang import Builder


class RoundTextInput(TextInput):
    input_type = OptionProperty('text')
    name_id = StringProperty('')
    link_ob = ObjectProperty(None)

    def set_params(self, ob, text, id):
        app = App.get_running_app()

        BaccaratPlayerScreen.params[id] = text
        print(BaccaratPlayerScreen.params)

        if app:
            if id in ['excel_round_count', 'excel_count']:
                try:
                    BaccaratPlayerScreen.params['texts']['bottom'] = "共模拟%d万次，导出%s个Excel，每个Excel押注%s~%s次。" % (
                        int(BaccaratPlayerScreen.params['excel_count']) * int(BaccaratPlayerScreen.params['excel_round_count']) * 70 / 10000,
                        BaccaratPlayerScreen.params['excel_count'], int(BaccaratPlayerScreen.params['excel_round_count']) * 65,
                        int(BaccaratPlayerScreen.params['excel_round_count']) * 80)
                except Exception as e:
                    BaccaratPlayerScreen.params['texts']['bottom'] = ''
                self.link_ob.ids.bottom_label.text = BaccaratPlayerScreen.params['texts']['bottom']
            if id in ['change_level_win_or_lose_time']:
                BaccaratPlayerScreen.params['texts']['jump_method'] = '[递进式]输%s次跳档的计算方法' % text
                self.link_ob.ids.jump_method_label.text = BaccaratPlayerScreen.params['texts']['jump_method']
                BaccaratPlayerScreen.params['texts']['lowest_level_change_win_time'] = "[递进式]最低档赢%s次后跳到第档" % text
                self.link_ob.ids.lowest_level_change_win_time_label.text = BaccaratPlayerScreen.params['texts']['lowest_level_change_win_time']

                BaccaratPlayerScreen.params['texts']['lowest_level_change_level'] = "[递进式]最低档赢%s次后跳到第x档" % text
                self.link_ob.ids.lowest_level_change_level_label.text = BaccaratPlayerScreen.params['texts']['lowest_level_change_level']

                BaccaratPlayerScreen.params['texts']['lowest_level_win_n_and_jump_to_level'] = '最低档赢%s次后打第x档' % text
                self.link_ob.ids.lowest_level_win_n_and_jump_to_level_label.text = BaccaratPlayerScreen.params['texts'][
                    'lowest_level_win_n_and_jump_to_level']
                BaccaratPlayerScreen.params['values']['jump_method'] = ("净输%s次" % text, "累计输%s次" % text)
                self.link_ob.ids.jump_method.values = BaccaratPlayerScreen.params['values']['jump_method']
                if BaccaratPlayerScreen.params['jump_method'].startswith('净'):
                    BaccaratPlayerScreen.params['jump_method'] = "净输%s次" % text
                else:
                    BaccaratPlayerScreen.params['jump_method'] = "累计输%s次" % text
                self.link_ob.ids.jump_method.text = BaccaratPlayerScreen.params['jump_method']
            app.params = BaccaratPlayerScreen.params


class RoundNumberInput(RoundTextInput):
    id = ObjectProperty(None)
    input_type = OptionProperty('number')
    input_filter = ObjectProperty('int')


class RoundSpinner(Spinner):
    def set_params(self, ob, text, id):
        BaccaratPlayerScreen.params[id] = text
        print(BaccaratPlayerScreen.params)


class RunningScreen(Screen):
    def setprogress(self, i, count, *largs):
        a = i + 1
        rate = a / float(count) * 100.0
        self.pb.value = rate
        if rate == 100:
            self.pbr.text = "%d%%" % rate
            self.pbl.text = '导出完成，返回设置页面'

            Clock.schedule_once(partial(self.go_to_setting_screen), 1)
        else:
            self.pbr.text = "%.2f%%" % rate

    def init_progress_bar(self):
        self.progressing = AnchorLayout(anchor_y='bottom', anchor_x='center')
        playoutContainer = BoxLayout(orientation="vertical")
        self.pb = ProgressBar(max=100, value=0)
        self.pbl = Label(text='正在导出excel', font_size='16dp', color=(1, 1, 1, 1), size_hint_y=None, height='30dp')
        self.pbr = Label(text='0%', font_size='32dp', color=(1, 1, 1, 1), size_hint_y=None, height='50dp')
        pblayout = BoxLayout(height='24dp', size_hint_y=None, padding=(150, 0, 150, 0))
        pblayout.add_widget(self.pb)
        playoutContainer.add_widget(self.pbr)
        playoutContainer.add_widget(pblayout)
        playoutContainer.add_widget(self.pbl)
        self.progressing.add_widget(playoutContainer)
        self.ids.running_screen.add_widget(self.progressing)

    def go_to_setting_screen(self, *largs):
        self.manager.current = 'setting'

    def __init__(self, **kwargs):
        super(RunningScreen, self).__init__(**kwargs)
        self.init_progress_bar()

    def export_excel(self, game, index, count, *largs):
        if index >= count:
            return
        else:
            game.play_baccarat(index, )
            index += 1
            Clock.schedule_once(partial(self.export_excel, game, index, count))

    def on_enter(self):
        self.pbr.text = '0%'
        self.pb.value = 0
        checkResult = App.get_running_app().params
        game = Play(
            params=checkResult["params"],
            playTime=checkResult['params']['playTime'],
            roundLimit=checkResult['params']['roundLimit'],
            ob=self,
            callback=self.setprogress)
        Clock.schedule_once(partial(self.export_excel, game, 0, checkResult['params']['playTime']), 1)


class BaccaratPlayerScreen(Screen):
    fullscreen = BooleanProperty(True)
    stake_method = '出庄打庄，出闲打闲'
    first_stake = '庄'
    fifteen = False
    fifteen_n1 = False
    fifteen_n2 = False
    selector = False
    submit_button = False
    currentPlayer = '滴水式'
    status = 'setting'
    params = {
        'texts': {
            "bottom": '',
            'jump_method': '输n次跳档的计算方法',
            'lowest_level_change_win_time': "最低档赢n次后跳到第档",
            'lowest_level_change_level': "最低档赢n次后跳到第x档",
            'lowest_level_win_n_and_jump_to_level': '最低档赢n次后打第x档'
        },
        'values': {
            'jump_method': ('净输n次', '累计输n次')
        },
        'jump_method': '净输n次',
        'output_path': '/Users/kaldr/Projects/Baccarat/Export/bbc/',
        'lowest_level_change_level': '150',
        'lowest_level_change_win_time': '2',
        'stay_time': '15',
        'profit_line': '3000',
        'change_level_win_or_lose_time': '3',
        'excel_round_count': '5',
        'excel_count': '5',
        'init_level': '50',
        "first_stake": '庄',
        'stake_method': '出庄打庄，出闲打闲',
        'init_levels': ('50', '100', '150', '200', '250'),
        'max_level': "8000",
        'max_levels': ('8000', '10000'),
        'type': ('滴水式', '递进式'),
        'last_level': '重新开始打',
        "lowest_level_win_n_and_jump_to_level": '100',
        'lowest_level_win_n_and_jump_to_levels': ('100', '150', '200', '250', '300')
    }

    def __init__(self, **kwargs):
        super(BaccaratPlayerScreen, self).__init__(**kwargs)
        self.init_panel()
        self.currentPlayer = '滴水式'
        self.selectPlayer('滴水式')
        self.build_init_params()

    def init_panel(self):
        self.build_bg_instructions()
        self.fifteen_n1 = self.ids.fifteen_n1
        self.fifteen_n2 = self.ids.fifteen_n2
        self.selector = self.ids.selector
        self.submit_button = self.ids.run
        # self.ids.selector.remove_widget(self.fifteen_n1)
        # self.ids.selector.remove_widget(self.fifteen_n2)
        # self.init_progress_bar()

    def build_init_params(self):
        #
        self.params['texts']['bottom'] = "共模拟%d万次，导出%s个Excel，每个Excel押注%s~%s次。" % (
            int(self.params['excel_count']) * int(self.params['excel_round_count']) * 70 / 10000, self.params['excel_count'],
            int(self.params['excel_round_count']) * 65, int(self.params['excel_round_count']) * 80)
        self.ids.bottom_label.text = self.params['texts']['bottom']
        #
        text = self.params['change_level_win_or_lose_time']
        #
        self.params['texts']['jump_method'] = '[递进式]输%s次跳档的计算方法' % text
        self.ids.jump_method_label.text = self.params['texts']['jump_method']
        #
        self.params['texts']['lowest_level_change_win_time'] = "最低档赢%s次后跳到x" % text
        self.ids.lowest_level_change_win_time_label.text = self.params['texts']['lowest_level_change_win_time']
        #
        self.params['texts']['lowest_level_change_level'] = "最低档赢%s次后跳到x" % text
        self.ids.lowest_level_change_level_label.text = self.params['texts']['lowest_level_change_level']
        #
        self.params['texts']['lowest_level_win_n_and_jump_to_level'] = '[递进式]最低档赢%s次后打x' % text
        self.ids.lowest_level_win_n_and_jump_to_level_label.text = self.params['texts']['lowest_level_win_n_and_jump_to_level']
        #
        self.params['values']['jump_method'] = ("净输%s次" % text, "累计输%s次" % text)
        if self.params['jump_method'].startswith('净'):
            self.params['jump_method'] = "净输%s次" % text
        else:
            self.params['jump_method'] = "累计输%s次" % text
        self.ids.jump_method.values = self.params['values']['jump_method']
        self.ids.jump_method.text = self.params['jump_method']

    def go_to_running_screen(self, *largs):
        self.manager.current = 'running'

    def build_bg_instructions(self):
        size = (1003, 650)
        instruction_setting_drop = InstructionGroup(name='setting_drop')
        instruction_setting_drop.add(Color(1, 1, 1, 1))
        instruction_setting_drop.add(Rectangle(size=size, source='bg.jpg'))
        instruction_setting_fifteen = InstructionGroup(name='setting_fifteen')
        instruction_setting_fifteen.add(Color(1, 1, 1, 1))
        instruction_setting_fifteen.add(Rectangle(size=size, source='bg1.jpg'))
        instruction_setting_running = InstructionGroup(name="running")
        instruction_setting_running.add(Color(1, 1, 1, 1))
        instruction_setting_running.add(Rectangle(size=size, source='bg2.jpg'))
        self.bg_instructions = {
            "setting_drop": instruction_setting_drop,
            "setting_fifteen": instruction_setting_fifteen,
            "running": instruction_setting_running
        }

    def build_bg(self, status_old):
        if self.status == 'setting':
            if self.currentPlayer == '滴水式':
                status_new = 'setting_drop'
            elif self.currentPlayer == '递进式':
                status_new = 'setting_fifteen'
        elif self.status == 'running':
            status_new = 'running'
        old_bg_instruction = self.bg_instructions[status_old]
        new_bg_instruction = self.bg_instructions[status_new]
        self.canvas.before.remove_group(status_old)
        self.canvas.before.add(new_bg_instruction)

    def run_game(self, params):
        pass

    def build_params(self):

        unzeroParams = [
            'lowest_level_change_level', 'lowest_level_change_win_time', 'stay_time', 'profit_line', 'change_level_win_or_lose_time',
            'excel_round_count', 'excel_count', 'init_level', 'max_level', 'output_path'
        ]
        flag = True
        for param in unzeroParams:
            if not self.params[param]:
                flag = False
            if self.params[param] in [0, '0', '', None]:
                flag = False
        params = {}
        if flag:
            params['output_path'] = self.params['output_path']
            if self.params['stake_method'] == '出庄打闲，出闲打庄':
                params['reverseStake'] = True
            elif self.params['stake_method'] == '随机打':
                params['randomStake'] = True
            elif self.params['stake_method'] == '庄闲循环':
                params['recursiveStake'] = True
            params['stay_times'] = int(self.params['stay_time'])
            params['initLevel'] = int(self.params['init_level'])
            params['firstStake'] = 1
            if self.params['first_stake'] == '闲':
                params['firstStake'] = 2
            params['playTime'] = int(self.params['excel_count'])
            params['roundLimit'] = int(self.params['excel_round_count'])
        return {"pass": flag, "error_info": '有信息没有输入完整，输入框的内容不能为空，也不能为0', 'params': params}

    def run_simulation(self):
        checkResult = self.build_params()
        if checkResult['pass'] == True:
            # self.manager['params'] = checkResult
            app = App.get_running_app()
            app.params = checkResult
            self.go_to_running_screen()
        else:
            self.ids.bottom_label.text = checkResult['error_info']

    def selectPlayer(self, player):
        current_bg_status = 'setting_'
        if player == '滴水式':
            if self.currentPlayer != '滴水式':
                self.currentPlayer = '滴水式'
                # self.ids.selector.remove_widget(self.fifteen_n1)
                # self.ids.selector.remove_widget(self.fifteen_n2)
                current_bg_status += 'fifteen'
            else:
                current_bg_status += 'drop'
        elif player == '递进式':
            if self.currentPlayer != '递进式':
                current_bg_status += 'drop'
                self.currentPlayer = '递进式'
                # self.ids.selector.add_widget(self.fifteen_n1)
                # self.ids.selector.add_widget(self.fifteen_n2)
            else:
                current_bg_status += 'fifteen'
        self.setParamsLevels()
        self.build_bg(current_bg_status)

    def setParamsLevels(self):
        levels = []
        if self.currentPlayer == '递进式':
            from_num = 25
            levels = ruleFifteen30000.levels[0]
        elif self.currentPlayer == '滴水式':
            from_num = 33
            levels = ruleDropThree.levels[0]
        self.params['init_levels'] = [str(level) for level in levels[0:5]]
        self.params['init_level'] = str(levels[0])
        self.params['lowest_level_win_n_and_jump_to_level'] = str(levels[1])
        self.params['lowest_level_win_n_and_jump_to_levels'] = [str(level) for level in levels[1:6]]
        self.params['max_levels'] = [str(level) for level in levels[from_num:]]
        self.params['max_level'] = str(levels[-1])
        self.ids.init_level.text = self.params['init_level']
        self.ids.init_level.values = self.params['init_levels']
        self.ids.max_level.text = self.params['max_level']
        self.ids.max_level.values = self.params['max_levels']
        self.ids.lowest_level_win_n_and_jump_to_level.text = self.params['lowest_level_win_n_and_jump_to_level']
        self.ids.lowest_level_win_n_and_jump_to_level.values = self.params['lowest_level_win_n_and_jump_to_levels']

    def selectStakeType(self, stakeType):
        pass

    def selectInitLevel(self, levelType):
        pass

    def selectMaxLevel(self, maxLevel):
        pass

    def selectFirstStake(self, firstStake):
        pass

    def selectLiftLevelLose(self, level):
        pass