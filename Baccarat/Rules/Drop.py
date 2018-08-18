from .Rule import Rule


class Drop(Rule):
    def __init__(self,
                 randomStake=False,
                 levelType=0,
                 maxLevel=0,
                 money=10000,
                 initLevel=0,
                 firstStake=1,
                 reverseStake=False,
                 liftLevelLose=3,
                 lowLevelWin=3,
                 lowestLevelWin3TimeJumpToLevel=0,
                 stopWhenProfit=False,
                 stopWhenProfitMoney=0,
                 stopOnLastLevel=False):
        Rule.__init__(self, money=money)
        self.maxLevel = maxLevel
        self.reverseStake = reverseStake
        self.initLevel = initLevel
        self.randomStake = randomStake
        self.firstStake = firstStake
        self.levelType = levelType
        self.lowLevelWin = lowLevelWin
        self.liftLevelLose = liftLevelLose
        self.levelSteps = self.levels[self.levelType]

    def getFirstStakeAndMoney(self):
        stake = 1
        money = 50
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
        if not self.reverseStake:
            if result['winner_id'] == 3:
                return result['stake_id']
            else:
                return result['winner_id']

    def setMoney(self, result={}):

        if result['win']:
            pass
        else:
            if result['winner_id'] != 3:
                pass
