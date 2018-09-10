from .Drop import Drop


# 100起打，100赢3次到50，50赢三次到100

# 最低档，净赢3次，还打最低档
# 最低档，净输3次，跟其他一样，升一档

class DropWithRound(Drop):
    round_types = [
        [
            [50, 100, 150, 200, 300, 400, 500, 600],
            [100, 200, 300, 400, 600, 800, 1000, 1200],
            [300, 600, 900, 1200, 1800, 2400, 3000, 3600],
            [1000, 2000, 3000, 4000, 6000, 8000, 10000, 12000],
            [3000, 6000, 9000, 12000, 18000, 24000, 30000, 36000]
        ]
    ]

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
                 lowest_level_win_count=True,
                 first_round=0,
                 round_type=0,
                 **kwargs):
        Drop.__init__(self,
                      randomStake=randomStake,
                      levelType=levelType,
                      maxLevel=maxLevel,
                      money=money,
                      initLevel=initLevel,
                      firstStake=firstStake,
                      reverseStake=reverseStake,
                      liftLevelLose=liftLevelLose,
                      lowLevelWin=lowLevelWin,
                      lowestLevelWin3TimeJumpToLevel=lowestLevelWin3TimeJumpToLevel,
                      stopWhenProfit=stopWhenProfit,
                      stopWhenProfitMoney=stopWhenProfitMoney,
                      stopOnLastLevel=stopOnLastLevel,
                      recursiveStake=recursiveStake,
                      **kwargs)
        self.maxLevel = maxLevel
        self.round_type = round_type
        self.rounds = self.round_types[self.round_type]
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
        self.currentLevelPureWin = 0
        self.lowest_level_win_count = lowest_level_win_count
        self.current_round = first_round
        self.levelSteps = self.rounds[self.current_round]
        if self.maxLevel == 0:
            self.maxLevel = len(self.levelSteps) - 1
        if stopWhenProfit and not stopWhenProfitMoney:
            self.stopWhenProfitMoney = 3000
            print('规则没有设置最大盈利停止点，默认设置为3000元')

    def getFirstStakeAndMoney(self):
        stake, money = Drop.getFirstStakeAndMoney(self)
        return stake, money

    def setStakeAndMoneyForNext(self, result=None):
        if not result:
            result = {}
        stake, money = Drop.setStakeAndMoneyForNext(self, result)
        return stake, money

    def setStake(self, result=None):
        if not result:
            result = {}
        return Drop.setStake(self, result)

    def lowestLevelMoney(self, result):
        # 50 赢3次到 100
        # 50 输3次到 100
        # 100 赢3次到50
        # 100 输3次
        pass

    def setMoneyWithLowestLevelSpecialJump(self, result):
        use_drop_func = False
        if self.currentRank == 0:
            if not self.lowest_level_win_count:
                # 最低档赢了不进行计数
                result['info'] = '最低档赢了，不进行计数'
            else:
                use_drop_func = True
        else:
            use_drop_func = True
        if use_drop_func:
            return Drop.setMoneyWithLowestLevelSpecialJump(self, result)

    def setMoneyWithoutLowestLevelSpecialJump(self, result):
        use_drop_func = False
        if self.currentRank == 0:
            if not self.lowest_level_win_count:
                # 最低档赢了不进行计数
                result['info'] = '最低档赢了，不进行计数'
            else:
                use_drop_func = True
        else:
            use_drop_func = True
        if use_drop_func:
            return Drop.setMoneyWithoutLowestLevelSpecialJump(self, result)

    def final_burst(self, result):
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
            self.current_round = 0
            self.set_round()
            result['info'] = '如果爆掉需要从头开始打'

    def set_round(self):
        self.levelSteps = self.rounds[self.current_round]
        self.maxLevel = len(self.levelSteps) - 1
        self.currentLevelPureWin = 0
        self.currentRank = 0

    def change_round(self, result):
        self.current_round += 1
        self.set_round()
        result['info'] = '上一轮爆掉，换下一轮'

    def set_money_and_level_for_burst(self, result):
        # 只有在最后一轮，才会判断最终游戏的爆掉
        if self.current_round == len(self.rounds) - 1:
            self.final_burst(result)
        else:
            self.change_round(result)

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
                self.setMoneyWithoutLowestLevelSpecialJump(result)
            # 上一次输
            else:
                # 输了，但是不为和
                if result['winner_id'] != 3:
                    self.currentLevelPureWin -= 1
                    # 如果爆掉，一定是最后哪一档已经连续输了3次的时候，爆掉了可以停止，可以重新开始打
                    if self.currentLevelPureWin == -self.liftLevelLose and self.currentRank == self.maxLevel:
                        self.set_money_and_level_for_burst(result)
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
