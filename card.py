import curses
import random
import numpy as np


class Card():
    def __init__(self, chrset, suit, suit_chr, value, value_chr, owner="Deck"):
        self.suit = suit
        self.value = value
        self.suit_chr = suit_chr
        self.value_chr = value_chr
        self.chrset = chrset
        self.owner = owner

    def name(self):
        return f"{self.value} of {self.suit}"

    def card_image(self, back=False):
        card_txt = []
        corner_txt = self.value_chr + self.suit_chr
        card_txt.append(self.chrset[2] + self.chrset[1] * 5 + self.chrset[3])      # '┏━━━━━┓'
        if back:
            for line in self.get_card_deco(back):
                card_txt.append(self.chrset[0] + line + self.chrset[0])
        else:
            card_txt.append(self.chrset[0] + corner_txt + "   " + self.chrset[0]) # '┃NS   ┃'
            for line in self.get_card_deco(back):
                card_txt.append(self.chrset[0] + line + self.chrset[0])
            card_txt.append(self.chrset[0] + "   " + corner_txt + self.chrset[0]) # '┃   NS┃'
        card_txt.append(self.chrset[4] + self.chrset[1] * 5 + self.chrset[5])      # '┗━━━━━┛
        return card_txt

    def get_card_deco(self, back):
        s = self.suit_chr
        s0 = f"     "
        s1 = f"  {s}  "
        s2 = f" {s} {s} "
        s3 = f"{s} {s} {s}"
        s4 = f"{s}{s} {s}{s}"
        decos = {
            "A": [s0,s1,s0],
            "2": [s1,s0,s1],
            "3": [s2,s0,s1],
            "4": [s2,s0,s2],
            "5": [s2,s1,s2],
            "6": [s2,s2,s2],
            "7": [s2,s3,s2],
            "8": [s3,s2,s3],
            "9": [s3,s3,s3],
            "10": [s3,s4,s3],
            "J": [
                "   ww",
                "   {)",
                "  \% ",
            ],
            "Q": [
                "   ww",
                "   {(",
                "  |%%",
            ],
            "K": [
                "   WW",
                "   {)",
                "  \%%",
            ],
        }
        if back:
            return [
                "/ ~ \\",
                "}}:{{",
                "}}:{{",
                "}}:{{",
                "\\ ~ /",
            ]
        return decos[self.value_chr]


PIPE_SETS = [
    "┃━┏┓┗┛",
    "│─╭╮╰╯",
    "│─┌┐└┘",
    "║═╔╗╚╝",
    "╿╼┍┑┕┚",
]


if __name__ == "__main__":
    cardtest = Card(PIPE_SETS[0],"Coins", "o", "Seven", "7") 

    print(cardtest.name())
    for line in cardtest.card_image():
        print(line)
    for line in cardtest.card_image(back=True):
        print(line)
