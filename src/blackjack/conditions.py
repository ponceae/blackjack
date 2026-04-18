"""
Blackjack game state verifiers.

This module contains functions for checking hand states, game states, and 
player bank statuses.

Author: Adrien P.
"""

from .actions import get_hand_value, get_soft_value
from .constants import MIN_BET, PLAYER_WIN, DEALER_WIN, PUSH
from .datatypes import Hand, Player, PlayerHand, Table 
from.payout_calculator import get_insurance_cost

def can_split(hand: Hand) -> bool:
	"""
	Return True if the first two cards in `hand` have the same rank.
	
	Args:
		hand (Hand): The hand to check.
	
	Returns:
		bool: True if `hand` can be split, False otherwise.
	"""
	return hand.cards[0].rank == hand.cards[1].rank

def compare_initial_hands(table: Table) -> int:
	"""
	Compare the hands at the start of the round and return the outcome flag if 
	applicable.
	
	Args:
		table (Table): The current game table containing the player and dealer hands.
	
	Returns:
		int: Outcome flag of the round.
			PLAYER_WIN if the player has blackjack, 
			DEALER_WIN if the dealer has blackjack, 
			PUSH if both have blackjack.
	"""
	player_blackjack = is_twenty_one(table.player.hands[0])
	dealer_blackjack = is_twenty_one(table.dealer)
 
	if player_blackjack and dealer_blackjack:
		return PUSH
	elif player_blackjack and not dealer_blackjack:
		return PLAYER_WIN
	elif not player_blackjack and dealer_blackjack:
		return DEALER_WIN
	
	return 0

def is_bust(hand: Hand) -> bool:
	"""
	Return True if the hand's total value exceeds 21.
	
	Args:
		hand (Hand): The hand to check.
	
	Returns:
		bool: True if bust, False otherwise.
	"""	
	return get_hand_value(hand) > 21

def is_soft(hand: Hand) -> bool:
	"""
	Return True if the hand treats any Ace as 1 (soft hand).
	
	Args:
		hand (Hand): The hand to check.
	
	Returns:
		bool: True if soft, False otherwise.
	"""
	return get_soft_value(hand) != get_hand_value(hand)
	
def is_split_aces(hand: Hand) -> bool:
	"""
	Return True if the hand contains 2 Aces.

	Args:
		hand (Hand): The hand to check.
	
	Returns:
		bool: True if split Aces, False otherwise.
	"""	
	return hand.cards[0].rank == 'Ace' and hand.cards[1].rank == 'Ace'

def is_twenty_one(hand: Hand) -> bool:
	"""
	Return True if the hand's total value equals 21.

	Args:
		hand (Hand): The hand to check.
	
	Returns:
		bool: True if the hand value is 21, False otherwise.
	"""	
	return get_hand_value(hand) == 21

def is_valid_wager(player: Player, wager: float) -> bool:
	"""
	Return True if the player has enough chips to cover the hand's wager.

	Args: 
		player (Player): The player whose bank is being checked.
		wager (float): The wager to verify.

	Returns:
		bool: True if the player has enough chips, False otherwise.
	"""
	if not (0 < wager >= MIN_BET):
		return False
	
	return wager <= player.bank.chips
          
def verify_chip_bounds(chips: float) -> bool:
	"""
	Return True if `chips` is a number between 15 - 1000 (inclusive).

	Args:
		chips (float): The amount of chips to validate.
	
	Returns:
		bool: True if the `chips` is within bounds, False otherwise.
	"""
	return isinstance(chips, (int, float)) and 15 <= chips <= 1000

def verify_chip_count(chips: float) -> bool:
	"""
	Return True if `chips` is greater than or equal to the MIN_BET.

	Args:
		chips (float): The amount of chips to validate.

	Returns:
		bool: True if `chips` is greater than the MIN_BET.
	"""
	return chips >= MIN_BET

def verify_doubled_wager(player: Player, hand: PlayerHand) -> bool:
	""" 
	Return True if the player has enough chips to double down or split (match the 
	current wager).

	Args:
		player (Player): The player whose bank is being checked.
		hand (PlayerHand): The hand containing the wager.
	
	Returns:
		bool: True if the player can afford to double the wager, False otherwise.
	"""
	return hand.wager <= player.bank.chips

def verify_insurance_bet(player: Player, hand: PlayerHand) -> bool: 
	"""
	Return True if the player can afford insurance (half the current wager).

	Args:
		player (Player): The player whose bank is being checked.
		hand (PlayerHand): The hand containing the wager.

	Returns:
		bool: True if the player can afford insurance, False otherwise.
	"""
	return get_insurance_cost(hand) <= player.bank.chips

def verify_min_bet(hand: PlayerHand) -> bool:
	"""
	Return True if the current wager meets the required minimum bet.

	Args:
		hand (PlayerHand): The hand containing the wager.
	
	Returns:
		bool: True if the player meets the minimum bet, False otherwise.
	"""
	return hand.wager >= MIN_BET
