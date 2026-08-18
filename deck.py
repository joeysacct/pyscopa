from card import Card
import random

class Deck:
    def __init__(self):
        self.cards = []


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
                raise ValueError(f"{self.cards}")
            card = self.cards.pop(0)
            recipient_deck.add_card(card)


    def deal(self, recipient_deck, card_idx):
        card = self.cards.pop(card_idx)
        recipient_deck.add_card(card)


    def deal_all(self, recipient_deck):
        for n in range(self.num_cards()):
            card = self.cards.pop(0)
            recipient_deck.add_card(card)
