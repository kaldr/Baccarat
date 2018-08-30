from .Rule import Rule


class AlwaysXian(Rule):
    def __init__(self, maxLevel=300, money=10000, initLevel=50, levelSpan=10):
        Rule.__init__(self, money=money)
        self.maxLevel = maxLevel
        maxLevelStep = (maxLevel) * levelSpan + initLevel
        self.levelSteps = range(initLevel, maxLevelStep, levelSpan)

    def getFirstStakeAndMoney(self):
        self.currentRank = 5
        return (2, self.levelSteps[self.currentRank])

    def setStakeAndMoneyForNext(self, result={}):
        stake = 2
        money = self.setMoney(result)
        return (stake, money)

    def setMoney(self, result):

        if result['win']:
            if self.currentRank > 0:
                self.currentRank -= 1
            elif self.currentRank == 0:
                self.currentRank = 5
        else:
            if result['winner_id'] != 3:
                self.currentRank += 1

        if self.currentRank >= self.maxLevel:
            self.currentRank = 0

        if self.currentRank < 0:
            self.currentRank = 5

        money = self.levelSteps[self.currentRank]
        return money
