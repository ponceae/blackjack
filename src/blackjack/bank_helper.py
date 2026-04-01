""" 
Helper functions that handle the buy in, payout or removal of game chips.

@author Adrien P.
@version 3.28.26
"""

import math
from .constants import MIN_BET, NO, PLAYER_WIN, PUSH, YES  
from .utilities import clear_terminal

""" 
Prompts the user if they wish to add chips and updates the player chip count.
"""
def add_chips(player_bank):
	if request_chips() == YES:
		while True:
			chip_count = float(input('How many chips would you like to add?\n'))
			if verify_chip_bounds(chip_count):
				player_bank.add_chips(chip_count)
				return
			print('Invalid Input. Must be a number between 15 - 1000.')

"""
Returns the payout for a natural blackjack win. (3:2 odds, bet * 1.5)
"""
def blackjack_payout(wager):
	return wager * 2.5

""" 
Updates player chips on an initial push or a blackjack win
"""
def initial_outcome_payout_helper(outcome, player_bank, wager):
	if outcome == PLAYER_WIN:
		payout = blackjack_payout(wager)
		player_bank.add_chips(payout)
	elif outcome == PUSH:
		player_bank.add_chips(wager)

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
Returns true if the player has enough chips for the requested bet. 
"""
def is_valid_bet_helper(player_bank, wager):
	return wager <= player_bank.get_chip_count()

""" 
Returns the wager and updates the player bank object.
"""
def is_valid_bet(player_bank):
	print(is_valid_bet_msg(player_bank))
	while True:
		try:
			wager = float(input('Enter Wager:\n'))
			valid_bet = is_valid_bet_helper(player_bank, wager)
			verified_bet = verify_chip_bounds(wager)
			if valid_bet and verified_bet:
				return wager
			elif not valid_bet:
				print('Not Enough Chips')
				add_chips(player_bank)
				clear_terminal()
				print(is_valid_bet_msg(player_bank))
			elif not verified_bet:
				print('Wager is Too Small')
		except ValueError:
			print('Please Enter a Valid Number.')

""" 
CLI output that displays the table minimum bet.
"""
def is_valid_bet_msg(player_bank):
	return (
		f'{player_bank.to_string()}\n'
		f'Minimum Bet is: $' + f'{MIN_BET:.2f}\n'
	)

""" 
Prompts the user if they wish to add chips and returns the choice.
"""
def request_chips():
	while True:
		choice = input('Add chips? (Y) / (N)\n')
		if choice.upper() in (YES, NO):
			return choice.upper()
		print('Invalid Choice, (Y) YES / (N) NO')
	 
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
