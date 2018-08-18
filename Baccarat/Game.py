from .Baccarat import Baccarat
from .Round import Round
from .Player import Player
import functools
print = functools.partial(print, flush=True)
from .Rules.WinTwiceAndReturn import WinTwiceAndReturn
ruleWinTwiceAndReturn = WinTwiceAndReturn(maxLevel=0)


class Game:
    roundLimit = 1000  # 70000次押注为一个excel
    roundLimit = 100  # 7000次押注为一个excel

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
    buster = 0
    stake_total = 0
    for i in range(l):
        player1 = Player(
            '三次交叉与上一轮相反', money=100000, rule=2, rule_2_stake_reverse=True)
        player2 = Player(
            '三次交叉与上一轮相同', money=100000, rule=2, rule_2_stake_reverse=False)
        player3 = Player(
            '交叉先押闲', money=100000, rule=1, rule_1_stake_reverse=True)
        player4 = Player(
            '交叉先押庄', money=100000, rule=1, rule_1_stake_reverse=False)
        player5 = Player(
            '150起三次交叉', money=100000, rule=3, rule_1_stake_reverse=False)
        player6 = Player(
            '赢二次回头', money=10000, rule=4, ruleObject=ruleWinTwiceAndReturn)
        players = [
            # player1,
            # player2,
            # player3,
            # player4,
            # player5,
            player6
        ]

        # player2=Player('随机',money=310000,)

        # players.append(player2)
        G = Game(players)

        s = "%d\t" % (i + 1)
        j = 0
        differ = 0
        for player in players:
            differ = player.current_money - player.money
            stake_total += player.stake_total
            buster += player.buster
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
    return (profit, stake_total, buster)

    # print(totalWin)


play_win = 0
play_lose = 0
playTime = 20
play_profit = 0
play_stake_cost = 0
play_buster = 0
for i in range(playTime):
    (current, stake_total, buster) = play(i)
    play_profit += current
    play_stake_cost += stake_total
    play_buster += buster
    if current > 0:
        play_win += 1
    else:
        play_lose += 1
    print('第%d次' % (i + 1))
    print('总盈利:%s，总押注：%s，总爆掉：%s' % (play_profit, play_stake_cost, play_buster))
print(
    "%s次模拟玩，每次模拟玩约%d次押注共盈利%s，共押注%d，共爆掉%d，赢%d次，输%d次，赢输比%.1f%%" %
    (playTime, Game.roundLimit * 70, play_profit, play_stake_cost, play_buster,
     play_win, play_lose, play_win / (play_lose + 0.001) * 100.0))
