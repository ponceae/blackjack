"""
Single-Deck Blackjack.
Dealer stands on soft 17.
Insurance offered.

Author: Adrien P.
"""

from . import actions
from .bank import Bank
from . import conditions
from . import constants
from .datatypes import (
	Insurance, 
	Outcome, 
	Player,
	PlayerAction, 
	PlayerHand, 
	SplitHands, 
	Table
)
from . import interface
from . import payout_calculator
from . import storage

# ==================================================
# INITIAL ROUND ACTIONS
# Player or dealer blackjack and insurance handling.
# ==================================================

def exe_initial_cond(table: Table) -> bool:
	"""
	Execute the initial round check. Check for a player or dealer blackjack or a push 
	after the initial round deal is completed. The user is also able to purchase 
	insurance if the dealer is showing an Ace. Pay out the player and update the player 
	bank accordingly depending on the win condition.

	Args:
		table (Table): The current game table containing the player and dealer hands.
	Returns:
		bool: True if the user wishes to start a new round, False otherwise.
	"""  
	insurance, outcome = Insurance(), Outcome()
	player_hand = table.player.hands[0]
	outcome.flag = conditions.compare_initial_hands(table)
	handle_insurance(insurance, table)
 
	if outcome.flag in (constants.PLAYER_WIN, constants.DEALER_WIN, constants.PUSH): 
		handle_outcomes(outcome, insurance, table)
		interface.load_timer(constants.SHOW)
		table.dealer.is_hidden = False
		interface.clear_and_print(table) 
		table.player.hands[0].insurance_wager = 0
		interface.clear_and_print(table)
		interface.print_initial_insurance_outcome(insurance) 
		interface.print_initial_outcome(outcome, player_hand)
	
		if interface.is_new_round(table):
			return True
	
	if insurance.active: 
		# Player purchased insurance and lost.
		insurance.win = False 	
		table.player.hands[0].insurance_wager = 0
	
	interface.clear_and_print(table)
	interface.print_initial_insurance_outcome(insurance)
	return False

def handle_insurance(insurance: Insurance, table: Table) -> None:
	"""
	Prompt the user if they wish to purchase insurance and update the insurance
	status and player bank.

	Args:
		insurance (Insurance): The insurance information.
		table (Table): The current game table containing the player hand.
		player_hand (PlayerHand): The player hand containing the wager.

	Returns:
		None
	"""
	insurance.cost = payout_calculator.get_insurance_cost(table.player.hands[0])
	player_hand = table.player.hands[0]
	
	if table.dealer.cards[0].rank == constants.ACE:
		interface.load_timer(constants.INITIAL)
		
		  # Verify player has enough chips for insurance.
		if (interface.request_insurance(insurance.cost) == constants.YES):
			if conditions.verify_insurance_bet(table.player, player_hand):  
				insurance.active = True
				player_hand.insurance_wager = insurance.cost
				table.player.bank.chips -= insurance.cost
				interface.clear_and_print(table)
			else:
				interface.clear_and_print(table)
				interface.load_timer(constants.BROKE)

def handle_outcomes(outcome: Outcome, insurance: Insurance, table: Table) -> None:
	"""
	Update the player bank if a win condition was met and pay out insurance
	if purchased by the player.

	Args:
		outcome (Outcome): The win condition that was met.
		insurance (Insurance): The insurance information.
		table (Table): The current game table containing the player and dealer hands.

	Returns: 
		None
	"""
	player_hand = table.player.hands[0]
	
	# Dealer blackjack, hidden card is shown.
	if outcome.flag == constants.DEALER_WIN:
		interface.clear_and_print(table)
		# Payout insurance to the player.
		insurance_helper(insurance, table)
	# Return initial wager to the player.
	elif outcome.flag == constants.PUSH:
		outcome.payout = payout_calculator.push_payout(player_hand)
		table.player.bank.chips += outcome.payout
		# Even money payout.
		insurance_helper(insurance, table)
	elif outcome.flag == constants.PLAYER_WIN:
		outcome.payout = payout_calculator.blackjack_payout(player_hand)
		table.player.bank.chips += outcome.payout

def insurance_helper(insurance: Insurance, table: Table) -> None:
	"""
	Pay out the insurance to the player if they had purchased it.

	Args:
		insurance (Insurance): The insurance information.
		table (Table): The current game table containing the player and dealer hands.

	Returns:
		None
	"""
	if insurance.active:
		insurance.win = True
		payout_calculator.insurance_logic(insurance, table.player)

# ==================================================
# PLAYER TURN ACTIONS
# Player can hit, stand, split, or double down.
# ==================================================

