"""
This file creates a standard 52-card deck represented as a list. It also contains 
functionality for shuffling a deck with the same characteristics.

@author: Adrien P.
@version: 3.16.26
"""

import random

from .card import Card
from .constants import CARD_RANKS, CARD_SUITS

"""
Creates a standard 52-card deck.
"""		
def create_deck():
	deck = []		
	for suit in CARD_SUITS:
		for rank in CARD_RANKS:
			deck.append(Card(suit, rank))
	return deck
	
"""
Shuffles the virtual deck of cards.

Uses a variation of the Fisher-Yates shuffle algorithm. 
Reference Link: https://en.wikipedia.org/wiki/Fisher%E2%80%93Yates_shuffle
"""	
def shuffle_deck(curr_deck):
	for i in range(len(curr_deck) - 1, 0, -1):
		seed = random.randint(0, i)
		curr_deck[i], curr_deck[seed] = curr_deck[seed], curr_deck[i]
	return curr_deck
		