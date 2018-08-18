import random
from .Rule import Rule


class WinTwiceAndReturn(Rule):
    name='double'
    levels = [[
        300, 300, 300, 300, 400, 500, 700, 1000, 1300, 1800, 2500, 3500, 4800,
        6500, 8800, 12000, 16000, 22000, 30000, 40000, 55000,75000,100000,137000,170000,230000,310000,450000
    ]]

    def __init__(self,
                 money=10000,
                 levelType=0,
                 loseAndStop=True,
                 stakeFollowPrevious=True,
                 randomStake=False,
                 maxLevel=0):
        Rule.__init__(
            self,
            money=money,
            loseAndStop=loseAndStop,
            stakeFollowPrevious=stakeFollowPrevious,
            randomStake=randomStake)

        self.concurrentWin = 0
        self.concurrentLose = 0
        self.levelSteps = self.levels[levelType]
        if not maxLevel:
            self.maxLevel=len(self.levelSteps)
        else:
            self.maxLevel=maxLevel
    def getFirstStakeAndMoney(self):
        self.currentRank = 0
        return (1, self.levelSteps[self.currentRank])

    def setStakeAndMoneyForNext(self, result={}):
        stake = self.setStake(result)
        money = self.setMoney(result)
        return (stake, money)

    def setStake(self, result):
        # 赢家不为和，跟着押
        if result['winner_id'] != 3:
            return result['winner_id']
        # 和赢，跟上一次押一样的
        else:
            return result['stake_id']

    def setMoney(self, result):
        factor = 1
        # 如何和赢，和上次押注一样，当做没有发生过
        if result['winner_id'] == 3:
            result['info'] = '和，当做没发生过'
            return result['stake_money']
        else:
            # 赢了
            if result['win']:
                self.win_or_lose += 1
                self.concurrentWin += 1
                self.concurrentLose = 0
                # 赢了2次，重新打
                if self.concurrentWin == 2:
                    self.win_or_lose = 0
                    self.currentRank = 0
                    self.concurrentWin = 0
                    result['info'] = '上次连赢2次，本次回到第一级'
                elif self.concurrentWin == 1:
                    factor = 2
                    result['info'] = '上次赢，本次翻倍'
                else:
                    result['info'] = '这一条不应该出现'

            # 输了
            else:
                self.concurrentLose += 1
                self.win_or_lose -= 1

                # 输了打下一级
                self.currentRank += 1
                self.concurrentWin = 0
                result['info'] = '上次输了，本次到下一档'
                if self.currentRank >= self.maxLevel:
                    self.currentRank = 0
                    result['buster']+=1
                    result['info'] = '爆掉，重新打'
            # if self.win_or_lose < -20:
            #     self.win_or_lose = 0
            #     self.currentRank = 0
            #     result['info'] = '净输太多，重新打'
            return factor * self.levelSteps[self.currentRank]
