from Poker.Card import Card
from random import randrange


class Baccarat:

    commission = 0.05
    cards = Card().decks_of_cards(deck=8, shuffle=True, Joker=False)
    stakeType = ['庄', '闲', '和', '对']
    drawedCards = []
    history_rounds = []
    current_round = 0
    current_xian_cards = []
    current_zhuang_cards = []
    current_suppliment_cards = {}
    current_result = 0

    def __init__(self):
        self.rounds = self.setRounds()

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
                self.current_zhuang_cards.append(self.draw_a_card())
            else:
                self.current_xian_cards.append(self.draw_a_card())
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
        if zhuang >= 10:
            zhuang -= 10
        if xian >= 10:
            xian -= 10
        # 天王
        if zhuang > 7 or xian > 7:
            return {}
        # 无天王
        else:
            # 玩家首2值为0，1，2，3，4，5，摸牌
            if xian < 6:
                # 玩家摸牌
                card = self.draw_a_card()
                self.current_xian_cards.append(card)
                xian += self.change_card_to_number(card)
                if xian >= 10:
                    xian -= 10
            # 庄家根据如下情况判断是否摸牌
            zhuangFlag = False
            if zhuang in [0, 1, 2]:
                zhuangFlag = True
            elif zhuang == 3:
                if xian == 8:
                    zhuangFlag = False
                else:
                    zhuangFlag = True
            elif zhuang == 4:
                if xian in [0, 1, 8, 9]:
                    zhuangFlag = False
                else:
                    zhuangFlag = True
            elif zhuang == 5:
                if xian in [0, 1, 2, 3, 8, 9]:
                    zhuangFlag = False
                else:
                    zhuangFlag = True
            elif zhuang == 6:
                if xian in [6, 7]:
                    zhuangFlag = True
            else:
                zhuangFlag = False
            if zhuangFlag:
                card = self.draw_a_card()
                self.current_zhuang_cards.append(card)
                zhuang += self.change_card_to_number(card)
                if zhuang >= 10:
                    zhuang -= 10

    def change_card_to_number(self, card):
        card = card[1:]
        if card == 'A':
            return 1
        elif card in ['10', "J", "Q", "K"]:
            return 0
        else:
            return int(card)

    def round_result(self,
                     zhuang_cards=[],
                     xian_cards=[]):
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
        }

    def win_or_not(self, stake=1):
        result = self.round_info()

        if stake == self.current_result:
            result['win'] = True
        else:
            result['win'] = False
        return result
