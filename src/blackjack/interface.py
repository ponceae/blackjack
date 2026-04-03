""" 
Blackjack CLI display functions.

@author Adrien P.
@version 4.3.26
"""

import subprocess
import sys
import time

from .constants import DEALER_WIN, HIT, NO, PLAYER_WIN, PUSH, ROMAN_NUMERALS, STAND, TIMER_MESSAGES, YES
from .actions import get_hand_value, get_soft_value
from .conditions import is_soft, is_twenty_one

# ==========================================
# DISPLAY
# Main CLI display functions.
# ==========================================

""" 
Compares the hands at the end of the round and displays the outcome.
"""
def compare_hands(player_hand_value, dealer_hand_value, index):
	msg = 'Hand ' + ROMAN_NUMERALS[index + 1]
	if player_hand_value == dealer_hand_value:
		print(msg + ' Push')
	elif player_hand_value > dealer_hand_value:
		print(msg + ' Win')
	elif player_hand_value < dealer_hand_value:
		print(msg + ' Lost')

"""
Main CLI output for Blackjack.
"""
def print_hands(table: Table):
	dealer_hand_value = str(get_hand_value(game_table.dealer))
	dealer_soft_value = str(get_soft_value(hands.dealer_hand))
	"""Parallel lists for player hand values"""
	player_hand_values = [str(get_hand_value(hand)) for hand in hands.player_hands]
	player_soft_values = [str(get_soft_value(hand)) for hand in hands.player_hands]

	output_buffer, dealer_buffer, player_buffer = [], [], []
 
	"""Dealer Hand Output"""
	dealer_buffer.append('Dealer: ')
	if is_hidden: # Dealer showing one card
		dealer_buffer.append(
			f'{hands.dealer_hand[0].get_rank_value()}\n'
			f'{hands.dealer_hand[0].to_string()}\n'
			'?\n'
		)
	else: # Dealer showing both cards
		if is_soft(hands.dealer_hand) and not is_twenty_one(hands.dealer_hand):
			dealer_buffer.append(f'{dealer_soft_value} / ')
		dealer_buffer.append(f'{dealer_hand_value}\n')
		for card in hands.dealer_hand:
			dealer_buffer.append(f'{card.to_string()}\n')
	if insurance_wager > 0:
		dealer_buffer.append(f'Insurance [${insurance_wager:.2f}]\n')
	dealer_buffer.append('--------------------\n')
	output_buffer.append(dealer_buffer)
 
	"""Player Hand Output"""
	for i, hand in enumerate(hands.player_hands):
		player_buffer.append(f'Hand {ROMAN_NUMERALS[i + 1]}: ')
		if is_soft(hand) and not is_twenty_one(hand): # Show soft value
			player_buffer.append(f'{player_soft_values[i]} / ')
		player_buffer.append(
			f'{player_hand_values[i]}'
			f'{print_wager(wager)}\n'
		)
		if i == active_index:
			player_buffer.append(' <- Active')
		for card in hand:
			player_buffer.append(f'{card.to_string()}\n')
		player_buffer.append('--------------------\n')
	player_buffer.append(player_bank.to_string())
	output_buffer.append(player_buffer)
	
	for strings in output_buffer:
		print(*strings, sep='', end='')
	print()

def print_dealer_hands():
    pass

def print_player_hands():
	pass

""" 
CLI output for initial round ending scenarios.
"""
def print_initial_outcome(outcome, payout, wager):
	if outcome == PUSH:
		print(f'Round Push. Returned ${wager:.2f}')
	elif outcome == PLAYER_WIN:
		print(f'Player Blackjack. You Won ${payout:.2f}')
	elif outcome == DEALER_WIN:
		print('Dealer Blackjack. You Lose')

""" 
CLI output for insurance outcomes.
"""
def print_initial_insurance_outcome(insurance, payout, insurance_win):
	if insurance and insurance_win:
		print(f'You Won ${payout:.2f} With Insurance.')
	elif insurance and not insurance_win:
		print('No Dealer Blackjack, Insurance Lost.')
  
""" 
Prints the wager in two-decimal format.
"""
def print_wager(wager):
	return f' [${wager:.2f}]'

# ==========================================
# I/O
# Prompts user for input.
# ==========================================

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
Prompts the user if they wish to double down and returns the choice.
"""
def double_or_not():
	while True:
		choice = input('\nDouble Down? (Y) / (N)\n')
		if choice.upper() in (YES, NO):
			return choice.upper()
		print('Invalid Choice, (Y) YES / (N) NO')

"""
Prompts the user if they wish to hit or stand and returns the choice.
"""
def hit_or_stand():
	while True:
		choice = input('\n(H) HIT / (S) STAND\n')
		if choice.upper() in (HIT, STAND):
			return choice.upper()
		print('Invalid Choice, (H) HIT / (S) STAND')

"""
Return true if the user wishes to continue the round, exits the game otherwise.
"""
def is_new_round():
	input = request_new_round()
	if input == NO:
		print('\nExiting Blackjack')
		sys.exit()
	elif input == YES:
		clear_terminal()
		return True

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
Prompts the user if they wish to add chips and returns the choice.
"""
def request_chips():
	while True:
		choice = input('Add chips? (Y) / (N)\n')
		if choice.upper() in (YES, NO):
			return choice.upper()
		print('Invalid Choice, (Y) YES / (N) NO')

"""
Prompts the user if they wish to buy insurance and returns the choice.
"""
def request_insurance(cost):
	while True:
		choice = input(f'\nInsurance? ${cost:.2f} (Y) / (N)\n')
		if choice.upper() in (YES, NO):
			return choice.upper()
		print('Invalid Choice, (Y) YES / (N) NO')

"""
Prompts the user if they wish to start a new round and returns the choice.
"""
def request_new_round():
	while True:
		choice = input('\nNew game with the same deck? (Y) / (N)\n')
		if choice.upper() in (YES, NO):
			return choice.upper()
		print('Invalid Choice, (Y) YES / (N) NO')

""" 
Prompts the user if they wish to split or not and returns the choice.
"""
def split_or_not():
	while True:
		choice = input('\nSplit? (Y) / (N)\n')
		if choice.upper() in (YES, NO):
			return choice.upper()
		print('Invalid Choice, (Y) YES / (N) NO')
  
# ==========================================
# DISPLAY HELPERS
# ==========================================

"""
Clears the CLI.
"""
def clear_terminal():
	subprocess.run('cls', shell=True)

""" 
CLI output that displays the table minimum bet.
"""
def is_valid_bet_msg(player_bank):
	return (
		f'{player_bank.to_string()}\n'
		f'Minimum Bet is: $' + f'{MIN_BET:.2f}\n'
	)

"""
Utility timer function for the CLI display.
"""
def load_timer(timer_flag_key=-1):
	timer_message = TIMER_MESSAGES.get(timer_flag_key, '{}')
	print()
	for i in range(3, 0, -1):
		print(timer_message.format(i), end='\r')
		time.sleep(1)
