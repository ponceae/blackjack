"""
Tests for card.py

@author: Adrien P.
@version: 3.5.26
"""

import pytest
from blackjack.card import Card
from blackjack.constants import FACE_CARD, ACE_VAL

a = Card('spaDEs', 5)
b = Card('heArTs', 2)
c = Card('CLUbs', 10)
d = Card('DiaMONds', 'acE')
e = Card('SPadEs', 'jaCk')
f = Card('HEArtS', 'queen')
g = Card('Clubs', 'King')

def test_init_mismatch():	
	assert a.suit == 'Spades'
	assert a.rank == 5
	
	assert b.suit == 'Hearts'
	assert b.rank == 2
	
	assert c.suit == 'Clubs'
	assert c.rank == 10
	
	assert d.suit == 'Diamonds'
	assert d.rank == 'Ace'
	
	assert e.suit == 'Spades'
	assert e.rank == 'Jack'
	
	assert f.suit == 'Hearts'
	assert f.rank == 'Queen'
	
	assert g.suit == 'Clubs'
	assert g.rank == 'King'
	
def test_init_typeerror_exception():
	with pytest.raises(TypeError):
		Card(5, 8)
	with pytest.raises(TypeError):
		Card('Spades', '5')
	with pytest.raises(TypeError):
		Card('Hearts', 12)
	with pytest.raises(TypeError):
		Card('Diamonds', 1)

def test_get_suit():
	assert a.get_suit() == 'Spades'
	assert b.get_suit() == 'Hearts'
	assert c.get_suit() == 'Clubs'
	assert d.get_suit() == 'Diamonds'
	assert e.get_suit() == 'Spades'
	assert f.get_suit() == 'Hearts'
	assert g.get_suit() == 'Clubs'
	
def test_get_rank_val():
	assert a.get_rank_val() == 5
	assert b.get_rank_val() == 2
	assert c.get_rank_val() == FACE_CARD
	assert d.get_rank_val() == ACE_VAL
	assert e.get_rank_val() == FACE_CARD
	assert f.get_rank_val() == FACE_CARD
	assert g.get_rank_val() == FACE_CARD

def test_to_string():
	assert a.to_string() == '5 of Spades'
	assert b.to_string() == '2 of Hearts'
	assert c.to_string() == '10 of Clubs'
	assert d.to_string() == 'Ace of Diamonds'
	assert e.to_string() == 'Jack of Spades'
	assert f.to_string() == 'Queen of Hearts'
	assert g.to_string() == 'King of Clubs'
	