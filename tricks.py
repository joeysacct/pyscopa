import random
from itertools import combinations
import numpy as np
from card import Card
from deck import Deck


# TRICK STRUCTURE:
# (s,v, [(s,v) of each card on table])

#

value_lookup = {
    "A": 1, 
    "2": 2, 
    "3": 3, 
    "4": 4, 
    "5": 5, 
    "6": 6, 
    "7": 7, 
    "J": 8,
    "Q": 9,
    "K": 10
}

def trick_prompt(trick):
    card = trick[0]
    table_cards = trick[1]
    is_scopa = trick[2]
    scopacheck = "(SCOPA)" if is_scopa else ""
    if len(table_cards) == 0:  #discard
        return "Discard " + card.name() + scopacheck
    return card.name() + "<=>" + "+".join([c.name() for c in table_cards]) + scopacheck

def get_tricks(hand, table):
   # check for direct captures
    direct_captures = []
    for card in hand.cards:
        for table_card in table.cards:
            if table_card.value == card.value:
                is_scopa = table.num_cards() == 1
                direct_captures.append([card, [table_card], is_scopa])

    # if direct captures exist, return those.
    if len(direct_captures) > 0:
        return direct_captures

    # if no direct captures, test for combo captures. return that list.
    combo_captures = []
    for card in hand.cards:
        # print(value_lookup[card.value])
        for r in range(2, table.num_cards() + 1):
            unique_combos = combinations(table.cards, r)
            for combo in unique_combos:
                sum_value = 0
                # print([value_lookup[c.value] for c in combo])
                sum_value = sum([value_lookup[c.value] for c in combo])
                if sum_value == value_lookup[card.value]:
                    # print("Combo found!")
                    is_scopa = table.num_cards() == r
                    combo_captures.append([card, [c for c in combo], is_scopa])

    if len(combo_captures) > 0:
        return combo_captures

    # if neither exists, return discard options.
    discards = []
    for card in hand.cards:
        discards.append([card, [], False])
    return discards


def play_trick(trick, table, hand, pile):
    hand_card= trick[0]
    if len(trick[1]) == 0: # if trick is a discard
       hand.deal_card(table, hand_card) 
    else:
        hand.deal_card(pile, hand_card)
        for table_card in trick[1]:
            table.deal_card(pile, table_card)


def play_comp_trick(tricks, table, comp_hand, comp_pile):
    trick = random.choice(tricks) # TODO make anythign at all happen here lol

    play_trick(trick, table, comp_hand, comp_pile)
    return trick


if __name__ == "__main__":
    deck = Deck()
    hand = Deck()
    hand.add_card(Card(0,"Coins","o","5"))
    deck.add_card(Card(0,"Swords","o","2"))
    deck.add_card(Card(0,"Batons","o","3"))

    tricks = get_tricks(hand, deck) # Test to get multi-card tricks
    print(tricks)



    
