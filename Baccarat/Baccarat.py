from Poker.Card import Card
from random import randrange


class Baccarat:

    commission = 0.05

    stakeType = ['庄', '闲', '和', '对']
    # 闲从0-9
    zhuang_third_card_rule = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 庄为0
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 庄为1
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 庄为2
        [1, 1, 1, 1, 1, 1, 1, 1, 0, 1],  # 庄为3
        [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],  # 庄为4
        [0, 0, 0, 0, 1, 1, 1, 1, 0, 0],  # 庄为5
        [0, 0, 0, 0, 0, 0, 1, 1, 0, 0],  # 庄为6
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 庄为7
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 庄为8
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 庄为9
    ]

    def __init__(self):
        self.cards = Card().decks_of_cards(deck=8, shuffle=True, Joker=False)
        self.drawedCards = []
        self.history_rounds = []
        self.current_round = 0
        self.current_xian_cards = []
        self.current_zhuang_cards = []
        self.current_suppliment_cards = {}
        self.current_result = 0
        self.rounds = self.setRounds()
        self.info = ''

    def printChart(self):
        pass

    def setRounds(self):
        return randrange(65, 71)

    def draw_a_card(self):
        card = self.cards[0]
        self.drawedCards.append(card)
        self.cards = self.cards[1:]
        return card

    def startRound(self):
        self.current_zhuang_cards = []
        self.current_xian_cards = []
        self.current_suppliment_cards = {}
        self.current_result = 0
        self.current_round += 1
        return self.current_round

    def draw(self):
        for i in range(4):
            if i % 2 == 0:
                self.current_xian_cards.append(self.draw_a_card())
            else:
                self.current_zhuang_cards.append(self.draw_a_card())
        return (self.current_zhuang_cards, self.current_xian_cards)

    def supplement(self, zhuang_cards=[], xian_cards=[]):
        zhuang = 0
        xian = 0
        if not zhuang_cards:
            zhuang_cards = self.current_zhuang_cards
        if not xian_cards:
            xian_cards = self.current_xian_cards
        for i in zhuang_cards:
            zhuang += self.change_card_to_number(i)
        for i in xian_cards:
            xian += self.change_card_to_number(i)
        xian = xian % 10
        zhuang = zhuang % 10
        xian_before = xian
        zhuang_before = zhuang
        if zhuang >= 10:
            zhuang -= 10
        if xian >= 10:
            xian -= 10
        # 天王
        if zhuang > 7 or xian > 7:
            self.info = '有一方前两张牌已经是8、9，不需要摸第三张牌'
            return {}
        # 无天王，闲为6、7
        elif xian > 5:
            if zhuang > 5:
                self.info = "闲为6、7，庄也为6、7，庄不需要摸排"
            else:
                self.info = '闲为6、7，庄小于6，庄需要摸牌'
                card = self.draw_a_card()
                self.current_zhuang_cards.append(card)
        # 无天王，闲不是6、7
        else:
            self.info = ''
            # 玩家首2值为0，1，2，3，4，5，摸牌
            xianFlag = False
            card_value = 0
            if xian < 6:
                # 玩家摸牌
                card = self.draw_a_card()
                self.current_xian_cards.append(card)
                self.info = '玩家小于6点，必须摸牌；'
                card_value = self.change_card_to_number(card)
                xian += card_value
                xianFlag = True
                if xian >= 10:
                    xian = xian % 10
            # 庄家根据如下情况判断是否摸牌
            zhuangFlag = self.zhuang_third_card_rule[zhuang_before][card_value]

            if zhuangFlag:
                self.info += '庄为%d，闲第三张为%d，装摸牌' % (zhuang_before, card_value)
                card = self.draw_a_card()
                self.current_zhuang_cards.append(card)
                zhuang += self.change_card_to_number(card)
                if zhuang >= 10:
                    zhuang -= 10
            else:
                self.info += '庄为%d，闲第三张为%d，装不摸牌' % (zhuang_before, card_value)

    def change_card_to_number(self, card):
        card = card[1:]
        if card == 'A':
            return 1
        elif card in ['10', "J", "Q", "K"]:
            return 0
        else:
            return int(card)

    def round_result(self, zhuang_cards=[], xian_cards=[]):
        zhuang = 0
        xian = 0
        if not zhuang_cards:
            zhuang_cards = self.current_zhuang_cards
        if not xian_cards:
            xian_cards = self.current_xian_cards
        for i in zhuang_cards:
            zhuang += self.change_card_to_number(i)
        for i in xian_cards:
            xian += self.change_card_to_number(i)
        if zhuang >= 10:
            zhuang = zhuang % 10
        if xian >= 10:
            xian = xian % 10
        self.current_zhuang_point = zhuang
        self.current_xian_point = xian
        if zhuang > xian:
            self.current_result = 1
        elif zhuang < xian:
            self.current_result = 2
        elif zhuang == xian:
            self.current_result = 3
        result = self.round_info()
        self.history_rounds.append(result)
        return self.current_result

    def round_info(self):
        return {
            "round_id": self.current_round,
            "zhuang": ' '.join(self.current_zhuang_cards),
            "xian": " ".join(self.current_xian_cards),
            "winner_id": self.current_result,
            "winner": self.stakeType[self.current_result - 1],
            "zhuang_point": self.current_zhuang_point,
            "xian_point": self.current_xian_point,
            'draw_info': self.info
        }

    def win_or_not(self, stake=1):
        result = self.round_info()

        if stake == self.current_result:
            result['win'] = True
        else:
            result['win'] = False
        return result
