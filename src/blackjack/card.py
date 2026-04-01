"""
This file contains the functionality for creating a standard 52-card deck.

@author Adrien P.
@version 3.16.26
"""

from .constants import DEFAULT_ACE_VALUE, CARD_SUITS, CARD_SUIT_SYMBOLS, FACE_CARD_VALUE, NAMED_CARD_RANKS

class Card:
	
	def __init__ (self, suit, rank):
		if isinstance(suit, str) and suit.capitalize() in CARD_SUITS: # Verify suit value
			self.suit = suit.capitalize()
		else:
			raise ValueError('Invalid Suit. Clubs, Diamonds, Hearts, Spades')
		if isinstance(rank, int) and (2 <= rank <= 11):
			self.rank = rank
		elif isinstance(rank, str) and rank.capitalize() in NAMED_CARD_RANKS:
			self.rank = rank.capitalize()
		else:
			raise ValueError('Invalid Rank. 2-11, Jack, King, Queen, Ace')
	
	def get_rank_value(self):
		if isinstance(self.rank, int):
			return self.rank
		elif isinstance(self.rank, str):
			if self.rank != 'Ace':
				return FACE_CARD_VALUE # Value of 10
			else:
				return DEFAULT_ACE_VALUE # Value of 11

	def get_suit(self):
		return self.suit

	def to_string(self):
		return CARD_SUIT_SYMBOLS[self.suit] + str(self.rank) 
		