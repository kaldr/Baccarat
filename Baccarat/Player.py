from .Baccarat import Baccarat
import random
import xlwt
import os
from .PlayerExporter import PlayerExporter


class Player:

    # rankToStop=5000
    lose_time_upper = 70
    triple_ranks = [
        50, 100, 150, 200, 250, 300, 400, 500, 600, 700, 800, 900, 1000, 1200,
        1400, 1600, 1900, 2200, 2600, 3000, 3500, 4000, 4500, 5000, 5700, 6400,
        7100, 8000, 9000, 10000, 11500, 13000, 14500, 17000, 19000, 21000,
        23000, 25500, 28000
    ]
    ranks = [
        50, 70, 100, 130, 150, 180, 200, 230, 250, 280, 300, 330, 350, 380,
        400, 430, 450, 480, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950,
        1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2200,
        2400, 2600, 2800, 3000, 3200, 3400, 3600, 3800, 4000, 4500, 5000, 5500,
        6000, 6500, 7000, 7500, 8000, 8500, 9000, 9500, 10000, 11000, 12000,
        13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000
    ]

    def __init__(self,
                 name='李妙',
                 money=10000,
                 rule=0,
                 rule_2_stake_reverse=False,
                 rule_1_stake_reverse=False):

        self.differ = 10000
        self.rule_2_stake_reverse = rule_2_stake_reverse
        self.rule_1_stake_reverse = rule_1_stake_reverse
        self.differ_span = 10000
        self.loss = -110000
        self.lossspan = -110000
        self.result_history = []
        self.zero_level_win = 0
        self.stop = 0
        self.current_stake = 0
        self.current_stake_money = 0
        self.rule = rule
        self.money = money
        self.current_money = money
        self.name = name
        self.currentRank = 0
        self.lose_time = 0
        self.current_level_win_or_loose = 0
        self.win_or_lose = 0
        self.baccarat_id = 0
        self.initial_rank = 0
        if rule == 1:
            self.setNextMoneyAndStakeFromRuleCrossStake()
            self.current_stake = 1
            if self.rule_1_stake_reverse:
                self.current_stake = 2
        if rule == 2:
            self.current_stake = 1
            if self.rule_2_stake_reverse:
                self.current_stake = 2
            self.current_stake_money = 50
        if rule == 3:
            self.differ = 3000
            self.currentRank = 2
            self.differ_span = 3000
            self.initial_rank = 2
            self.current_stake_money = 150
        else:
            self.setNextMoneyAndStakeFromRuleRandom()
        self.exporter = PlayerExporter(self)

    def set_current_round_result(self, result):
        if not self.stop:
            if result['round_id'] == 1:
                self.baccarat_id += 1
            result['baccarat_id'] = self.baccarat_id
            result['stake'] = Baccarat.stakeType[self.current_stake - 1],
            result['stake_money'] = self.current_stake_money
            result['money_before'] = self.current_money
            result['change'] = 0
            if result['win']:
                self.win_or_lose += 1
                if self.current_stake == 1:
                    change = self.current_stake_money * \
                        (1 - Baccarat.commission)
                elif self.current_stake == 2:
                    change = self.current_stake_money
                result['change'] = change
                self.current_money += change
            else:
                if result['winner_id'] != 3:
                    self.win_or_lose -= 1
                    result['change'] = self.current_stake_money * (-1)
                    self.current_money -= self.current_stake_money
            result['money'] = self.current_money
            result['profit'] = self.current_money - self.money
            result['win_or_lose'] = self.win_or_lose
            self.result_history.append(result)
            result['info'] = ''
            self.setNextMoneyAndStake(result)

    def setNextMoneyAndStake(self, result={}):
        if self.rule == 1:
            self.setNextMoneyAndStakeFromRuleCrossStake(result)
        elif self.rule == 2 or self.rule == 3:
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

        # if self.currentRank == len(self.ranks):
        #     self.currentRank = 0
        #     result['info'] = '遍历完了，从最开始重新打'
        # 如果赚到了一定量的钱，从第一级开始打
        # if self.current_money - self.money > self.differ:
        #     self.currentRank = 0
        #     self.differ += self.differ_span
        #     result['info'] = '赢到了%s，重新开始打' % self.differ
        # self.stop = 1
        # 如果赔了相应的钱，从第一级开始打
        # if self.current_money - self.money < self.loss:
        #     self.currentRank = 0
        #     self.stop = 1
        #     self.loss += self.lossspan
        # lastLevel = self.triple_ranks[-1]
        # if self.current_stake_money == lastLevel and self.current_level_win_or_loose == -3:
        #     self.currentRank = 0
        #     self.stop = 0
        #     result['info'] = '最后一级输了3次，重新开始打' % lastLevel
        # if self.lose_time > self.lose_time_upper:
        #     self.currentRank = 0
        #     result['info'] = '输超过了%s次，重新开始打' % self.lose_time_upper
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
        if result:
            if result['round_id'] == 1:
                if self.rule_1_stake_reverse:
                    self.current_stake = 2
                else:
                    self.current_stake = 1

        self.CrossStakeMoney(result)

    def setNextLevelWhenLevelWinOrLose(self, result):
        if self.current_level_win_or_loose == -3:
            self.current_level_win_or_loose = 0
            self.currentRank += 1
            if self.currentRank == len(self.triple_ranks):
                self.stop = 1
                result['info'] = '最后一级输了3次，停止'
            else:
                result['info'] = '输了3次，打下一级'

        if self.current_level_win_or_loose == 3:
            self.current_level_win_or_loose = 0
            self.currentRank -= 1
            result['info'] = '赢了3次，打上一级'

    def setNextLevelWhenTotalWinOrLose(self,
                                       result,
                                       cost_lose_restart=False,
                                       top_restart=True):
        if top_restart or self.rule == 3:
            if self.current_money - self.money >= self.differ:
                result['info'] = '赢了%d重新打' % self.differ
                self.differ += self.differ_span
                self.currentRank = self.initial_rank
                return
            # if self.win_or_lose < -50:
            #     self.stop = 1
            #     return
        if self.win_or_lose >= 0:
            if self.rule == 3:
                if self.win_or_lose == 3:
                    self.currentRank = 1
                elif self.win_or_lose == 6:
                    self.currentRank = 0
                elif self.win_or_lose == 9:
                    self.currentRank = 2
                    self.win_or_lose = 0
                # self.current_level_win_or_loose = 0
            elif self.rule == 2:
                self.currentRank = self.initial_rank
                result['info'] = '没输，打最低级'
        else:

            lose_time = -self.win_or_lose
            if lose_time % 3 == 0:
                # if self.zero_level_win:
                #     self.currentRank += lose_time // 3
                # else:
                self.currentRank = lose_time // 3 + self.initial_rank
                if self.currentRank >= len(self.triple_ranks):
                    if cost_lose_restart:
                        self.win_or_lose = 0
                        self.currentRank = self.initial_rank
                        result['info'] = '爆了，重新开始打'
                    else:
                        self.stop = 1
                        result['info'] = '爆了停止'
                else:
                    result['info'] = '输了%d次，打%d级' % (lose_time,
                                                     self.currentRank)
            else:
                result['info'] = '净输了%d次，仍然打%d级' % (lose_time,
                                                    self.currentRank)

    def setNextMoneyAndStakeFromRuleComplicated(self, result={}):
        result['info'] = '没有赢或者输3次，继续打这一等级'
        if result['win']:
            self.current_level_win_or_loose += 1
        else:
            if result["winner_id"] != 3:
                self.current_level_win_or_loose -= 1
            else:
                result['info'] = '和，当做没有发生过'

        # self.setNextLevelWhenLevelWinOrLose(result)
        self.setNextLevelWhenTotalWinOrLose(result)

        # if self.currentRank == len(self.triple_ranks):
        #     self.currentRank = 0
        if self.currentRank == -1:
            self.currentRank = 0
        if self.currentRank >= len(self.triple_ranks):
            self.currentRank = len(self.triple_ranks) - 1
        if result['winner_id'] != 3:
            self.current_stake = result['winner_id']
            if self.rule_2_stake_reverse:
                if result['winner_id'] == 1:
                    self.current_stake = 2
                else:
                    self.current_stake = 1
        # if self.current_money - self.money > self.differ:
        #     result['info'] = '赢到了%s，重新开始打' % self.differ
        #     self.differ += self.differ_span
        #     self.currentRank = 0
        # if self.current_money - self.money < self.loss:
        #     self.currentRank = 0
        #     self.loss += self.lossspan
        #     result['info'] = '亏了%s，重新打' % self.loss
        # lastLevel = self.triple_ranks[-1]
        # if self.currentRank == len(self.triple_ranks) - 1 and self.current_level_win_or_loose == -3:
        #     self.currentRank = 0
        #     self.stop = 0
        #     result['info'] = '最后一级输了3次，重新开始打' % lastLevel
        self.current_stake_money = self.triple_ranks[self.currentRank]

    def exportToExcel(self, filename='玩家', folder=False):
        workbook = xlwt.Workbook(encoding='utf-8')
        data = self.result_history
        header = {
            'baccarat_id': "局",
            'round_id': "轮",
            'zhuang': "庄牌",
            "zhuang_point": "庄家点数",
            'xian': "闲牌",
            "xian_point": "闲家点数",
            'winner': "赢家",
            'stake': "押注",
            "change": "本轮变化",
            'win': "本轮输赢",
            'win_or_lose': "净",
            'stake_money': "押注金额",
            # "money_before": "押注前金额",
            # 'money': "本轮后金额",
            'profit': "总盈利",
            'info': "决策"
        }
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


print("全输掉，成本是：%d" % (sum(Player.triple_ranks) * 3))
