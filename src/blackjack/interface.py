""" 
Blackjack CLI display functions.

This module contains functions for displaying player and dealer hands, round states,
and gathering user input.

Author: Adrien P.
"""

import subprocess
import sys
import time

from .actions import get_hand_value, get_soft_value
from .bank import Bank
from .conditions import (
	is_soft, 
	is_twenty_one, 
	is_valid_wager, 
	verify_chip_bounds, 
	verify_chip_count,
)
from .constants import (
	BUST,
	DEALER_WIN, 
	HIT, 
	MIN_BET,
	NO, 
	PLAYER_WIN, 
	PUSH, 
	ROMAN_NUMERALS, 
	STAND, 
	TIMER_MESSAGES, 
	YES,
)
from .datatypes import (
	Buffers,
	Insurance,
	Outcome,
	Player,
	PlayerHand,
	Table,
)
from .payout_calculator import push_payout, standard_payout
from .storage import load_user_data, save_chips

# ==========================================
# DISPLAY
# Main CLI display functions.
# ==========================================

def compare_hands(table: Table, hand: PlayerHand, index: int) -> tuple[str, int]:
	"""
	Compare the PlayerHand(s) and DealerHand at the end of the round and display the 
	outcome. Return the round outcome flag.

	Args:
		table (Table): The current game table containing the player and dealer hands.
		index (int): The index of the current player hand.
	
	Returns:
		tuple[str, int]: A tuple containing:
			A string containing the display message.
  			The flag determining the round outcome.
	"""
	msg = 'Hand ' + ROMAN_NUMERALS[index + 1]

	player_hand_value = get_hand_value(hand)
	dealer_hand_value = get_hand_value(table.dealer)
	
	if player_hand_value == dealer_hand_value:
		return (f'{msg} Push, Returned ${push_payout(hand):.2f}\n'), PUSH
	elif player_hand_value > dealer_hand_value:
		return (f'{msg} Win, You Won ${standard_payout(hand):.2f}\n'), PLAYER_WIN
	elif player_hand_value < dealer_hand_value:
		return (f'{msg} Lost\n'), DEALER_WIN
	
	return '', 0

def clear_and_print(table: Table) -> None:
	"""
	Clear the CLI display and display the table hands.

	Args:
		table (Table): The current game table containing the player and dealer hands.

	Returns:
		None
	"""
	clear_terminal()
	print_hands(table)

def print_hands(table: Table) -> None:
	"""
	Display the PlayerHand(s) and DealerHand to the CLI.

	Args: 
		table (Table): The current game table containing the player and dealer hands.

	Returns:
		None
	"""
	buffers = Buffers([], [], [])

	_print_dealer_hands(table, buffers)
	_print_player_hands(table, buffers)

	for strings in buffers.main:
		print(*strings, sep='', end='')

	print()

def _print_dealer_hands(table: Table, buffers: Buffers) -> None:
	"""
	Display the DealerHand or the dealer's first card depending on the game state.
	Display insurance if purchased by the player.

	Args:
		table (Table): The current game table containing the dealer hand.
		buffers (Buffer): A NamedTuple containing the dealer and main buffer.
	
	Returns:
		None
	"""
	dealer_hand_value = str(get_hand_value(table.dealer))
	dealer_soft_value = str(get_soft_value(table.dealer))
	
	buffers.dealer.append('Dealer: ')

	if table.dealer.is_hidden: # Dealer showing one card.
		buffers.dealer.append(
			f'{table.dealer.cards[0].get_rank_value()}\n'
			f'{table.dealer.cards[0].to_string()}\n'
			'?\n'
		)	
	else: # Dealer showing both cards.
		if is_soft(table.dealer) and not is_twenty_one(table.dealer):
			buffers.dealer.append(f'{dealer_soft_value} / ')

		buffers.dealer.append(f'{dealer_hand_value}\n')
		
		for card in table.dealer.cards:
			buffers.dealer.append(f'{card.to_string()}\n')
	
	if table.player.hands[0].insurance_wager > 0:
		buffers.dealer.append(
			f'Insurance [${table.player.hands[0].insurance_wager:.2f}]\n'
		)

	buffers.dealer.append('--------------------\n')

	buffers.main.append(buffers.dealer)

