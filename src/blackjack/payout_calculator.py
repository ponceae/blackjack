""" 
Blackjack payout functions.

This module contains functions for calculating the payout for a blackjack win, an 
insurance win, double down and splits, and pushes.

Author: Adrien P.
"""

import math

from .datatypes import Insurance, Player, PlayerHand

def blackjack_payout(hand: PlayerHand) -> float:
	"""
	Return the payout for a natural blackjack win (3:2 odds)

	Args: 
		hand (PlayerHand): The hand containing the wager.

	Returns:
		float | int: The blackjack payout.
	"""
	return hand.wager * 2.5

def insurance_logic(insurance: Insurance, player: Player) -> None:
	"""
	Payout the insurance wager to the player, and update their bank.

	Args:
		insurance (Insurance): Contains the insurance information.
		hand (PlayerHand): The hand containing the wager.
		player (Player): The player to payout the wager to.

	Returns:
		None
	"""
	insurance.payout = insurance_payout(insurance.cost)
	player.bank.chips += insurance.payout

def insurance_payout(insurance_cost: float) -> float:
	"""
	Return the insurance payout (half the wager) if the dealer has blackjack.

	Args:
		insurance_cost (float | int): The cost for purchasing insurance

	Returns:
		float: The insurance payout.
	"""
	return insurance_cost * 2.0

def get_insurance_cost(hand: PlayerHand) -> float:
	"""
	Return the cost for purchasing insurance (half the wager).
	Usage: round down and then divide by 1/2. (Ex. 5.5 -> 5 -> 2.5))

	Args:
		hand (PlayerHand): The hand containing the wager.
	
	Returns:
		float: The cost for insurance.
	"""
	return math.floor(hand.wager) * 0.5

def push_payout(hand: PlayerHand) -> float:
	"""
	Return the original wager back to the player.

	Args:
		hand (PlayerHand): The hand containing the wager.

	Returns:
		float: The original wager.
	"""
	return hand.wager

def standard_payout(hand: PlayerHand) -> float:
	"""
	Return the standard payout for a win (1:1 odds).

	Args:
		hand (PlayerHand): The hand containing the wager.

	Returns:
		float: The standard payout.
	"""
	return hand.wager * 2.0