def exe_player_control(table: Table) -> None:
	"""
	Execute the player turn. Here the player can choose to hit, stand, double down,
	or split their hand. Update the player bank and player hands based on the decision
	that they make.

	Args:
		table (Table): The current game table containing the player hands

	Returns:
		None
	"""
	split = SplitHands()
	handle_split(table, split)  
	
	 # Cannot hit on split aces, advance to the dealer's turn.
	if split.split_aces:
		return   
	
	interface.clear_terminal()   
	prev_action = None     
	
	for i, hand in enumerate(table.player.hands):
		table.player.hands[i].is_active = True
		interface.print_hands(table)
		# User can only double down before hitting.
		try:
			if (
				interface.double_or_not() == constants.YES 
				and conditions.verify_doubled_wager(
					table.player, 
					table.player.hands[i],
				)
			):
				action = handle_double_down(table, i, split)
				if action == PlayerAction.NEXT_HAND:
					continue
				else:
					break
			else:
				interface.clear_and_print(table)
				prev_action, action = handle_hitting(table, split, hand, i)		
				if action == PlayerAction.NEXT_HAND:
					continue
				
				if prev_action not in (constants.BUST, constants.STAND): 
					interface.clear_and_print(table)
					interface.print_stand_or_bust(i, constants.STAND)
					print()

					if hands_left(split, table.player.hands, i):
						continue
					else:
						break
		finally:
			table.player.hands[i].is_active = False

def handle_hitting(
    	table: Table, 
     	split: SplitHands, 
      	hand: PlayerHand, 
       	i: int
) -> tuple[str, PlayerAction]:
	"""
	Main loop when a player decides to hit the current hand. Break out of the loop
	when the user stops hitting or when a bust or 21 condition is met, and return
	the player action.

	Args: 
		table (Table): The current game table containing the player hands
		split (SplitHands): The split hands flag container.
		hand (PlayerHand): The current player hand to modify.
		i (int): The current hand pointer.
	Returns:
		tuple[str, PlayerAction]: The previous recorded action and the 
  								  next player action.
	"""
	while interface.hit_or_stand() == constants.HIT:
		actions.hit_hand(table, hand)
		interface.clear_and_print(table)

		if conditions.is_bust(hand): 
			prev_action = constants.BUST
			interface.print_stand_or_bust(i, constants.BUST)

			if hands_left(split, table.player.hands, i):
				return prev_action, PlayerAction.NEXT_HAND
			else:
				return prev_action, PlayerAction.END_TURN

		elif conditions.is_twenty_one(hand):  
			prev_action = constants.STAND
			interface.print_stand_or_bust(i, constants.STAND)
			
			if hands_left(split, table.player.hands, i):
				return prev_action, PlayerAction.NEXT_HAND
			else:
				return prev_action, PlayerAction.END_TURN
	
	prev_action = constants.STAND
	if hands_left(split, table.player.hands, i):
		return prev_action, PlayerAction.NEXT_HAND
	else:
		return prev_action, PlayerAction.END_TURN

def hands_left(split: SplitHands, player_hands: list[PlayerHand], i: int) -> bool:
	"""
	Return True if the player has another hand after doubling down.

	Args:
		split (SplitHands): The split hands flag container.
		player_hands (list[PlayerHand]): All of the player's current hands.
		i (int): The current hand pointer.

	Returns:
		bool: True if the player has another hand, False otherwise.
	"""
	# Switch hands if applicable.
	if (split.split_hand and i != len(player_hands) - 1): 
		interface.load_timer(constants.PLAYER)
		interface.clear_terminal()
		return True

	# Normal flow, player turn is finished.
	interface.load_timer(constants.SWITCH_TURN) 
	interface.clear_terminal()
	return False

def handle_double_down(table: Table, i: int, split: SplitHands) -> PlayerAction:
	"""
	Update the player bank and hand wager if the user decides to double down (match
	orignal wager), and return the player action.

	Args: 
		table (Table): The current game table containing the player hands.
		i (int): The current hand pointer.
		split (SplitHands): The split hands flag container.

	Returns:
		PlayerAction: The player action. 
			 			1: NEXT_HAND 
			 			2: END_TURN
	"""
	table.player.bank.chips -= table.player.hands[i].wager
	table.player.hands[i].wager += table.player.hands[i].wager
	
	actions.hit_hand(table, table.player.hands[i]) 
	interface.clear_and_print(table)
 
	if hands_left(split, table.player.hands, i): 
		# Switch player hands if applicable.
		return PlayerAction.NEXT_HAND 
	else:
		return PlayerAction.END_TURN
	
