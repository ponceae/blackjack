"""
Blackjack game actions and calculations.

This module contains functions to deal cards, manage hands, and 
calculates hand values and payouts.

Author: Adrien P.
"""

from .card import Card
from .constants import ACE_ALT_VALUE, DEFAULT_ACE_VALUE, PLAYER_WIN, PUSH
from .datatypes import (
    DealerHand, 
    Hand, 
    Player, 
    PlayerHand, 
    Table
)
from .deck import create_deck, shuffle_deck
from .payout_calculator import blackjack_payout

# ==========================================
# GAME ACTIONS
# Hand modification & initialization
# ==========================================

def copy_deck(old_deck: list[Card], new_deck: list[Card]):
	"""
	Copy the shuffled `new_deck` into `old_deck`.
	
	Args:
		old_deck (list[Card]): The deck to overwrite.
		new_deck (list[Card]): The deck to copy from.

	Returns:
		None
	"""
	old_deck[:] = new_deck

def create_split_hands(table: Table):
	"""
	Create a new split hand for the player by popping a card from the first initial 
	hand and hitting both hands.
	
	Args: 
		table (Table): The current game table containing the player hands and the deck.

	Returns:
		None
	"""
	popped_card = table.player.hands[0].cards.pop()
	new_hand = PlayerHand(cards=[popped_card])
 
	table.player.hands.append(new_hand)
	for hand in table.player.hands:
		hit_hand(table, hand)
  
def hit_hand(table: Table, hand: Hand):
	"""
	Add a card from the table deck to `hand`. Create and shuffle a new deck if empty.
	
	Args:
		table (Table): The current game table containing the hand and the deck.
		hand (Hand): The hand being modified.
	
	Returns:
		None
	"""
	while True:
		if table.deck:
			hand.cards.append(table.deck.pop())
			break
		print('Deck is empty. Adding cards.')
		copy_deck(table.deck, create_and_shuffle())

def initial_round_deal(table: Table):
	"""
	Create a new player and dealer hand, then deal two cards each.

	Args:
		table (Table): The current game table containing the player, dealer, and deck.

	Returns:
		None
	"""
	table.player.hands = [PlayerHand()]
	table.dealer = DealerHand()
 
	for i in range(4):
		if not table.deck:
			print('Deck is empty. Adding cards.')
			copy_deck(table.deck, create_and_shuffle())
		card = table.deck.pop()
		if i % 2 == 0:
			table.player.hands[0].cards.append(card)
		else:
			table.dealer.cards.append(card)

# ==========================================
# CALCULATIONS
# Evaluates hand values.
# ==========================================

def get_hand_value(hand: Hand):
	"""
	Return the total numeric value of `hand`, contextually counting Aces as a 1 or 11.

	Args:
		hand (Hand): The hand to calculate.

	Returns:
		int: Total numeric value of `hand`.
	"""
	value, ace_count = 0, 0
	for card in hand.cards:
		if card.rank == 'Ace':	
			value += DEFAULT_ACE_VALUE # Default ace value is 11
			ace_count += 1 
		else:
			value += card.get_rank_value()
	while ace_count > 0 and value > 21: 
		value -= DEFAULT_ACE_VALUE
		value += ACE_ALT_VALUE # Alternate ace value is 1
		ace_count -= 1
	return value
	
def get_soft_value(hand: Hand):
	"""
	Return the hand value, treating all Aces as 1 (soft value).
	
	Args: 
		hand (Hand): The hand to calculate.

	Returns:
		int: Numeric value of `hand` when all aces are counted as 1.
	"""
	soft_value = 0
	for card in hand.cards:
		if card.rank == 'Ace':
			soft_value += ACE_ALT_VALUE # Alternate ace value is 1
		else:
			soft_value += card.get_rank_value()
	return soft_value

# ==========================================
# DECK GENERATION
# ==========================================

def create_and_shuffle():
	"""
	Create a new 52-card deck, shuffle it, and return it.
	
	Returns:
		list[Card]: A shuffled deck of cards.
	"""
	return shuffle_deck(create_deck())
		