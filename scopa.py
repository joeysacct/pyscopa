import random
import curses
from deck import Deck
from card import Card
from player import Player
from menu import render_screen
from score import score_piles

PIPE_SETS = [
    "┃━┏┓┗┛",
    "│─╭╮╰╯",
    "│─┌┐└┘",
    "║═╔╗╚╝",
    "╿╼┍┑┕┚",
]

def run_scopa(stdcsr):
    repeat_game = True
    pipe_set = 0
    # instantiate deck
    deck = Deck()
    deck.populate_deck()

    # add players
    player = Player("Player")
    comp = Player("COMP", player_type='comp')
    players = [player, comp]

    while repeat_game:
        # shuffle deck
        deck.shuffle()
        # set table, hand, score
        table = Deck()

        # decide who goes first 
        current_player_idx = random.choice(range(len(players)))

        # deal cards
        deck.deal_from_top(table, 4)
        deck.deal_from_top(player.hand, 3)
        deck.deal_from_top(comp.hand, 3)

        while deck.num_cards() > 0: 
            current_player = players[current_player_idx]
            current_player_idx = (current_player_idx + 1) % len(players)
            next_player = players[current_player_idx]

            current_player.run_scopa_turn(stdcsr, table, next_player)

            current_player = next_player # pass turn

            # deal a new hand of cards when needed
            if sum([p.hand.num_cards() for p in players]) == 0: #if all players are out of cards
                if deck.num_cards() < 3*len(players): # end round when no cards remain
                    break
                else:
                    for p in players:
                        deck.deal_from_top(p.hand, 3)
        

        # score round given returned scopas, decks of both players verbosely
        prompt = score_piles(players)
        tricks = []
        options = 'Continue Game'
        _ = render_screen(stdcsr, current_player, next_player, table, tricks, prompt, options)

        # if score of player surpasses 11, declare winner.
        max_score = max([p.score for p in players])
        winning_players = [p for p in players if p.score == max_score and p.score >= 11]
        if len(winning_players) == 1:
            winner = winning_players[0]
            prompt = f'{winner.name} wins! Would you like to play again?'
            tricks = ["Yes", "No"]
            options = ["Yes", "No"]
            response = render_screen(stdcsr, current_player, next_player, table, tricks, prompt, options)
            if response == "No":
                exit()
            else:
                for p in players:
                    p.score = 0

        for p in players: # redeal back to deck
            p.return_cards_to_deck(deck)



    
   
