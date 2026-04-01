"""
Tests some blackjack methods from blackjack.py

@author Adrien P.
@version 2.24.26
"""

from blackjack.helper import can_split, get_hand_value, get_soft_value, is_split_aces, is_soft
from blackjack.utilities import hit_hand, init_deal
from blackjack.card import Card

def test_is_split_aces():
	h1 = [Card('Spades', 'Ace'), Card('Hearts', 'Ace')]
	h2 = [Card('Spades', 5), Card('Hearts', 'Ace')]
	h3 = [Card('Spades', 'Ace'), Card('Hearts', 'King')]
	
	assert is_split_aces(h1) == True
	assert is_split_aces(h2) == False
	assert is_split_aces(h3) == False

def test_can_split():
	h1 = [Card('Spades', 5), Card('Hearts', 5)]
	h2 = [Card('Spades', 10), Card('Hearts', 10)]
	h3 = [Card('Spades', 'King'), Card('Hearts', 'King')]
	h4 = [Card('Spades', 'Queen'), Card('Hearts', 'Queen')]
	h5 = [Card('Spades', 'Jack'), Card('Hearts', 'Jack')]
	h6 = [Card('Spades', 'Ace'), Card('Hearts', 'Ace')]
	h7 = [Card('Spades', 3), Card('Hearts', 3)]

	assert can_split(h1) == True
	assert can_split(h2) == True
	assert can_split(h3) == True
	assert can_split(h4) == True
	assert can_split(h5) == True
	assert can_split(h6) == True
	assert can_split(h7) == True
	
	h8 = [Card('Spades', 5), Card('Hearts', 7)]
	h9 = [Card('Spades', 10), Card('Hearts', 'Queen')]
	h10 = [Card('Spades', 'Queen'), Card('Hearts', 'Jack')]
	h11 = [Card('Spades', 'Jack'), Card('Hearts', 'King')]
	h12 = [Card('Spades', 'King'), Card('Hearts', 'Queen')]
	h13 = [Card('Spades', 'King'), Card('Hearts', 'Ace')]
	h14 = [Card('Spades', 10), Card('Hearts', 5)]
	h15 = [Card('Spades', 'Ace'), Card('Hearts', 2)]
	h16 = [Card('Spades', 'Jack'), Card('Hearts', 'Ace')]
	
	assert can_split(h8) == False
	assert can_split(h9) == False
	assert can_split(h10) == False
	assert can_split(h11) == False
	assert can_split(h12) == False
	assert can_split(h13) == False
	assert can_split(h14) == False

def test_get_soft_value():
	h = [Card('Spades', 'Ace'), Card('Hearts', 6)]
	
	assert get_soft_value(h) == 7
	assert get_hand_value(h) == 17
	assert is_soft(h) == True
	
	h1 = [Card('Spades', 'Ace'), Card('Hearts', 5), 
			Card('Clubs', 'Ace')]
	
	assert get_soft_value(h1) == 7
	assert get_hand_value(h1) == 17
	assert is_soft(h1) == True
	
	"""
	--------------------------------------------------------------------
	Tests for one ace and 2 cards
	--------------------------------------------------------------------
	"""
	h2 = [Card('Spades', 'Ace'), Card('Hearts', 2), 
			Card('Clubs', 3)]
	
	assert get_soft_value(h2) == 6
	assert get_hand_value(h2) == 16
	assert is_soft(h2) == True
	
	h3 = [Card('Spades', 'Ace'), Card('Hearts', 2), 
			Card('Clubs', 4)]
			
	assert get_soft_value(h3) == 7
	assert get_hand_value(h3) == 17
	assert is_soft(h3) == True
	
	"""
	--------------------------------------------------------------------
	Test for 3 ace soft hand
	--------------------------------------------------------------------
	"""
	h4 = [Card('Spades', 'Ace'), Card('Hearts', 'Ace'), 
			Card('Clubs', 'Ace'), Card('Diamonds', 4)]
			
	assert get_soft_value(h4) == 7
	assert get_hand_value(h4) == 17
	assert is_soft(h4) == True
	
	"""
	--------------------------------------------------------------------
	Test for a hand with all of the ace's in a deck
	--------------------------------------------------------------------
	"""
	h5 = [Card('Spades', 'Ace'), Card('Hearts', 'Ace'), 
			Card('Clubs', 'Ace'), Card('Diamonds', 'Ace'),
			Card('Spades', 2)]
			
	assert get_soft_value(h5) == 6
	assert get_hand_value(h5) == 16
	assert is_soft(h5) == True
	
	"""
	--------------------------------------------------------------------
	Test hard hands
	--------------------------------------------------------------------
	"""
	h6 = [Card('Spades', 'Ace'), Card('Clubs', 6), 
			Card('Clubs', 5)]
			
	assert get_hand_value(h6) == 12
	assert get_soft_value(h6) == 12
	assert is_soft(h6) == False
	
	h8 = [Card('Spades', 'Ace'), Card('Clubs', 5), 
			Card('Clubs', 8)]
			
	assert get_hand_value(h8) == 14
	assert get_soft_value(h8) == 14
	assert is_soft(h8) == False
	
	h9 = [Card('Spades', 'Ace'), Card('Clubs', 9), 
			Card('Clubs', 9)]
			
	assert get_hand_value(h9) == 19
	assert get_soft_value(h9) == 19
	assert is_soft(h9) == False
	
	h10 = [Card('Spades', 'Ace'), Card('Clubs', 9), 
			Card('Clubs', 5)]
			
	assert get_hand_value(h10) == 15
	assert get_soft_value(h10) == 15
	assert is_soft(h10) == False
	
	h11 = [Card('Spades', 'Ace'), Card('Clubs', 'Queen'), 
			Card('Clubs', 10)]
			
	assert get_hand_value(h11) == 21
	assert get_soft_value(h11) == 21
	assert is_soft(h11) == False
	
