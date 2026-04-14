"""
Tests for the card class module.

Author: Adrien P.
"""

import pytest

from blackjack.card import Card
from blackjack.constants import CARD_RANKS, CARD_SUITS

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

@pytest.mark.parametrize(
	'rank, suit',
	[
		(rank, suit) for rank in CARD_RANKS for suit in CARD_SUITS
	]
)
def test_all_cards(rank, suit):
	card = Card(suit, rank)
	
	assert card.rank == rank
	assert card.suit == suit

@pytest.mark.parametrize(
	'invalid_suit, invalid_rank, expected_err_msg',
	[
		(5, 8, 'Invalid Suit, Usage: Clubs, Diamonds, Hearts, Spades'),
		('Spades', '5', 'Invalid Rank, Usage: 2-10, Jack, King, Queen, Ace'),
		('Hearts', 12, 'Invalid Rank, Usage: 2-10, Jack, King, Queen, Ace'),
		('Diamonds', 1, 'Invalid Rank, Usage: 2-10, Jack, King, Queen, Ace'),
		('Card', 'Ace', 'Invalid Suit, Usage: Clubs, Diamonds, Hearts, Spades'),
	]
)
def test_init_raises_valueerror_on_invalid_input(
	invalid_suit, invalid_rank, expected_err_msg
):
	with pytest.raises(ValueError, match=expected_err_msg):
		Card(invalid_suit, invalid_rank)

@pytest.mark.parametrize(
	'card, expected_rank_value',
	[
		(Card('Spades', 5), 5),
		(Card('Hearts', 2), 2),
		(Card('Clubs', 10), 10),
		(Card('Diamonds', 'Ace'), 11),
		(Card('Spades', 'Jack'), 10),
		(Card('Clubs', 'Queen'), 10),
		(Card('Hearts', 'King'), 10),
	]
)
def test_get_card_rank_value(card, expected_rank_value):
	assert card.get_rank_value() == expected_rank_value

@pytest.mark.parametrize(
	'card, expected_string',
	[
		(Card('Spades', 5), '♠5'),
		(Card('Hearts', 2), '♥2'),
		(Card('Clubs', 10), '♣10'),
		(Card('Diamonds', 'Ace'), '♦Ace'),
		(Card('Spades', 'Jack'), '♠Jack'),
		(Card('Hearts', 'Queen'), '♥Queen'),
		(Card('Clubs', 'King'), '♣King'),
	]
)
def test_card_to_string(card, expected_string):
	assert card.to_string() == expected_string
