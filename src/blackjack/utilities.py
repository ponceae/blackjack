"""
Card and deck getters & setters for blackjack.

Also contains CLI modification functions.

@author: Adrien P.
@version: 3.23.26
"""

import subprocess
import time

from .constants import ACE_ALT_VALUE, DEFAULT_ACE_VALUE, TIMER_MESSAGES
from .deck import create_deck, shuffle_deck

"""
Clears the CLI.
"""
def clear_terminal():
	subprocess.run('cls', shell=True)

"""
Copies a new 52-card deck to an empty deck.
"""
def copy_deck(old_deck: list, new_deck: list):
	old_deck[:] = new_deck

"""
Returns a newly created and shuffled deck of cards.
"""
def create_and_shuffle():
	return shuffle_deck(create_deck()) # from deck.py

"""  
Creates two separate hands for the player.
"""
def create_split_hands(player_hand, game_deck):
	"""Player will only be able to split once, so we can hard code 0"""
	player_hand.append([player_hand[0].pop()])
	for hand in player_hand:
		hit_hand(hand, game_deck)
	
"""
Returns the hard hand value.
"""
def get_hand_value(hand):
	value, ace_count = 0, 0
	for card in hand:
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
Returns the soft hand value.
"""	
def get_soft_value(hand):
	soft_value = 0
	for card in hand:
		if card.rank == 'Ace':
			soft_value += ACE_ALT_VALUE # Alternate ace value is 1
		else:
			soft_value += card.get_rank_value()
	return soft_value

"""
Adds a card to the hand, and creates a new game deck if empty.
"""
def hit_hand(hand, game_deck):
	while True:
		if game_deck:
			hand.append(game_deck.pop())
			break
		print('Game deck is now empty. Recreating deck and reshuffling.')
		copy_deck(game_deck, create_and_shuffle())

"""
Deals cards to the player and dealer.
"""
def initial_round_deal(player_hands, dealer_hand, game_deck):
	player_temp = []
	for i in range(4):
		if not game_deck:
			print('Game deck is now empty. Recreating deck and reshuffling.')
			copy_deck(game_deck, create_and_shuffle())
		card = game_deck.pop()
		if i % 2 == 0:
			player_temp.append(card)
		else:
			dealer_hand.append(card)
	player_hands.append(player_temp)    

"""
Utility timer function for the CLI.
"""
def load_timer(timer_flag_key=-1):
	timer_message = TIMER_MESSAGES.get(timer_flag_key, '{}')
	print()
	for i in range(3, 0, -1):
		print(timer_message.format(i), end='\r')
		time.sleep(1)
		