#----------------------------------------------------------------------------------------#

def test_init_deal():
	"""
	--------------------------------------------------------------------
	Tests for all empty deck
	--------------------------------------------------------------------
	"""
	deck = []
	h1, h2 = [], []
	
	init_deal(h1, h2, deck)
	
	assert len(deck) == 48
	assert len(h1) == 2
	assert len(h2) == 2

	"""
	--------------------------------------------------------------------
	Tests with only one card in the deck
	--------------------------------------------------------------------
	"""
	deck2 = [Card('Spades', 5)]
	h3, h4 = [], []
	
	init_deal(h3, h4, deck2)
	
	assert len(deck2) == 49
	assert len(h3) == 2
	assert len(h4) == 2
	
	"""
	--------------------------------------------------------------------
	Tests with only two cards in the deck
	--------------------------------------------------------------------
	"""
	deck3 = [Card('Spades', 5), Card('Diamonds', 4)]
	h5, h6 = [], []
	
	init_deal(h5, h6, deck3)
	
	assert len(deck3) == 50
	assert len(h5) == 2
	assert len(h6) == 2
	
	"""
	--------------------------------------------------------------------
	Tests with only three cards in the deck
	--------------------------------------------------------------------
	"""
	deck4 = [Card('Spades', 5), Card('Diamonds', 4),
		Card('Clubs', 10)]
	h7, h8 = [], []
	
	init_deal(h7, h8, deck4)
	
	assert len(deck4) == 51
	assert len(h7) == 2
	assert len(h8) == 2
	
	"""
	--------------------------------------------------------------------
	Normal test that has four cards in the deck
	--------------------------------------------------------------------
	"""
	deck5 = [Card('Spades', 5), Card('Diamonds', 4),
		Card('Clubs', 10), Card('Hearts', "King")]
	h9, h10 = [], []
	
	init_deal(h9, h10, deck5)
	
	assert len(deck5) == 0
	assert len(h9) == 2
	assert len(h10) == 2
	
	"""
	--------------------------------------------------------------------
	For good measure, reuse variable deck5 and ensure that it creates a 
	new deck and pulls 4 cards.
	--------------------------------------------------------------------
	"""
	h11, h12 = [], []
	init_deal(h11, h12, deck5)
	
	assert len(deck5) == 48
	assert len(h11) == 2
	assert len(h12) == 2	

#----------------------------------------------------------------------------------------#

def test_hit_hand():
	"""
	--------------------------------------------------------------------
	Normal Deck Hit
	--------------------------------------------------------------------
	"""
	deck = [Card('Spades', 'Ace'), Card('Hearts', 7), 
		Card('Clubs', 'King'), Card('Diamonds', 10)]
	hand = [Card('Spades', 6), Card('Hearts', 4)]
	hit_hand(hand, deck) 
	
	assert len(deck) == 3
	assert len(hand) == 3
	
	"""
	--------------------------------------------------------------------
	Hitting On An Empty Deck
	--------------------------------------------------------------------
	"""
	deck = []
	hand = [Card('Spades', 6), Card('Hearts', 4)]
	hit_hand(hand, deck)
	
	assert len(deck) == 51
	assert len(hand) == 3

#----------------------------------------------------------------------------------------#