def handle_split(table: Table, split: SplitHands) -> None:
	"""
	Add another hand to the player if they wish to split, and update the player
	bank and add a wager (match original wager) to the new hand.

	Args:
		table (Table): The current game table containing the player hands.
		split (SplitHands): The split hands flag container.

	Returns:
		None
	"""
	req_split = (
		conditions.can_split(table.player.hands[0]) 
		and interface.split_or_not() == constants.YES
	)
	if (
		req_split
		and conditions.verify_doubled_wager(table.player, table.player.hands[0])
	): 
		# User wishes to split & has enough chips.
		split.split_hand = True 
		split_aces = conditions.is_split_aces(table.player.hands[0])
		actions.create_split_hands(table)

		table.player.bank.chips -= table.player.hands[0].wager
		table.player.hands[1].wager = table.player.hands[0].wager
		if split_aces:
			split.split_aces = True
	elif (
		req_split 
		and not conditions.verify_doubled_wager(table.player, table.player.hands[0])
	):
		interface.load_timer(constants.BROKE)

# ======================
# DEALER TURN ACTIONS.
# ======================

def exe_dealer_control(table: Table):
	"""
	Execute the dealer turn. Hit until they encounter a soft 17 in which case they 
	stand. Turn will end if the dealer busts or hits 21.

	Args:
		table (Table): The current game table containing the dealer hand.
	
	Returns:
		None
	"""
	interface.print_hands(table)
	# Dealer will now show the hidden card
	interface.load_timer(constants.SHOW) 
	table.dealer.is_hidden = False
	interface.clear_and_print(table)
	while actions.get_hand_value(table.dealer) < 17: 
		interface.load_timer(constants.DEALER) 
		actions.hit_hand(table, table.dealer) 
		interface.clear_and_print(table)
		if conditions.is_bust(table.dealer):
			interface.print_dealer_state(constants.BUST)
			return
		elif conditions.is_twenty_one(table.dealer):
			interface.print_dealer_state(constants.STAND)
			return
	interface.print_dealer_state(constants.STAND)

# ==================
# ROUND END CHECK.
# ==================

def verify_round_end_cond(table: Table):
	""" 
	Compare the hand values at the end of the round and determine the winner.
	Update the player bank if applicable.

	Args: 
		table (Table): The current game table containing the player and dealer hands.

	Returns:
		None
	"""
	tmp_buffer = []
	outcome = Outcome()
	dealer_bust = conditions.is_bust(table.dealer)
	table.dealer.is_hidden = False
	interface.print_hands(table)
	for i, hand in enumerate(table.player.hands):
		player_bust = conditions.is_bust(hand)
		if player_bust:
			tmp_buffer.append(interface.get_round_outcome_msg(i, constants.BUST))
			# Check next hand if applicable or exit on a bust.
			continue 
		elif not player_bust and dealer_bust:
			table.player.bank.chips += payout_calculator.standard_payout(hand)
			tmp_buffer.append(interface.get_round_outcome_msg(i, constants.WIN))
			tmp_buffer.append(interface.get_round_outcome_payout_msg(hand))
		elif not player_bust and not dealer_bust: 
			msg, outcome.flag = interface.compare_hands(table, hand, i)
			tmp_buffer.append(msg)
			if outcome.flag == constants.PUSH:
				table.player.bank.chips += payout_calculator.push_payout(hand)
			elif outcome.flag == constants.PLAYER_WIN:
				table.player.bank.chips += payout_calculator.standard_payout(hand)
	interface.clear_and_print(table)
	for strings in tmp_buffer:
		print(*strings, sep='', end='')
	if interface.is_new_round(table):
		return True

def get_player_wager(player: Player):
	"""
	Prompt the user for a wager amount.

	Args:
		player (Player): The player whose wager is being set.
	
	Returns:
		float | int: The wager amount.
	"""
	wager = interface.wager_prompt(player) 
	interface.clear_terminal()
	player.bank.chips -= wager 
	return wager
						
def blackjack(deck: list, player_bank: Bank, username: str):
	"""
	Execute the main blackjack game loop.

	Args:
		deck (list): The table deck of cards.
		player_bank (Bank): The player's bank containing their chip count.
	
	Returns:
		None
	"""
	table = Table(Player(username=username, bank=player_bank))
	table.deck = deck
	while True:
		wager_amount = get_player_wager(table.player)    
		round_done = False		
		actions.initial_round_deal(table)
		table.player.hands[0].wager = wager_amount
		interface.print_hands(table)
		round_done = round_done or exe_initial_cond(table)	
		if not round_done: 
			exe_player_control(table)
			exe_dealer_control(table)
			interface.load_timer(constants.CHECK)
			interface.clear_terminal()
			round_done = verify_round_end_cond(table)
		if not round_done:
			break
  
def main():
	"""
	Start the Blackjack game. Initialize the player bank and begin the main 
	game loop.
	"""
	print('Blackjack Pays 3:2\n' + 
		'Dealer Stands on Soft 17\n' +
		  'Insurance Pays 2:1\n')
	input('Press Enter to Continue\n')
	interface.clear_terminal()
	chips, username = storage.pull_user_info()
	player_bank = Bank(chips)
	interface.clear_terminal()
	blackjack(actions.create_and_shuffle(), player_bank, username)
 
if __name__ == '__main__':
	main()
