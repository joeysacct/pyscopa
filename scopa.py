import random
import curses
import numpy as np
from deck import Deck
from card import Card
from tricks import get_tricks, play_trick, play_comp_trick
from menu import render_screen

PIPE_SETS = [
    "┃━┏┓┗┛",
    "│─╭╮╰╯",
    "│─┌┐└┘",
    "║═╔╗╚╝",
    "╿╼┍┑┕┚",
]

def score_piles(player_pile, comp_pile, player_scopas, comp_scopas, player_score, comp_score):
    suits = [ "Coins", "Cups", "Swords", "Batons" ]
    primiera_values = {
        "A": 16, 
        "2": 12, 
        "3": 13, 
        "4": 14, 
        "5": 15, 
        "6": 18, 
        "7": 21, 
        "J": 10,
        "Q": 10,
        "K": 10 
    }
    output = ["Round scores:"]

    # Scopas
    output.append(f"Player got {player_scopas} Scopas, and COMP got {comp_scopas} Scopas.")
    player_score += player_scopas
    comp_score += comp_scopas

    # Capture count1
    if player_pile.num_cards() > comp_pile.num_cards():
       player_score += 1
       output.append("Player captured the most cards, and earns a point.")
    elif player_pile.num_cards() < comp_pile.num_cards():
       comp_score += 1
       output.append("COMP captured the most cards, and earns a point.")
    else:
        output.append("Player and COMP captured the same number of cards.")

    # Coin count
    player_coins = sum(1 for card in player_pile.cards if card.suit == "Coins")
    comp_coins = sum(1 for card in comp_pile.cards if card.suit == "Coins")
    if player_coins > comp_coins:
       player_score += 1
       output.append("Player captured the most coins, and earns a point.")
    elif player_coins < comp_coins:
       comp_score += 1
       output.append("COMP captured the most coins, and earns a point.")
    else:
       output.append("Player and COMP captured the same numebr of coins.")

    # seven of coins 
    if any(card.suit == "Coins" and card.value_chr == "7" for card in player_pile.cards):
       player_score += 1
       output.append("Player captured the 7 of Coins, and thus earns a point.")
    elif any(card.suit == "Coins" and card.value_chr == "7" for card in comp_pile.cards):
       comp_score += 1
       output.append("COMP captured the 7 of Coins, and thus earns a point.")

    # primiera
    player_primiera = 0
    comp_primiera = 0
    for suit in suits:
       highest_player_card = max((card for card in player_pile.cards if card.suit == suit), key=lambda card: primiera_values[card.value_chr], default=0)
       highest_comp_card = max((card for card in comp_pile.cards if card.suit == suit), key=lambda card: primiera_values[card.value_chr])
       player_primiera += primiera_values[highest_player_card.value_chr]
       comp_primiera += primiera_values[highest_comp_card.value_chr]

    if player_primiera > comp_primiera:
       player_score += 1
       output.append(f"Player had the highest primiera at {player_primiera}, earning them a point.")
    elif player_primiera < comp_primiera:
       comp_score += 1
       output.append(f"COMP had the highest primiera at {comp_primiera}, earning it a point.")

    output.append(f"Player score: {player_score}, COMP score: {comp_score}")
    return "\n".join(output)

def run_scopa(stdcsr):
    repeat_game = True
    pipe_set = 0
    # instantiate deck
    deck = Deck()
    suits = [ "Coins", "Cups", "Swords", "Batons" ]
    suit_chrs = [ "o", "U", "/", "!" ]
    values = [ "Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Jack", "Queen", "King" ]
    value_chrs = [ "A", "2", "3", "4", "5", "6", "7", "J", "Q", "K" ]
    

    # populate deck with cards
    for s,sc in zip(suits, suit_chrs): 
        for v, vc in zip(values, value_chrs):
            card = Card(PIPE_SETS[pipe_set],s,sc,v,vc)
            deck.add_card(card)

    while repeat_game:
        # shuffle deck
        deck.shuffle()
        # set table, hand, score
        table = Deck()
        player_hand = Deck()
        player_pile = Deck()
        comp_hand = Deck()
        comp_pile = Deck()

        player_score = 0
        comp_score = 0

        # decide who goes first TEMP start with player
        turn = "player"

        # deal cards
        deck.deal_from_top(table, 4)
        deck.deal_from_top(player_hand, 3)
        deck.deal_from_top(comp_hand, 3)

        player_scopas = 0
        comp_scopas = 0

        while deck.num_cards() > 0: 

            if turn == "player":
                options = get_tricks(player_hand, table)
                tricks = []
                for o in options:
                    t_str = f"Hand: {o[0]}{o[1]}, Table: "
                    for t in o[2]:
                        t_str = ", ".join([t_str, f"{t[0]}{t[1]}"])
                    tricks.append(t_str)
                prompt = "Select a trick/discard from the list:"

                player_trick = render_screen(stdcsr, player_hand, comp_hand, table, tricks, prompt, options, player_score, comp_score)
                play_trick(player_trick, table, player_hand, player_pile)

                if table.num_cards() == 0:
                    if player_hand.num_cards() >= 0 or comp_hand.num_cards() >= 0:
                        player_scopas += 1

            elif turn == "comp":
                comp_tricks = get_tricks(comp_hand, table)
                comp_trick = play_comp_trick(comp_tricks, table, comp_hand, comp_pile)
                t_str = f"Hand: {comp_trick[0]}{comp_trick[1]}, Table: "
                for t in comp_trick[2]:
                    t_str = t_str + f"{t[0]}{t[1]}, "
                tricks = []

                scopacheck = ""
                if table.num_cards() == 0:
                    if player_hand.num_cards() >= 0 or comp_hand.num_cards() >= 0:
                        comp_scopas += 1
                        scopacheck = "Scopa!"

                prompt = f"COMP played {t_str}. {scopacheck}\nhit ENTER to continue"
                options = 'Continue Game'

                _ = render_screen(stdcsr, player_hand, comp_hand, table, tricks, prompt, options, player_score, comp_score)


            turn = "comp" if turn == "player" else "player"
            # deal a new hand of cards when needed
            if player_hand.num_cards() == 0 and comp_hand.num_cards() == 0:
                if deck.num_cards() < 6: # if insufficient cards to deal, end round
                    break
                else:
                    deck.deal_from_top(player_hand, 3)
                    deck.deal_from_top(comp_hand, 3)
        

        # score round given returned scopas, decks of both players verbosely
        prompt = score_piles(player_pile, comp_pile, player_scopas, comp_scopas, player_score, comp_score)
        options = 'Continue Game'
        _ = render_screen(stdcsr, player_hand, comp_hand, table, tricks, prompt, options, player_score, comp_score)

        # if score of player/cpu surpasses 11, declare winner.
        if player_score >= 11:
            print("player wins!")
            # handle player win
        elif comp_score >= 11:
            print("comp wins!")
            # handle comp win
        # prompt for replay
        player_hand.deal_all(deck)
        player_pile.deal_all(deck)
        comp_hand.deal_all(deck)
        comp_pile.deal_all(deck)



    
   