def test_get_total_hand_val():
	"""
	--------------------------------------------------------------------
	Main Ace Card Handling
	--------------------------------------------------------------------
	"""
	a = [Card('Hearts', 'Ace'), Card('Spades', 9)]
	b = [Card('Spades', 'Ace'), Card('Clubs', 'King')]
	c = [Card('Diamonds', 'Ace'), Card('Hearts', 9), 
		Card('Diamonds', 5)]
	
	assert get_hand_value(a) == 20
	assert get_hand_value(b) == 21
	assert get_hand_value(c) == 15

	"""
	--------------------------------------------------------------------
	Multiple Ace Card Handling
	--------------------------------------------------------------------
	"""
	a = [Card('Hearts', 'Ace'), Card('Spades', 'Ace')]
	b = [Card('Spades', 'Ace'), Card('Clubs', 'Ace'), 
		Card('Diamonds', 9)]
	c = [Card('Spades', 'Ace'), Card('Diamonds', 'Ace'), 
		Card('Spades', 9), Card('Diamonds', 9)]
	d = [Card('Hearts', 'Ace'), Card('Clubs', 'Ace'), 
		Card('Diamonds', 'Ace')]
	e = [Card('Hearts', 'Ace'), Card('Clubs', 'Ace'), 
		Card('Diamonds', 'Ace'), Card('Hearts', 9)]
	f = [Card('Hearts', 'Ace'), Card('Spades', 'Ace'),
		Card('Hearts', 8)]
	
	assert get_hand_value(a) == 12
	assert get_hand_value(b) == 21
	assert get_hand_value(c) == 20
	assert get_hand_value(d) == 13
	assert get_hand_value(e) == 12
	assert get_hand_value(f) == 20

	"""
	--------------------------------------------------------------------
	Face Card Handling
	--------------------------------------------------------------------
	"""
	a = [Card('Hearts', 'Jack'), Card('Hearts', 'Queen')]
	b = [Card('Hearts', 'King'), Card('Hearts', 9),
		Card('Hearts', 2)]
	c = [Card('Hearts', 'Queen'), Card('Hearts', 'King'),
		Card('Hearts', 2)]
	
	assert get_hand_value(a) == 20
	assert get_hand_value(b) == 21
	assert get_hand_value(c) == 22
	
	"""
	--------------------------------------------------------------------
	Hand Bust Edge Cases
	--------------------------------------------------------------------
	"""
	a = [Card('Hearts', 10), Card('Hearts', 9),
		Card('Hearts', 3)]
	b = [Card('Hearts', 'Ace'), Card('Hearts', 9),
		Card('Spades', 9), Card('Diamonds', 2)]
	c = [Card('Hearts', 'Ace'), Card('Hearts', 9),
		Card('Spades', 9), Card('Hearts', 5)]
	
	assert get_hand_value(a) == 22
	assert get_hand_value(b) == 21	
	assert get_hand_value(c) == 24
	
	"""
	--------------------------------------------------------------------
	Blackjack vs. Normal 21 detection (Will be important later)
	--------------------------------------------------------------------
	"""
	a = [Card('Hearts', 'Ace'), Card('Hearts', 'King')]
	b = [Card('Hearts', 10), Card('Hearts', 'Ace')]
	c = [Card('Hearts', 'Ace'), Card('Hearts', 9),
		Card('Spades', 'Ace')]
	d = [Card('Hearts', 7), Card('Clubs', 7),
		Card('Diamonds', 7)]
	e = [Card('Hearts', 'Ace'), Card('Hearts', 5),
		Card('Spades', 5), Card('Hearts', 10)]	
		
	assert get_hand_value(a) == 21 # blackjack
	assert get_hand_value(b) == 21 # blackjack
	assert get_hand_value(c) == 21 # hand 21 win
	assert get_hand_value(d) == 21 # hand 21 win
	assert get_hand_value(e) == 21 # hand 21 win 
	
	"""
	--------------------------------------------------------------------
	Soft vs. Hard Hands -> Will be important later
	--------------------------------------------------------------------
	"""
	a = [Card('Diamonds', 'Ace'), Card('Spades', 6)]
	b = [Card('Spades', 'Ace'), Card('Hearts', 6),
		Card('Diamonds', 10)]
	c = [Card('Spades', 'Ace'), Card('Spades', 7)]
	d = [Card('Spades', 'Ace'), Card('Spades', 7),
		Card('Spades', 5)]
	
	assert get_hand_value(a) == 17 # soft 17
	assert get_hand_value(b) == 17 # hard 17
	assert get_hand_value(c) == 18 # soft 18
	assert get_hand_value(d) == 13 # hard 13

	"""
	--------------------------------------------------------------------
	Winning hands > len(2)
	--------------------------------------------------------------------
	"""
	a = [Card('Spades', 'Ace'), Card('Spades', 'King')]
	b = [Card('Spades', 7), Card('Clubs', 7),
		Card('Hearts', 7)]
	c = [Card('Clubs', 5), Card('Hearts', 5),
		Card('Diamonds', 5), Card('Spades', 6)]
		
	assert get_hand_value(a) == 21
	assert get_hand_value(b) == 21	
	assert get_hand_value(c) == 21	
	