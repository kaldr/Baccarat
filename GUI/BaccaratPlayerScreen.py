from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty, StringProperty, ObjectProperty, BooleanProperty, ListProperty, OptionProperty
from kivy.uix.textinput import TextInput
from Baccarat.Game import Game, ruleFifteen30000, ruleDropThree


class RoundTextInput(TextInput):
    input_type = OptionProperty('text')
    name_id = StringProperty('')

    def set_params(self, ob, text, id):
        print(text)
        print(ob)
        print(id)
        BaccaratPlayerScreen.params[id] = text
        print(BaccaratPlayerScreen.params)


class RoundNumberInput(RoundTextInput):
    id = ObjectProperty(None)
    input_type = OptionProperty('number')
    input_filter = ObjectProperty('int')


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
        'output_path': '/Users/kaldr/Projects/Baccarat/Export/',
        'lowest_level_change_level': '150',
        'lowest_level_change_win_time': '2',
        'stay_time': '15',
        'profit_line': '3000',
        'change_level_win_or_lose_time': '3',
        'excel_round_count': '100',
        'excel_count': '40',
        'init_level': '请选择起打档',
        'init_levels': (),
        'type': ('滴水式', '递进式'),
    }

    def __init__(self, **kwargs):
        super(BaccaratPlayerScreen, self).__init__(**kwargs)

        self.fifteen_n1 = self.ids.fifteen_n1
        self.fifteen_n2 = self.ids.fifteen_n2
        self.selector = self.ids.selector
        self.submit_button = self.ids.run
        self.progressing = self.ids.progressing
        self.ids.selector.remove_widget(self.fifteen_n1)
        self.ids.selector.remove_widget(self.fifteen_n2)
        self.currentPlayer = '滴水式'
        self.selectPlayer('滴水式')
        self.ids.panel.remove_widget(self.progressing)

    def build_simulation_screen(self):
        if self.status == 'setting':
            self.status = 'running'
            self.ids.panel.remove_widget(self.selector)
            self.ids.panel.add_widget(self.progressing)
        else:
            self.status = 'setting'
            self.ids.panel.add_widget(self.selector, index=0)
            self.ids.panel.remove_widget(self.progressing)

    def run_game(self, params):
        pass

    def build_params(self):
        print(self.params)

    def run_simulation(self):
        self.build_params()
        self.build_simulation_screen()

    def selectPlayer(self, player):
        if player == '滴水式' and self.currentPlayer != '滴水式':
            self.currentPlayer = '滴水式'
            self.ids.selector.remove_widget(self.fifteen_n1)
            self.ids.selector.remove_widget(self.fifteen_n2)

        elif player == '递进式' and self.currentPlayer != '递进式':
            self.currentPlayer = '递进式'
            self.ids.selector.add_widget(self.fifteen_n1)
            self.ids.selector.add_widget(self.fifteen_n2)
        self.setParamsLevels()

    def setParamsLevels(self):
        levels = []
        if self.currentPlayer == '递进式':
            levels = ruleFifteen30000.levels[0]
        elif self.currentPlayer == '滴水式':
            levels = ruleDropThree.levels[0]
        self.params['init_levels'] = (str(levels[0]), str(levels[1]), str(levels[2]), str(levels[3]), str(levels[4]))
        self.params['init_level'] = str(levels[0])
        print(self.ids.init_level)
        self.ids.init_level.text = self.params['init_level']
        self.ids.init_level.values = self.params['init_levels']
        print(self.params)

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