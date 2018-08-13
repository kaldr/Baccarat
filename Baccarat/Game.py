from .Baccarat import Baccarat
from .Round import Round
from .Player import Player
import functools
print = functools.partial(print, flush=True)


class Game:
    roundLimit = 100

    def __init__(self, players=[]):
        self.players = players
        self.start()

    def start(self):
        for j in range(self.roundLimit):
            baccarat = Baccarat()
            for i in range(baccarat.rounds):
                round = Round(baccarat, self.players)

    def export_player_history_for_a_game(self, idx=0, folder=False):
        for player in self.players:
            win = False
            if player.current_money - player.money > 0:
                win = True
                winT = "赢"
            else:
                win = False
                winT = "输"
            player.exportToExcel(filename='玩家%s_%s_%s' %
                                 (player.name, (idx), winT), folder=False)


totals = [0, 0]
totalWin = [0, 0]
l = 1
for i in range(l):
    players = []
    player1 = Player('三重交叉', money=310000, rule=2)
    # player2=Player('随机',money=310000,)
    players.append(player1)
    # players.append(player2)
    G = Game(players)

    s = "%d\t" % (i + 1)
    j = 0
    differ = 0
    for player in players:
        differ = player.current_money - player.money

        result = 0
        if differ > 0:
            result = 1

        if j % 2 == 0:
            totals[0] += differ
            if differ > 0:
                totalWin[0] += 1
        else:
            totals[1] += differ
            if differ > 0:
                totalWin[1] += 1
        s += '%s\t%d\t%s\t' % (player.name, differ, result)
        j += 1

    G.export_player_history_for_a_game(
        "%d_%d" % (i, differ), folder="%d" % (i + 1))
    # print(s)
print(totals)
print(totalWin)
