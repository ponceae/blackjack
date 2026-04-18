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
	return [Card(suit, rank) for suit in CARD_SUITS for rank in CARD_RANKS]
		
def shuffle_deck(deck: list[Card]) -> list[Card]:
	"""
	 Shuffle and return the `deck`.

	Args:
		deck (list[Card]): The list of Card objects to shuffle.

	Returns:
		list[Card]: The deck of cards.
	"""
	for i in range(len(deck) - 1, 0, -1):
		j = random.randint(0, i)
		deck[i], deck[j] = deck[j], deck[i]
	return deck
		