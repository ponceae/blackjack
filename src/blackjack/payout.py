""" 
Helper functions that handle the buy in, payout or removal of game chips.

@author Adrien P.
@version 4.3.26
"""

import math
from .constants import MIN_BET, NO, PLAYER_WIN, PUSH, YES  

"""
Returns the payout for a natural blackjack win. (3:2 odds, bet * 1.5)
"""
def blackjack_payout(wager):
	return wager * 2.5

""" 
Helper that executes the insurance logic for initial conditions in the main game loop.
Returns if the insurance 
"""
def exe_insurance_logic(payout, insurance_cost, insurance_win, wager, player_bank):
	payout = insurance_payout(insurance_cost, wager)
	player_bank.add_chips(payout)
	return insurance_win

""" 
Returns the payout for insurance if the dealer has blackjack.
"""
def insurance_payout(insurance_cost, wager):
	return insurance_cost + wager

""" 
Returns the cost of insurance based on the player wager.
Usage: round down and then divide by 1/2. (Ex. 5.5 -> 5 -> 2.5))
"""
def get_insurance_cost(wager):
	return math.floor(wager) * 0.5

"""
Returns the original bet back to the player
"""
def push_payout(wager):
	return wager

"""
Returns the payout for a standard win. (1:1 odds, bet * 2.0)
"""
def standard_payout(wager):
	return wager * 2.0

""" 
Return true if the bet is higher than the minimum bet amount.
"""
def verify_min_bet(wager):
	return wager >= MIN_BET
