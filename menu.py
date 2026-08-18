import curses
import time
import numpy as np
from card import Card
from deck import Deck


def render_screen(stdcsr, player, comp, table, tricks, prompt: str, options: dict):
    idx = 0
    keys = options
    curses.curs_set(0)
    stdcsr.clear()
    screen_height, screen_width = stdcsr.getmaxyx()


    card_height = 7
    card_length = 7
    screen_margin = 1
 

    # render comp hand
    if comp.hand.num_cards() * (card_length+1) > screen_width: # compact view
        stepsize = 3 # needed for |SN on side of card
    else: # full view
        stepsize = card_length+1

    card_x = screen_margin + stepsize

    for card in comp.hand.cards:
        card_y = screen_margin
        for line in card.card_image(back=True):
            stdcsr.addstr(card_y, card_x, line, curses.color_pair(5))
            card_y += 1
        card_x += stepsize


    # render table - 5x2 grid
    stepsize = card_length+1
    grid_width = 5
    card_x_init = screen_margin

    for n, card in enumerate(table.cards):
        card_y = screen_margin + 2*stepsize + card_height * (n//grid_width - 1)-1 # n//5 to add to next row
        card_x = card_x_init + stepsize * (n % grid_width)

        for line in card.card_image():
            stdcsr.addstr(card_y, card_x, line, curses.color_pair(card.color))
            card_y += 1

    # render player hand
    if player.hand.num_cards() * (card_length+1) > screen_width: # compact view
        stepsize = 3 # needed for |SN on side of card
    else: # full view
        stepsize = card_length+1

    card_x = screen_margin + stepsize

    for card in player.hand.cards:
        card_y = screen_margin + 3* stepsize
        for line in card.card_image():
            stdcsr.addstr(card_y, card_x, line, curses.color_pair(card.color))
            card_y += 1
        card_x += stepsize
   
    # render dividers
    stepsize = card_height + 1
    y_stops = [0, screen_margin + card_height, screen_margin + 2*stepsize+card_height, screen_margin + 3*stepsize + card_height ]
    x_stops = [0, screen_margin + 5*stepsize]
    for w in range(screen_width):
        for h in range(screen_height):
            if h in y_stops and w in x_stops:
                stdcsr.addstr(h,w,"+")
            elif h in y_stops:
                stdcsr.addstr(h,w,"-")
            elif w in x_stops:
                stdcsr.addstr(h,w,"|")

    # render labels
    lbl = f" Player - Score: {player.score}, Opponent - Score: {comp.score} "
    stdcsr.addstr(0, (screen_width - len(lbl))//2, lbl, curses.color_pair(2))


    # render player prompt
    if len(keys) < 1:
        return ""
    prompt_x = screen_margin + 5*stepsize + 1
    prompt_y = screen_margin + stepsize
    for subprompt in prompt.split("\n"):
        try:
            stdcsr.addstr(prompt_y,prompt_x,subprompt)
        except:
            raise ValueError(f"{prompt}\n{prompt_y}\n{prompt_x}")
        prompt_y += 1

    # render and wait for options
    while True:
        for i, label in enumerate(tricks):
            marker = ">" if i == idx else " "
            color = 2 if i == idx else 6
            stdcsr.addstr(prompt_y+i+1,prompt_x, f"{marker} {label}", curses.color_pair(color))

        key = stdcsr.getch()
        if key == curses.KEY_UP and len(keys) > 1:
            idx = (idx - 1) % len(keys)
        elif key == curses.KEY_DOWN and len(keys) > 1:
            idx = (idx + 1) % len(keys)
        elif key in (curses.KEY_ENTER, ord("\n")):
            label = keys[idx]
            return options[idx]



