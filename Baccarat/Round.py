class Round:
    def __init__(self, baccarat, players=[]):
        self.baccarat = baccarat
        self.startRound()
        self.win_or_lose(players)

    def startRound(self):
        self.baccarat.startRound()
        (zhuang_cards, xian_cards) = self.baccarat.draw()
        self.baccarat.supplement()
        self.baccarat.round_result()
        # print(self.baccarat.round_info())

    def win_or_lose(self, players=[]):
        # print(self.baccarat.round_info())
        for player in players:
            win = self.baccarat.win_or_not(player.current_stake)
            player.set_current_round_result(win)