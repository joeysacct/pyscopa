from card import Card
from deck import Deck
from menu import render_screen
from tricks import get_tricks, play_trick, play_comp_trick, trick_prompt


class Player:
    def __init__(self, player_name='Player', player_type='player'):
        self.type = player_type
        self.name = player_name
        
        self.hand = Deck()
        self.capture_pile = Deck()

        self.score = 0
        self.scopas = 0
        self.primiera = 0

    def cards(self):
        return self.hand.cards


    def deal_card_from_s_v(self, recipient: Deck, suit: str, value: str):
        for i, card in enumerate(self.cards):
            if card.value == value and card.suit == suit:
                dealt_card = self.cards.pop(idx)
                recipient.add_card(card)

    def return_cards_to_deck(self, main_deck: Deck):
        for player_deck in (self.hand, self.capture_pile):
            for n in range(player_deck.num_cards()):
                player_deck.deal(main_deck, 0)


    def run_scopa_turn(self, stdcsr, table: Deck, opponent):
        if self.type == 'player':
            options = get_tricks(self.hand, table)
            tricks = []
            for o in options:
                tricks.append(trick_prompt(o))
            prompt = "Select a trick/discard from the list:"

            player_trick = render_screen(stdcsr, self, opponent, table, tricks, prompt, options)
            play_trick(player_trick, table, self.hand, self.capture_pile)

            if table.num_cards() == 0:
                if self.hand.num_cards() >= 0 or opponent.hand.num_cards() >= 0:
                    self.scopas += 1

        elif self.type == "comp":
            comp_tricks = get_tricks(self.hand, table)
            comp_trick = play_comp_trick(comp_tricks, table, self.hand, self.capture_pile)
            tricks = ["Continue Game"]

            scopacheck = ""
            if table.num_cards() == 0:
                if self.hand.num_cards() >= 0 or opponent.hand.num_cards() >= 0:
                    self.scopas += 1
                    scopacheck = "Scopa!"

            prompt = f"COMP played {trick_prompt(comp_trick)}. {scopacheck}"
            options = ['Continue Game']

            _ = render_screen(stdcsr, opponent, self, table, tricks, prompt, options) # flipped to keep parity when playing solo.
