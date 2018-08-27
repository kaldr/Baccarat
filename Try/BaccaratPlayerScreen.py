from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty, StringProperty, BooleanProperty, ListProperty


class BaccaratPlayerScreen(Screen):
    fullscreen = BooleanProperty(True)
    init_levels = ('50', '100', '150', '200')

    def selectPlayer(self, player):
        if player == '滴水':
            pass
        else:
            pass

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