import curses
import time
import numpy as np
from card import Card
from deck import Deck


def render_screen(stdcsr, player_hand, comp_hand, table, tricks, prompt: str, options: dict, player_score, comp_score):
    idx = 0
    keys = options
    curses.curs_set(0)
    stdcsr.clear()
    screen_height, screen_width = stdcsr.getmaxyx()


    card_height = 7
    card_length = 7
    screen_margin = 2

    # render player hand
    if player_hand.num_cards() * (card_length+1) > screen_width: # compact view
        stepsize = 3 # needed for |SN on side of card
    else: # full view
        stepsize = card_length+1

    card_x = screen_width//2 - stepsize*player_hand.num_cards() + card_length//2

    for card in player_hand.cards:
        card_y = screen_height - screen_margin - card_height
        for line in card.card_image():
            stdcsr.addstr(card_y, card_x, line)
            card_y += 1
        card_x += stepsize
    

    # render comp hand
    if comp_hand.num_cards() * (card_length+1) > screen_width: # compact view
        stepsize = 3 # needed for |SN on side of card
    else: # full view
        stepsize = card_length+1

    card_x = screen_width//2 - stepsize*comp_hand.num_cards() + card_length//2

    for card in comp_hand.cards:
        card_y = screen_margin
        for line in card.card_image(back=True):
            stdcsr.addstr(card_y, card_x, line)
            card_y += 1
        card_x += stepsize


    # render table - 5x2 grid
    stepsize = 8
    grid_width = 5
    card_x_init = screen_width//2 - (stepsize*grid_width//2) + card_length//2

    for n, card in enumerate(table.cards):
        card_y = screen_height//2 + card_height * (n//grid_width - 1) # n//5 to add to next row
        card_x = card_x_init + stepsize * (n % grid_width)

        for line in card.card_image():
            stdcsr.addstr(card_y, card_x, line)
            card_y += 1

    
    # render player tricks
    # n_tricks = len(tricks)
    # stdcsr.addstr(screen_height//2 - n_tricks+8, screen_margin, "Available Tricks:")
    # stdcsr.addstr(screen_height//2 - n_tricks+9, screen_margin, "-----------------")
    # for i,trick in enumerate(tricks):
    #     # t_str = f"{trick[0]}{trick[1]}, "
    #     # for t in trick[2]:
    #     #     # raise ValueError(f"{t}")
    #     #     t_str = t_str + f"{t[0]}{t[1]}, "
    #     stdcsr.addstr(screen_height//2 - n_tricks+i+10, screen_margin,trick)

   
    # render player prompt
    if len(keys) < 1:
        return ""
    longest_label = max(map(len, "\n".split(prompt))) + 1
    prompt_x = screen_margin 
    prompt_y = screen_height//2 + 10
    try:
        stdcsr.addstr(prompt_y-1,prompt_x,prompt)
    except:
        raise ValueError(f"{prompt}\n{prompt_y}\n{prompt_x}")
    prompt_y += prompt.count("\n")

    # render and wait for options
    while True:
        for i, label in enumerate(tricks):
            marker = ">" if i == idx else " "
            stdcsr.addstr(prompt_y+i+2,prompt_x, f"{marker} {label}")

        key = stdcsr.getch()
        if key == curses.KEY_UP:
            idx = (idx - 1) % len(keys)
        elif key == curses.KEY_DOWN:
            idx = (idx + 1) % len(keys)
        elif key in (curses.KEY_ENTER, ord("\n")):
            label = keys[idx]
            return options[idx]



