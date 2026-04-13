"""
Tests for the card class module.

Author: Adrien P.
"""

import pytest

from blackjack.card import Card
from blackjack.constants import FACE_CARD_VALUE, DEFAULT_ACE_VALUE

@pytest.mark.parametrize(
	'raw_suit, raw_rank, expected_suit, expected_rank',
 	[
		('spaDEs', 5, 'Spades', 5),
		('heArTs', 2, 'Hearts', 2),
		('CLUbs', 10, 'Clubs', 10),
  		('DiaMONds', 'acE', 'Diamonds', 'Ace'),
		('SPadEs', 'jaCk', 'Spades', 'Jack'),
		('HEArtS', 'queen', 'Hearts', 'Queen'),
	]
)
def test_init_mismatch_conversion(raw_suit, raw_rank, expected_suit, expected_rank):
    test_card = Card(raw_suit, raw_rank)
    assert test_card.suit == expected_suit
    assert test_card.rank == expected_rank

# C1 = Card('spaDEs', 5)
# C2 = Card('heArTs', 2)
# C3 = Card('CLUbs', 10)
# C4 = Card('DiaMONds', 'acE')
# C5 = Card('SPadEs', 'jaCk')
# C6 = Card('HEArtS', 'queen')
# C7 = Card('Clubs', 'King')

# def test_init_mismatch():	
# 	assert C1.suit == 'Spades'
# 	assert C1.rank == 5
	
# 	assert C2.suit == 'Hearts'
# 	assert C2.rank == 2
	
# 	assert C3.suit == 'Clubs'
# 	assert C3.rank == 10
	
# 	assert C4.suit == 'Diamonds'
# 	assert C4.rank == 'Ace'
	
# 	assert C5.suit == 'Spades'
# 	assert C5.rank == 'Jack'
	
# 	assert C6.suit == 'Hearts'
# 	assert C6.rank == 'Queen'
	
# 	assert C7.suit == 'Clubs'
# 	assert C7.rank == 'King'
	
# def test_init_valueerror_exception():
# 	with pytest.raises(ValueError):
# 		Card(5, 8) # type: ignore 
# 	with pytest.raises(ValueError):
# 		Card('Spades', '5')
# 	with pytest.raises(ValueError):
# 		Card('Hearts', 12)
# 	with pytest.raises(ValueError):
# 		Card('Diamonds', 1)

# def test_get_suit():
# 	assert C1.get_suit() == 'Spades'
# 	assert C2.get_suit() == 'Hearts'
# 	assert C3.get_suit() == 'Clubs'
# 	assert C4.get_suit() == 'Diamonds'
# 	assert C5.get_suit() == 'Spades'
# 	assert C6.get_suit() == 'Hearts'
# 	assert C7.get_suit() == 'Clubs'
	
# def test_get_rank_value():
# 	assert C1.get_rank_value() == 5
# 	assert C2.get_rank_value() == 2
# 	assert C3.get_rank_value() == FACE_CARD_VALUE
# 	assert C4.get_rank_value() == DEFAULT_ACE_VALUE
# 	assert C5.get_rank_value() == FACE_CARD_VALUE
# 	assert C6.get_rank_value() == FACE_CARD_VALUE
# 	assert C7.get_rank_value() == FACE_CARD_VALUE

# def test_to_string():
# 	assert C1.to_string() == '♠5'
# 	assert C2.to_string() == '♥2'
# 	assert C3.to_string() == '♣10'
# 	assert C4.to_string() == '♦Ace'
# 	assert C5.to_string() == '♠Jack'
# 	assert C6.to_string() == '♥Queen'
# 	assert C7.to_string() == '♣King'
	