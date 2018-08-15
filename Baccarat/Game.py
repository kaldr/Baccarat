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
            player.exporter.export_player()


def play(playTime):
    totals = [0, 0]
    totalWin = [0, 0]
    l = 1
    profit = 0
    for i in range(l):
        player1 = Player(
            '三次交叉与上一轮相反', money=100000, rule=2, rule_2_stake_reverse=True)
        player2 = Player(
            '三次交叉与上一轮相同', money=100000, rule=2, rule_2_stake_reverse=False)
        player3 = Player(
            '交叉先押闲', money=100000, rule=1, rule_1_stake_reverse=True)
        player4 = Player(
            '交叉先押庄', money=100000, rule=1, rule_1_stake_reverse=False)
        players = [
            # player1,
            player2
            # player3,
            # player4
        ]

        # player2=Player('随机',money=310000,)

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
            profit += differ
        G.export_player_history_for_a_game()
        # print(s)
    print('每个玩家盈利：')
    print(totals)

    print('本次盈利：%s' % profit)
    print("----------------------")
    return profit

    # print(totalWin)


playTime = 1
play_profit = 0
for i in range(playTime):
    play_profit += play(i)
print("%s次模拟玩，每次模拟玩6000-7000次押注共盈利%s" % (playTime, play_profit))
