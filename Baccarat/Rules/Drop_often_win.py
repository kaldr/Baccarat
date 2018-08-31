from .Rule import Rule
from random import randrange

# 2018年8月31日保存，这个打法经常会出现一直赢到底的情况

# 100起打，100赢3次到50，50赢三次到100

# 最低档，净赢3次，还打最低档
# 最低档，净输3次，跟其他一样，升一档


class DropOftenWin(Rule):
    levels = [[
        50, 100, 150, 200, 250, 300, 400, 500, 600, 700, 800, 900, 1000, 1200, 1400, 1600, 1900, 2200, 2600, 3000, 3500, 4000, 4500, 5000, 5700, 6400, 7100, 8000, 9000, 10000, 11500, 13000, 14500,
        17000, 19000, 21000, 23000, 25500, 28000
    ], [
        50, 70, 100, 130, 150, 180, 200, 230, 250, 280, 300, 330, 350, 380, 400, 430, 450, 480, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800,
        1900, 2000, 2200, 2400, 2600, 2800, 3000, 3200, 3400, 3600, 3800, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500, 8000, 8500, 9000, 9500, 10000, 11000, 12000, 13000, 14000, 15000, 16000,
        17000, 18000, 19000, 20000, 21500, 23000, 24500, 26000, 27500, 29000, 31000, 33000, 35000, 37000, 39000, 41000, 44000, 47000, 50000
    ]]

    def __init__(self,
                 randomStake=False,
                 levelType=0,
                 maxLevel=0,
                 money=10000,
                 initLevel=1,
                 firstStake=1,
                 reverseStake=False,
                 liftLevelLose=3,
                 lowLevelWin=3,
                 lowestLevelWin3TimeJumpToLevel=0,
                 stopWhenProfit=True,
                 stopWhenProfitMoney=0,
                 stopOnLastLevel=False,
                 recursiveStake=False,
                 **kwargs):
        Rule.__init__(self, money=money)
        self.maxLevel = maxLevel
        self.lowestLevelWin3TimeJumpToLevel = lowestLevelWin3TimeJumpToLevel
        self.stopWhenProfit = stopWhenProfit
        self.stopWhenProfitMoney = stopWhenProfitMoney
        self.stopOnLastLevel = stopOnLastLevel
        self.reverseStake = reverseStake
        self.initLevel = initLevel
        self.randomStake = randomStake
        self.firstStake = firstStake
        self.recursiveStake = recursiveStake
        self.levelType = levelType
        self.lowLevelWin = lowLevelWin
        self.liftLevelLose = liftLevelLose
        self.levelSteps = self.levels[self.levelType]
        self.currentLevelPureWin = 0
        if stopWhenProfit and not stopWhenProfitMoney:
            self.stopWhenProfitMoney = 3000
            print('规则没有设置最大盈利停止点，默认设置为3000元')

    def getFirstStakeAndMoney(self):
        self.currentLevelPureWin = 0
        self.currentRank = self.initLevel
        stake = 1
        money = self.levelSteps[0]
        if self.firstStake:
            stake = self.firstStake
        if self.initLevel:
            money = self.levelSteps[self.initLevel]
        return (stake, money)

    def setStakeAndMoneyForNext(self, result={}):
        stake = self.setStake(result)
        money = self.setMoney(result)
        return (stake, money)

    def setStake(self, result={}):
        if self.randomStake:
            return randrange(1, 3)
        else:
            if self.recursiveStake:
                if result['stake_id'] == 1:
                    return 2
                elif result['stake_id'] == 2:
                    return 1
            elif not self.reverseStake:
                if result['winner_id'] == 3:
                    return result['stake_id']
                else:
                    return result['winner_id']

    def lowestLevelMoney(self, result):
        # 50 赢3次到 100
        # 50 输3次到 100
        # 100 赢3次到50
        # 100 输3次
        pass

    def setMoneyWithLowestLevelSpecialJump(self, result):
        # 如果最低档在连赢3次的情况下，要到特定的档上去
        if self.currentRank == 0 and self.currentLevelPureWin == self.liftLevelLose:
            # 默认 self.lowestLevelWin3TimeJumpToLevel 是0，因此默认是还打最低的档
            # 如果不是0，那么根据初始设置打对应的档
            self.currentRank = self.lowestLevelWin3TimeJumpToLevel
            if self.lowestLevelWin3TimeJumpToLevel == 0:
                self.currentLevelPureWin = 0
            result['info'] = '最低档在连赢%d次的情况下，要到特定的档上去' % self.lowLevelWin
        #如果不是最低档，是其他档赢了3次
        elif self.currentLevelPureWin == self.lowLevelWin:
            self.currentRank -= 1
            self.currentLevelPureWin = 0
            result['info'] = '当前档累计赢了%d次，降档' % self.lowLevelWin
        # 如果不是最低档，其他档赢了非3次，那么还是返回当前的档
        else:
            result['info'] = '当前档没有累计赢了%d次，不变' % self.lowLevelWin

    def setMoneyWithoutLowestLevelSpecialJump(self, result):
        # 如果最低档，那么净赢不管多少次都不变
        if self.currentRank == 0:
            result['info'] = '最低档赢了%d次，不变' % self.lowLevelWin
        #如果不是最低档，是其他档赢了3次
        elif self.currentLevelPureWin == self.lowLevelWin:
            self.currentRank -= 1
            self.currentLevelPureWin = 0
            result['info'] = '当前档累计赢了%d次，降档' % self.lowLevelWin
        # 如果不是最低档，其他档赢了非3次，那么还是返回当前的档
        else:
            result['info'] = '当前档没有累计赢了%d次，不变' % self.lowLevelWin

    def setMoney(self, result={}):
        # 如果达到了已经要的利润，可能要停止
        if self.stopWhenProfit and result['profit'] >= self.stopWhenProfitMoney:
            result['stop'] = 1
            result['reach_profit'] += 1
            result['info'] = '达到了已经要的利润，停止'
            self.currentRank = self.initLevel
            return self.levelSteps[self.currentRank]
        # 如果没有达到需要停止的利润
        else:
            # 上一次赢
            if result['win']:
                self.currentLevelPureWin += 1
                self.setMoneyWithoutLowestLevelSpecialJump(result)
            # 上一次输
            else:
                # 输了，但是不为和
                if result['winner_id'] != 3:
                    self.currentLevelPureWin -= 1
                    # 如果爆掉，一定是最后哪一档已经连续输了3次的时候，爆掉了可以停止，可以重新开始打
                    if self.currentLevelPureWin == -self.liftLevelLose and self.currentRank == len(self.levelSteps) - 1:
                        result['buster'] += 1
                        result['is_buster'] = True
                        self.currentLevelPureWin = 0
                        # 如果爆掉需要停止
                        if self.stopOnLastLevel:
                            result['stop'] = 1
                            result['info'] = '爆掉需要停止'
                        # 如果爆掉需要从头开始打
                        else:
                            self.currentRank = self.initLevel
                            result['info'] = '如果爆掉需要从头开始打'
                    # 如果没有爆掉
                    else:
                        # 如果当前档累计输3次，打下一档
                        if self.currentLevelPureWin == -self.liftLevelLose:
                            self.currentLevelPureWin = 0
                            self.currentRank += 1
                            result['info'] = '当前档累计输%d次，打下一档' % self.liftLevelLose
                        else:
                            result['info'] = '当前档没有累计输%d次，不变' % self.lowLevelWin
                # 输了，结果是和，还跟上一次打的一样
                else:
                    result['info'] = '和不变'
            return self.levelSteps[self.currentRank]
