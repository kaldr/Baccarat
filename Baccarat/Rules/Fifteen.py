from .Rule import Rule


class Fifteen(Rule):
    levels = [[100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600, 2800, 3000, 3400, 3800, 4200, 4600, 5000, 5400, 5800, 6200, 6600, 7200, 7600, 8000]]

    def __init__(
            self,
            initLevel=0,
            stay_times=15,
            randomStake=False,
            reverseStake=False,
            recursiveStake=False,
            levelType=0,
            money=10000,
            stopWhenProfit=True,
            stopProfit=8000,
            firstStake=1,
            lastLevelStop=True,
            pureChange=False,  # 净输赢达到次数才变化，默认为false，即累计输赢达到次数变化
            lowestLevelWinAndJump=[3, 3],
            highestLevelForRestartLoseTime=3,
            stopWhenBlast=True,
            **kwargs):
        """初始化方法

        15次打法

        Keyword Arguments:
            initLevel {number} -- [description] (default: {3})
            levelType {number} -- [description] (default: {0})
            money {number} -- [description] (default: {10000})
            stopWhenProfit {bool} -- [description] (default: {True})
            stopProfit {number} -- [description] (default: {8000})
            firstStake {number} -- [description] (default: {1})
            lowestLevelWinAndJump {list} -- [description] (default: {[3,3]})
            stopWhenBlast {bool} -- [description] (default: {True})
        """
        Rule.__init__(self, money=money)
        self.initLevel = initLevel
        self.lastLevelStop = lastLevelStop
        self.pureChange = pureChange
        self.reverseStake = reverseStake
        self.stay_times = stay_times
        self.randomStake = randomStake
        self.recursiveStake = recursiveStake
        self.firstStake = firstStake
        self.levelType = levelType
        self.levelSteps = self.levels[levelType]
        self.stopProfit = stopProfit
        self.stopWhenBlast = stopWhenBlast
        self.stopWhenProfit = stopWhenProfit
        self.lowestLevelWinAndJump = lowestLevelWinAndJump
        self.highestLevelForRestartLoseTime = highestLevelForRestartLoseTime

    def getFirstStakeAndMoney(self):
        self.currentRank = self.initLevel
        self.current_level_win_or_lose = 0
        self.current_level_win = 0
        self.current_level_lose = 0
        self.current_level_time = 0
        return (self.firstStake, self.levelSteps[self.currentRank])

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

    def checkIfHighestLevel(self, result):
        r = False
        if self.current_level_lose == self.highestLevelForRestartLoseTime and self.currentRank == len(self.levelSteps) - 1:
            if self.stopWhenBlast:
                result['stop'] = 1
                result['info'] = '停止，'
            else:
                self.currentRank = self.initLevel
                result['info'] = '重新开始，'
            result['buster'] += 1
            result['is_buster'] = True
            self.current_level_win = 0
            self.current_level_lose = 0
            self.current_level_win_or_lose = 0
            self.current_level_time = 0
            r = True
        return r

    def setMoney(self, result):
        # 上次赢了
        self.current_level_time += 1
        if result['win']:
            self.current_level_win += 1
            self.current_level_win_or_lose += 1
        # 上次输了
        else:
            if result['winner_id'] != 3:
                self.current_level_lose += 1
                self.current_level_win_or_lose -= 1
            else:
                # 当做没有发生过
                self.current_level_time -= 1
        if result['profit'] >= self.stopProfit:
            result['stop'] = 1
        # 达到了指定次数时判断
        if self.checkIfHighestLevel(result):
            result['info'] += '爆掉'
        elif self.current_level_time == self.stay_times:
            clearFlag = True
            self.current_level_time = 0
            if self.lastLevelStop and self.currentRank == len(self.levelSteps) - 1:
                result['stop'] = 1
                result['info'] = '最后一级次数达到，停止'
            # 最低级赢了足够的次数，跳级
            elif self.currentRank == 0 and self.current_level_win == self.lowestLevelWinAndJump[0]:
                self.currentRank = self.lowestLevelWinAndJump[1]
                result['info'] = '最低级赢了%s次，跳级到%s级' % (self.lowestLevelWinAndJump[0], self.lowestLevelWinAndJump[1])
            # 最低级没有赢足够次数、以及其他等级
            else:
                if self.pureChange:
                    if self.current_level_win_or_lose in [-4, -5, -6]:
                        self.currentRank += 1
                        result['info'] = '本档累计输掉3次，打下一档'
                    elif self.current_level_win_or_lose in [-7, -8, -9, -10]:
                        self.currentRank += 2
                        result['info'] = '本档累计输掉5次，打+2档'
                    elif self.current_level_win_or_lose in [-11, -12, -13, -14, -15]:
                        self.currentRank += 3
                        result['info'] = '本档累计输掉9次，打+3档'
                    else:
                        clearFlag = False
                        result['info'] = '不变'
                else:
                    if self.current_level_lose in [4, 5, 6]:
                        self.currentRank += 1
                        result['info'] = '本档累计输掉3次，打下一档'
                    elif self.current_level_lose in [7, 8, 9, 10]:
                        self.currentRank += 2
                        result['info'] = '本档累计输掉5次，打+2档'
                    elif self.current_level_lose in [11, 12, 13, 14, 15]:
                        self.currentRank += 3
                        result['info'] = '本档累计输掉9次，打+3档'
                    else:
                        clearFlag = False
                        result['info'] = '不变'

            if clearFlag:
                self.current_level_win = 0
                self.current_level_lose = 0
                self.current_level_win_or_lose = 0

        # 没有达到指定次数
        else:
            # 之后一级爆掉
            if self.checkIfHighestLevel(result):
                result['info'] += '爆掉'
            else:
                result['info'] = '仍旧打这一级'
        if self.currentRank > len(self.levelSteps) - 1:
            self.currentRank = len(self.levelSteps) - 1
        money = self.levelSteps[self.currentRank]
        return money