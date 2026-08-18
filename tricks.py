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
    "J": 99999,
    "Q": 99999,
    "K": 99999
}

def get_tricks(hand, table):
   # check for direct captures
    direct_captures = []
    for card in hand.cards:
        for table_card in table.cards:
            if table_card.value == card.value:
                direct_captures.append([card.suit, card.value, [(table_card.suit, table_card.value)]])

    # if direct captures exist, return those.
    if len(direct_captures) > 0:
        return direct_captures

    # if no direct captures, test for combo captures. return that list.
    combo_captures = []
    for card in hand.cards:
        for r in range(2, table.num_cards() + 1):
            unique_combos = combinations(table.cards, r)
            for combo in unique_combos:
                sum_value = 0
                for card in combo:
                    sum_value += value_lookup[card.value_chr]
                if sum_value == value_lookup[card.value_chr]:
                    combo_captures.append([card.suit, card.value, [(c.suit, c.value) for c in combo]])

    if len(combo_captures) > 0:
        return combo_captures

    # if neither exists, return discard options.
    discards = []
    for card in hand.cards:
        discards.append([card.suit, card.value, []])
    return discards


def play_trick(trick, table, hand, pile):
    hand_card_suit, hand_card_value = trick[0], trick[1]
    hand_card_idx = hand.card_idx_from_s_v(hand_card_suit, hand_card_value)
    if len(trick[2]) == 0: # if trick is a discard
       hand.deal(table, hand_card_idx) 
    else:
        hand.deal(pile, hand_card_idx)

        for table_card_suit, table_card_value in trick[2]:
            table_card_idx = table.card_idx_from_s_v(table_card_suit, table_card_value)
            table.deal(pile, table_card_idx)


def play_comp_trick(tricks, table, comp_hand, comp_pile):
    trick = random.choice(tricks) # TODO make anythign at all happen here lol


    play_trick(trick, table, comp_hand, comp_pile)
    return trick