def _print_player_hands(table: Table, buffers: Buffers) -> None:
	"""
	Display the PlayerHand(s) and `wager`. If PlayerHand is split, display the
	active hand.

	Args:
		table (Table): The current game table containing the player's hands.
		buffers (Buffers): A NamedTuple containing the player and main buffer.

	Returns:
		None
	"""
	player_hand_values = [str(get_hand_value(hand)) for hand in table.player.hands]

	player_soft_values = [str(get_soft_value(hand)) for hand in table.player.hands]

	for i, hand in enumerate(table.player.hands):
		buffers.player.append(f'Hand {ROMAN_NUMERALS[i + 1]}: ')

		if is_soft(hand) and not is_twenty_one(hand): # Show soft value
			buffers.player.append(f'{player_soft_values[i]} / ')

		buffers.player.append(
			f'{player_hand_values[i]}'
			f'{_print_wager(table.player.hands[i].wager)}'
		)

		if table.player.hands[i].is_active:
			buffers.player.append(' <- Active\n')
		else:
			buffers.player.append('\n')
		for card in hand.cards:
			buffers.player.append(f'{card.to_string()}\n')

		buffers.player.append('--------------------\n')
	
	buffers.player.append(table.player.bank.to_string())

	buffers.main.append(buffers.player)

def print_initial_outcome(outcome: Outcome, hand: PlayerHand) -> None:
	"""
	Display the outcome at the beginning of the round if a player or dealer
	blackjack occured.

	Args:
		outcome (Outcome): Contains the outcome flag and payout.
		hand (PlayerHand): The player hand containing the wager.

	Returns:
		None
	"""
	if outcome.flag == PUSH:
		print(f'Round Push, Returned ${hand.wager:.2f}')
	elif outcome.flag == PLAYER_WIN:
		print(f'Player Blackjack, You Won ${outcome.payout:.2f}')
	elif outcome.flag == DEALER_WIN:
		print('Dealer Blackjack, You Lose')

def print_initial_insurance_outcome(insurance: Insurance) -> None:
	"""
	Display the insurance outcome if purchased by the player.

	Args:
		insurance (Insurance): Contains the insurance status, win status, and payout.
	
	Returns:
		None
	"""
	if insurance.active and insurance.win:
		print(f'You Won ${insurance.payout:.2f} With Insurance.')
	elif insurance.active and not insurance.win:
		print('No Dealer Blackjack, Insurance Lost.')

# ==========================================
# I/O
# Prompt user for input.
# ==========================================

def _add_chips(player: Player) -> None:
	"""
	Prompt the user if they wish to add chips to their bank and updates the
	chip count.

	Args: 
		player (Player): The player whose bank to update.
	
	Returns:
		None
	"""
	if request_chips() == YES:
		while True:
			chips = float(input('Enter the amount of chips to add.\n'))
			
			if verify_chip_bounds(chips):
				player.bank.chips += chips
				break
			
			print('Invalid Input, Must be a number between 15 - 1000.')

def double_or_not() -> str:
	"""
	Prompt the user if they wish to double down (match the wager) and return their 
	choice.

	Returns:
		str: The user's yes or no decision.
	"""
	while True:
		choice = input('\nDouble Down? (Y) / (N)\n')

		if choice.upper() in (YES, NO):
			return choice.upper()
		
		print('Invalid Choice, (Y) YES / (N) NO')

def hit_or_stand() -> str:
	"""
	Prompt the user if they wish to hit or stand and return their choice.

	Returns:
		str: The user's hit or stand decision.
	"""
	while True:
		choice = input('\n(H) HIT / (S) STAND\n')

		if choice.upper() in (HIT, STAND):
			return choice.upper()
		
		print('Invalid Choice, (H) HIT / (S) STAND')

def is_new_round(table: Table) -> bool:
	"""
	Prompt the user if they wish to continue the round with the same game deck and
	return their choice.

	Returns:
		bool: True if the user wants to continue, otherwise exit the program.
	"""
	input = request_new_round()

	if input == NO:
		print('\nExiting Blackjack & Saving Data.')
		save_chips(table.player.username, table.player.bank.chips, load_user_data())
		sys.exit()
	elif input == YES:
		clear_terminal()
		return True
	
	return False

def wager_prompt(player: Player) -> float:
	"""
	Prompt and verify the user for a wager amount. If there are not enough chips,
	prompt the user for more chips.

	Args:
		player (Player): The player whose bank to check or update.

	Returns:
		float: The validated wager
	"""
	print(_print_min_bet(player.bank))

	while True:
		try:
			if not verify_chip_count(player.bank.chips):
				_wager_prompt_helper(player)

			wager = float(input('Enter Wager:\n'))

			valid_bet = is_valid_wager(player, wager)
			verified_bet = verify_chip_bounds(wager)
		
			if valid_bet and verified_bet:
				return wager
			elif not valid_bet:
				_wager_prompt_helper(player)
			elif not verified_bet:
				print('Wager is Too Small.')

		except ValueError:
			print('Please Enter a Valid Number.')

