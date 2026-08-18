from deck import Deck
from card import Card
from player import Player

def score_piles(players, suits=[ "Coins", "Cups", "Swords", "Batons" ]):
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
    output.append(", and ".join([f"{p.name} got {p.scopas} Scopas" for p in players]) + ".")
    for p in players:
        p.score += p.scopas
        p.scopas = 0

    # Capture count
    max_captures = max([p.capture_pile.num_cards() for p in players])
    winning_players = [p for p in players if p.capture_pile.num_cards() == max_captures]

    if len(winning_players) == 1:
        winner = winning_players[0]
        winner.score += 1
        output.append(f"{winner.name} captured the most cards, and earns a point.")


    # Coin count
    max_coins = max([len(p.capture_pile.cards_with_suit("Coins")) for p in players])
    winning_players = [p for p in players if len(p.capture_pile.cards_with_suit("Coins")) == max_coins]

    if len(winning_players) == 1:
        winner = winning_players[0]
        winner.score += 1
        output.append(f"{winner.name} captured the most coins, and earns a point.")

    # seven of coins 
    for p in players:
        if p.capture_pile.has_card("Coins", "7"):
           p.score += 1
           output.append(f"{p.name} captured the 7 of Coins, and earns a point.")

    # primiera
    for p in players:
        for suit in suits:
           highest_player_card = max(p.capture_pile.cards_with_suit(suit), key=lambda card: primiera_values[card.value], default=0)
           if highest_player_card == 0: # if players does not have a card of this suit
               p.primiera = 0
               break
           p.primiera += primiera_values[highest_player_card.value]

    max_primiera = max([p.primiera for p in players])
    winning_players = [p for p in players if p.primiera == max_primiera]

    if len(winning_players) == 1:
        winner = winning_players[0]
        winner.score += 1
        output.append(f"{winner.name} had the highest primiera of {winner.primiera},\nand earns a point.")

    output.append(", ".join([f"{p.name} has {p.score} points" for p in players]) + ".")
    return "\n".join(output)
