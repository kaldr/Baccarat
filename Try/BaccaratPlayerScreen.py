from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty, StringProperty, ObjectProperty, BooleanProperty, ListProperty, OptionProperty
from kivy.uix.textinput import TextInput


class RoundTextInput(TextInput):
    input_type = OptionProperty('text')


class RoundNumberInput(RoundTextInput):
    input_type = OptionProperty('number')
    input_filter = ObjectProperty('int')

    def search(self, ob, text, id):
        print(text)
        print(ob)
        print(id)


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

    def run_simulation(self):
        print(self.status)
        if self.status == 'setting':
            self.status = 'running'
            self.ids.panel.remove_widget(self.selector)
            self.ids.panel.add_widget(self.progressing)
        else:
            self.status = 'setting'
            self.ids.panel.add_widget(self.selector, index=0)
            self.ids.panel.remove_widget(self.progressing)

    def selectPlayer(self, player):
        if player == '滴水式' and self.currentPlayer != '滴水式':
            self.currentPlayer = '滴水式'
            self.ids.selector.remove_widget(self.fifteen_n1)
            self.ids.selector.remove_widget(self.fifteen_n2)
        elif player == '递进式' and self.currentPlayer != '递进式':
            self.currentPlayer = '递进式'
            self.ids.selector.add_widget(self.fifteen_n1)
            self.ids.selector.add_widget(self.fifteen_n2)

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