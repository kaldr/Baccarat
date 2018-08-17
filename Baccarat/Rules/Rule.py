class Rule:
    def __init__(self,
                 money=10000,
                 levelType=0,
                 loseAndStop=True,
                 stakeFollowPrevious=True,
                 randomStake=False):
        self.differ = 10000
        self.differ_span = 10000
        self.loss = -110000
        self.lossspan = -110000

        self.stop = False

        self.current_stake = 0
        self.current_stake_money = 0

        self.money = money
        self.current_money = money

        self.currentRank = 0
        self.lose_time = 0
        self.current_level_win_or_loose = 0
        self.win_or_lose = 0
        self.baccarat_id = 0
        self.initial_rank = 0

    def getFirstStakeAndMoney(self):
        self.currentRank = 0
        return (1, 50)