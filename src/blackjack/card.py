"""
Define the Card class for representing a single playing card.

Author: Adrien P.
"""

from .constants import (
    DEFAULT_ACE_VALUE, 
    CARD_SUITS, 
    CARD_SUIT_SYMBOLS, 
    FACE_CARD_VALUE, 
    NAMED_CARD_RANKS,
)

class Card:
	"""Represent a single playing card with rank and suit."""

	def __init__ (self, suit: str, rank: int | str):
		"""
		Initialize a Card with a given rank and suit.

		Args:
			suit (str): The suit of the card ('Clubs', 'Diamonds', 'Hearts', 'Spades').
			rank (int | str): The rank of the card. (2-10, 'Jack', 'Queen', 'King', 
				'Ace').
		"""
		if isinstance(suit, str) and suit.capitalize() in CARD_SUITS:
			self.suit = suit.capitalize()
		else:
			raise ValueError('Invalid Suit, Usage: Clubs, Diamonds, Hearts, Spades')
		if isinstance(rank, int) and (2 <= rank <= 11):
			self.rank = rank
		elif isinstance(rank, str) and rank.capitalize() in NAMED_CARD_RANKS:
			self.rank = rank.capitalize()
		else:
			raise ValueError('Invalid Rank, Usage: 2-10, Jack, King, Queen, Ace')
	
	def get_rank_value(self):
		"""
		Return the rank value of the Card.

		Returns:
			int: The card's rank value.
		"""
		if isinstance(self.rank, int):
			return self.rank
		elif isinstance(self.rank, str):
			if self.rank != 'Ace':
				# Value of 10
				return FACE_CARD_VALUE 
			else:
				# Value of 11
				return DEFAULT_ACE_VALUE 
		return 0
	
	def to_string(self):
		"""
		Return the string representation of the card.

		Returns:
			str: The string representation (e.g., ♦5).
		"""
		return f'{CARD_SUIT_SYMBOLS[self.suit]}{str(self.rank)}'
		