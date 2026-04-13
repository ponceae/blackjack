"""
This file creates a standard 52-card deck represented as a list. It also contains 
functionality for shuffling a deck with the same characteristics.

Author: Adrien P.
"""

import random

from .card import Card
from .constants import CARD_RANKS, CARD_SUITS
		
def create_deck() -> list[Card]:
	"""
	 Create and return a 52-card deck as a list.

	Returns:
		list[Card]: The deck of cards.
	"""
	deck = []		
	for suit in CARD_SUITS:
		for rank in CARD_RANKS:
			deck.append(Card(suit, rank))
	return deck
	# return [Card(rank, suit) for suit in CARD_SUITS for rank in CARD_RANKS]
		
def shuffle_deck(deck: list) -> list[Card]:
	"""
	 Shuffle and return the `deck`.

	Args:
		deck (list): The list of Card objects to shuffle.

	Returns:
		list[Card]: The deck of cards.
	"""
	for i in range(len(deck) - 1, 0, -1):
		seed = random.randint(0, i)
		deck[i], deck[seed] = deck[seed], deck[i]
	return deck
		