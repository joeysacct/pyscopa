from card import Card
import random

class Deck:


    def __init__(self):
        self.cards = []
        self.PIPE_SETS = [
            "┃━┏┓┗┛",
            "│─╭╮╰╯",
            "│─┌┐└┘",
            "║═╔╗╚╝",
            "╿╼┍┑┕┚",
        ]


    def populate_deck(self,
                      suits=[ "Coins", "Cups", "Swords", "Batons" ],
                      suit_chrs=["o", "U", "?", "!"],
                      values=[ "A", "2", "3", "4", "5", "6", "7", "J", "Q", "K" ],
                      pipe_set=3):
        for s, sc in zip(suits, suit_chrs):
            for v in values:
                card = Card(self.PIPE_SETS[pipe_set], s, sc, v)
                self.add_card(card)


    def add_card(self, card):
        self.cards.append(card)


    def shuffle(self):
        random.shuffle(self.cards)
        

    def card_idx_from_s_v(self, suit, value):
        for i, card in enumerate(self.cards):
            if card.value == value and card.suit == suit:
                return i
        return None


    def num_cards(self):
        return len(self.cards)


    def deal_from_top(self, recipient_deck, n_cards):
        for n in range(n_cards):
            if self.num_cards() == 0:
                continue
            card = self.cards.pop(0)
            recipient_deck.add_card(card)


    def deal_card(self, recipient_deck, card):
        card_idx = self.card_idx_from_s_v(card.suit,card.value)
        self.deal(recipient_deck, card_idx)


    def deal(self, recipient_deck, card_idx):
        card = self.cards.pop(card_idx)
        recipient_deck.add_card(card)


    def deal_all(self, recipient_deck):
        for n in range(self.num_cards()):
            card = self.cards.pop(0)
            recipient_deck.add_card(card)



    def has_card(self, suit, value):
        return any(card.suit == suit and card.value == value for card in self.cards)


    def cards_with_suit(self,suit):
        return [c for c in self.cards if c.suit == suit]


    def cards_with_value(self, value):
        return [c for c in self.cards if c.value == value]
