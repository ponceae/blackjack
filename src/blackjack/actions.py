"""
Blackjack game actions and calculations.

@author: Adrien P.
@version: 4.3.26
"""

from .datatypes import Hand, PlayerHand, DealerHand, Table
from .constants import ACE_ALT_VALUE, DEFAULT_ACE_VALUE
from .deck import create_deck, shuffle_deck
from .card import Card

# ==========================================
# GAME ACTIONS
# Hand modification & initialization
# ==========================================

"""
Copies a new 52-card deck to an empty deck.
"""
def copy_deck(old_deck: list[Card], new_deck: list[Card]):
	old_deck[:] = new_deck

"""  
Adds another hand to the player.
"""
def create_split_hands(table: Table):
	popped_card = table.player.hands[0].cards.pop()
	new_hand = PlayerHand(cards=[popped_card])
 
	table.player.hands.append(new_hand)
	for hand in table.player.hands:
		hit_hand(table, hand)
  
"""
Adds a card to the hand. Creates a new deck when empty.
"""
def hit_hand(table: Table, hand: Hand):
	while True:
		if table.deck:
			hand.cards.append(table.deck.pop())
			break
		print('Deck is empty. Adding cards.')
		copy_deck(table.deck, create_and_shuffle())

"""
Deals cards at the table to the player & dealer.
"""
def initial_round_deal(table: Table):
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

""" 
Updates player chips on an initial push or a blackjack win
"""
def initial_outcome_payout_helper(outcome, player_bank, wager):
	if outcome == PLAYER_WIN:
		payout = blackjack_payout(wager)
		player_bank.add_chips(payout)
	elif outcome == PUSH:
		player_bank.add_chips(wager)

# ==========================================
# CALCULATIONS
# Evaluates hand values.
# ==========================================

"""
Returns the total hand value.
"""
def get_hand_value(hand: Hand):
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

"""
Returns the soft value of the hand.
"""	
def get_soft_value(hand: Hand):
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

"""
Creates and returns a shuffled deck as a list.
"""
def create_and_shuffle():
	return shuffle_deck(create_deck())
		