from .Baccarat import Baccarat
import random
import xlwt
import os


class Player:

    # rankToStop=5000
    lose_time_upper = 70
    triple_ranks = [
        50,
        100,
        150,
        200,
        250,
        300,
        400,
        500,
        600,
        700,
        800,
        900,
        1000,
        1200,
        1400,
        1600,
        1800,
        2000,
        2300,
        2600,
        2900,
        3200,
        3600,
        4000
    ]
    ranks = [
        50,
        70,
        100,
        130,
        150,
        180,
        200,
        230,
        250,
        280,
        300,
        330,
        350,
        380,
        400,
        430,
        450,
        480,
        500,
        550,
        600,
        650,
        700,
        750,
        800,
        850,
        900,
        950,
        1000,
        1100,
        1200,
        1300,
        1400,
        1500,
        1600,
        1700,
        1800,
        1900,
        2000,
        2200,
        2400,
        2600,
        2800,
        3000,
        3200,
        3400,
        3600,
        3800,
        4000,
        4500,
        5000,
        5500,
        6000,
        6500,
        7000,
        7500,
        8000,
        8500,
        9000,
        9500,
        10000,
        11000,
        12000,
        13000,
        14000,
        15000,
        16000,
        17000,
        18000,
        19000,
        20000
    ]

    def __init__(self, name='李妙', money=10000, rule=0):
        self.differ = 5000
        self.differ_span = 5000
        self.loss = -3000
        self.lossspan = -1000
        self.result_history = []
        self.stop = 0
        self.current_stake = 0
        self.current_stake_money = 0
        self.current_money = 0
        self.rule = rule
        self.money = money
        self.current_money = money
        self.name = name
        self.currentRank = -1
        self.lose_time = 0
        self.current_level_win_or_loose = 0

        if rule == 1:
            self.setNextMoneyAndStakeFromRuleCrossStake()
            self.current_stake = 1
        else:
            self.setNextMoneyAndStakeFromRuleRandom()

    def set_current_round_result(self, result):
        if not self.stop:
            result['stake'] = Baccarat.stakeType[self.current_stake - 1],
            result['stake_money'] = self.current_stake_money
            result['money_before'] = self.current_money
            result['change'] = 0
            if result['win']:
                if self.current_stake == 1:
                    change = self.current_stake_money * \
                        (1 - Baccarat.commission)
                elif self.current_stake == 2:
                    change = self.current_stake_money
                result['change'] = "+%s" % change
                self.current_money += change
            else:
                if result['winner_id'] != 3:
                    result['change'] = "-%s" % self.current_stake_money
                    self.current_money -= self.current_stake_money
            result['money'] = self.current_money
            result['profit'] = self.current_money - self.money
            self.result_history.append(result)
            result['info'] = ''
            self.setNextMoneyAndStake(result)

    def setNextMoneyAndStake(self, result={}):
        if self.rule == 1:
            self.setNextMoneyAndStakeFromRuleCrossStake(result)
        elif self.rule == 2:
            self.setNextMoneyAndStakeFromRuleComplicated(result)
        else:
            self.setNextMoneyAndStakeFromRuleRandom(result)

    def setNextMoneyAndStakeFromRuleRandom(self, result={}):
        self.current_stake = random.randrange(1, 3)
        self.CrossStakeMoney(result)

    def CrossStakeMoney(self, result={}):

        if result:
            if not result['win']:
                self.lose_time += 1
                self.currentRank += 1
                result['info'] = '本轮没有赢，下一轮打下一级'
            else:
                self.currentRank -= 1
                if self.currentRank < 0:
                    self.currentRank = 0
                self.lose_time = 0
                result['info'] = '本轮赢，打上一级'
            # 遍历完了，从第一级开始打
        else:
            self.currentRank += 1
        if self.currentRank == len(self.ranks):
            self.currentRank = 0
            result['info'] = '遍历完了，从最开始重新打'
        # 如果赚到了一定量的钱，从第一级开始打
        if self.current_money - self.money > self.differ:
            self.currentRank = 0
            result['info'] = '赢到了%s，停止' % self.differ
            self.stop = 1
        # 如果赔了相应的钱，连续输超过n轮，从第一级开始打
        if self.current_money - self.money < self.loss:
            self.currentRank = 0
            self.stop = 1
            self.loss += self.lossspan

        if self.lose_time > self.lose_time_upper:
            self.currentRank = 0
            result['info'] = '输超过了%s次，重新开始打' % self.lose_time_upper
            # if self.current_stake==1:
            #     self.current_stake=2
            # elif self.current_stake==2:
            #     self.current_stake=1

            # if self.current_stake_money>5000:
        #     self.currentRank=0
        self.current_stake_money = self.ranks[self.currentRank]

    def setNextMoneyAndStakeFromRuleCrossStake(self, result={}):
        if self.current_stake == 1:
            self.current_stake = 2
        elif self.current_stake == 2:
            self.current_stake = 1

        self.CrossStakeMoney(result)

    def setNextMoneyAndStakeFromRuleComplicated(self, result={}):
        result['info'] = '没有赢或者输3次，继续打这一等级'
        if result['win']:
            self.current_level_win_or_loose += 1
        else:
            if result["winner_id"] != 3:
                self.current_level_win_or_loose -= 1
            else:
                result['info'] = '和，当做没有发生过'

        if self.current_level_win_or_loose == -3:
            self.current_level_win_or_loose = 0
            self.currentRank += 1
            result['info'] = '输了3次，打下一级'

        if self.current_level_win_or_loose == 3:
            self.current_level_win_or_loose = 0
            self.currentRank -= 1
            result['info'] = '赢了3次，打上一级'

        if self.currentRank == len(self.triple_ranks):
            self.currentRank = 0
        if self.currentRank == -1:
            self.currentRank = 0
        if result['winner_id'] != 3:
            self.current_stake = result['winner_id']

        if self.current_money - self.money > self.differ:
            result['info'] = '赢到了%s，重新开始打' % self.differ
            self.differ += self.differ_span
            self.currentRank = 0

        self.current_stake_money = self.triple_ranks[self.currentRank]

    def exportToExcel(self, filename='玩家', folder=False):
        workbook = xlwt.Workbook(encoding='utf-8')
        data = self.result_history
        header = {
            'round_id': "轮",
            'zhuang': "庄牌",
            "zhuang_point": "庄家点数",
            'xian': "闲牌",
            "xian_point": "闲家点数",
            'winner': "赢家",
            'stake': "押注",
            "change": "本轮变化",
            'win': "本轮输赢",
            'stake_money': "押注金额",
            "money_before": "押注前金额",
            'money': "本轮后金额",
            'profit': "总盈利",
            'info': "决策"}
        sheet = workbook.add_sheet(filename, cell_overwrite_ok=True)
        col = 0
        row = 0
        for (key, title) in header.items():
            sheet.write(row, col, title)
            for d in data:
                row += 1
                # print(d[key])
                if key == 'win':
                    if d[key]:
                        sheet.write(row, col, 1)
                    else:
                        sheet.write(row, col, -1)
                else:
                    sheet.write(row, col, d[key])
            col += 1
            row = 0
        filepath = "./Export/"

        if folder:
            filepath = filepath + folder + "/"
            if not os.path.exists(filepath.encode('utf8')):
                os.mkdir(filepath.encode('utf8'))
            filepath = filepath + filename + ".xls"
        else:
            filepath = filepath + filename + ".xls"

        workbook.save(filepath.encode('utf8'))
