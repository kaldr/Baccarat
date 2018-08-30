import random


class Card:
    numbers = [
        'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', "Q", 'K'
    ]
    colors = ['♥', '♠', '♣', '♦']
    jokers = ['Big Joker', 'Small Joker']

    def a_deck_of_cards(self, shuffle=False, Joker=False):
        cards = []
        for n in self.numbers:
            for c in self.colors:
                cards.append("%s%s" % (c, n))
        if Joker:
            cards += self.jokers

        if shuffle:
            random.shuffle(cards)

        return cards

    def decks_of_cards(self, deck=1, shuffle=False, Joker=False):
        decks = []

        for i in range(deck):
            decks += self.a_deck_of_cards(shuffle=True, Joker=Joker)

        if shuffle:
            random.shuffle(decks)

        return decks
