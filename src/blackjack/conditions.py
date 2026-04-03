"""
Contains the main boolean logic for blackjack.

Also contains CLI output functions.

@author Adrien P.
@version 3.23.26
"""

from .datatypes import Hand, Player, PlayerHand, DealerHand, Table 
from .constants import HIT, NO, ROMAN_NUMERALS, STAND, YES, PLAYER_WIN, DEALER_WIN, PUSH
from .actions import get_hand_value, get_soft_value

"""
Returns true if the hand can be split.
"""
def can_split(hand):
	return hand[0].rank == hand[1].rank

"""
Compares the hands at the start of the round and returns the outcome.
"""
def compare_initial_hands(player_hand, dealer_hand):
	player_blackjack = is_twenty_one(player_hand)
	dealer_blackjack = is_twenty_one(dealer_hand)
	if player_blackjack and dealer_blackjack:
		return PUSH
	elif player_blackjack and not dealer_blackjack:
		return PLAYER_WIN
	elif not player_blackjack and dealer_blackjack:
		return DEALER_WIN

"""
Returns true if the current hand value is greater than 21.
"""	
def is_bust(hand):
	return get_hand_value(hand) > 21

"""
Returns true if the current hand is considered soft.
"""
def is_soft(hand):
	return get_soft_value(hand) != get_hand_value(hand)

"""
Returns true if the hand contains 2 aces.
"""		
def is_split_aces(hand):
	return hand[0].rank == "Ace" and hand[1].rank == "Ace"
		
"""
Returns true if the current hand value equals 21.
"""	
def is_twenty_one(hand):
	return get_hand_value(hand) == 21

""" 
Returns true if the player has enough chips for the requested bet. 
"""
def is_valid_bet_helper(player_bank, wager):
	return wager <= player_bank.get_chip_count()

""" 
Returns true if the chip count is between 15 - 1000 AND is an int or float.
"""            
def verify_chip_bounds(chip_count):
	return isinstance(chip_count, (int, float)) and 15 <= chip_count <= 1000

""" 
Returns true if the player has enough chips to double down/split.
"""
def verify_double_bet(player_bank, wager):
	return wager <= player_bank.get_chip_count()

""" 
Returns true if the player has enough chips for insurance.
"""
def verify_insurance_bet(player_bank, wager): 
	return get_insurance_cost(wager) <= player_bank.get_chip_count()
