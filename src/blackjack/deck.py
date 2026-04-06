"""
This file creates a standard 52-card deck represented as a list. It also contains 
functionality for shuffling a deck with the same characteristics.

@author: Adrien P.
@version: 4.3.26
"""

import random

from .card import Card
from .constants import CARD_RANKS, CARD_SUITS

"""
Creates a and returns a standard 52-card deck as a list.
"""		
def create_deck():
	deck = []		
	for suit in CARD_SUITS:
		for rank in CARD_RANKS:
			deck.append(Card(suit, rank))
	return deck
	
"""
Shuffles and returns the deck of cards as a list.

Uses a variation of the Fisher-Yates shuffle algorithm. 
Reference Link: https://en.wikipedia.org/wiki/Fisher%E2%80%93Yates_shuffle
"""	
def shuffle_deck(deck: list):
	for i in range(len(deck) - 1, 0, -1):
		seed = random.randint(0, i)
		deck[i], deck[seed] = deck[seed], deck[i]
	return deck
		