def _wager_prompt_helper(player: Player):
	"""
	Add chips to the player's bank if they do not have enough for the minimum bet.

	Args:
		player (Player): The player containing the bank of chips.

	Returns:
		None
	"""
	print('Not Enough Chips.')

	_add_chips(player)

	clear_terminal()
	print(_print_min_bet(player.bank))

def request_chips():
	"""
	Prompt the user if they wish to add chips and return their choice.

	Returns:
		str: The user's yes or no decision.
	"""
	while True:
		choice = input('Add Chips? (Y) / (N)\n')
		
		if choice.upper() in (YES, NO):
			return choice.upper()
		
		print('Invalid Choice, (Y) YES / (N) NO')

def request_insurance(cost: float | int):
	"""
	Prompt the user if they wish to purchase insurance and return their choice.

	Returns:
		str: The user's yes or no decision.
	"""
	while True:
		choice = input(f'\nInsurance? ${cost:.2f} (Y) / (N)\n')
		
		if choice.upper() in (YES, NO):
			return choice.upper()
		
		print('Invalid Choice, (Y) YES / (N) NO')

def request_new_round():
	"""
	Prompt the user if they wish to start a new round with the same game deck
	and return their choice.

	Returns:
		str: The user's yes or no decision.
	"""
	while True:
		choice = input('\nContinue? (Y) / (N)\n')
		
		if choice.upper() in (YES, NO):
			return choice.upper()
		
		print('Invalid Choice, (Y) YES / (N) NO')

def split_or_not():
	"""
	Prompt the user if they wish to split their hand and return their choice.

	Returns:
		str: The user's yes or no decision.
	"""
	while True:
		choice = input('\nSplit? (Y) / (N)\n')
		
		if choice.upper() in (YES, NO):
			return choice.upper()
		
		print('Invalid Choice, (Y) YES / (N) NO')
  
# ==========================================
# DISPLAY HELPERS
# ==========================================

def clear_terminal():
	"""
	Clear the CLI display.

	Returns:
		None
	"""
	subprocess.run('cls', shell=True)

def _print_min_bet(player_bank: Bank):
	"""
	Display the player's bank and the table's minimum bet.

	Args:
		player_bank (Bank): The player bank to display.
	
	Returns:
		str: The string representation of the player bank and the table minimum bet.
	"""
	return (
		f'{player_bank.to_string()}\n'
		f'Minimum Bet is: $' + f'{MIN_BET:.2f}\n'
	)

def load_timer(timer_flag_key: int=-1):
	"""
	Display the timer functions for the CLI depending on the game state.

	Args:
		timer_flag_key (int): The timer flag for the display message.

	Returns:
		None
	"""
	timer_message = TIMER_MESSAGES.get(timer_flag_key, '{}')
	
	print()

	for i in range(3, 0, -1):
		print(timer_message.format(i), end='\r')
		time.sleep(1)
  
def print_dealer_state(flag: str) -> None:
	""" 
	Display if the dealer turn resulted in a bust or stand.
	
	Arguments:
		flag (str): The flag that determines the state of the hand.
	Returns:
		None
	"""
	if flag == STAND:
		print('Dealer is Standing')
	elif flag == BUST:
		print('Dealer has Busted')

def get_round_outcome_msg(index: int, flag: str):
	""" 
	Get round outcome message based off of the flag and return the message.
	
	Arguments:
		index (int): The index of the hand.
		flag (str): The flag that determines the game state.
	Returns:
		str: The outcome message.
	"""
	if flag == BUST:
		return f'Hand {ROMAN_NUMERALS[index + 1]} Busted & Lost\n'
	elif flag == PLAYER_WIN:
		return f'Hand {ROMAN_NUMERALS[index + 1]} Win. ' 

def get_round_outcome_payout_msg(hand: PlayerHand) -> str:
	""" 
	Get and return the display message for a standard blackjack win.
	
	Arguments:
		hand (PlayerHand): The hand containing the wager.
	Returns:
		The display message for a win.
	"""
	return f'You Won ${standard_payout(hand):.2f}\n'

def print_stand_or_bust(index: int, flag: str) -> None:
	""" 
	Display which hand is standing or if it has already busted.
	
	Arguments:
		index (int): The index of the hand.
		flag (str): The flag that determines the state of the hand.
 	Returns:
		None
	"""
	if flag == STAND:
		print(f'Hand {ROMAN_NUMERALS[index + 1]} is Standing')
	elif flag == BUST:
		print(f'Hand {ROMAN_NUMERALS[index + 1]} has Busted')

def _print_wager(wager: float | int):
	"""
	Display the player wager in two-decimal format.

	Args:
		wager (float | int): The current wager on the player hand.

	Returns:
		The string representation of the player wager.
	"""
	return f' [${wager:.2f}]'
