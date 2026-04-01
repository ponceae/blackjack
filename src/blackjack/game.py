"""
Single-Deck Blackjack.
Dealer stands on soft 17.
Insurance not offered.

@author Adrien P.
@version 3.28.26
"""

from .card import Card
from .bank import Bank
from .datatypes import GameHands

from . import file_helper
from . import bank_helper
from . import helper
from . import constants 
from . import utilities

"""
Dealer turn, hits until they encounter a soft 17 in which case they stand.
Will terminate if the dealer busts or hits 21.
"""
def exe_dealer_control(player_hands, dealer_hand, game_deck):
	helper.print_hands(player_hands, dealer_hand)
	utilities.load_timer(constants.SHOW) # Dealer will now show the hidden card
	helper.clear_terminal()
	helper.print_hands(player_hands, dealer_hand, is_hidden=False)
	while helper.get_hand_value(dealer_hand) < 17: # Dealer will hit until a soft 17 value occurs
		utilities.load_timer(constants.DEALER) 
		utilities.hit_hand(dealer_hand, game_deck) 
		helper.clear_terminal()
		helper.print_hands(player_hands, dealer_hand, is_hidden=False)
		if helper.is_bust(dealer_hand):
			print('Dealer has Busted\n')
			return
		elif helper.is_twenty_one(dealer_hand):
			print('Dealer is Standing\n')
			return
	print('Dealer is Standing\n')

""" 
Checks for a player/dealer blackjack or a push after the initial round deal
is completed. The user can also buy insurance if the dealer is showing
an ace. Pays out the player and updates the player bank depending
on the win condition.
"""
def exe_initial_cond(player_hands, dealer_hand, player_bank, wager):  
	outcome = helper.compare_initial_hands(player_hands[0], dealer_hand)
	insurance, insurance_win = False, False
	payout = 0.0
	broke = False
	insurance_cost = bank_helper.get_insurance_cost(wager)
	if (dealer_hand[0].rank == 'Ace' and helper.request_insurance(insurance_cost) == constants.YES): 
		if bank_helper.verify_insurance_bet(player_bank, wager):# Verify player has enough chips for insurance
			insurance = True
			player_bank.remove_chips(insurance_cost)
			utilities.clear_terminal()
			helper.print_hands(
				player_hands,
				dealer_hand,
				wager,
				player_bank,
				insurance_wager=insurance_cost
			)
		else:
			utilities.clear_terminal()
			helper.print_hands(
				player_hands,
				dealer_hand,
				wager,
				player_bank,
			)
			utilities.load_timer(constants.BROKE) # Display broke message
	if outcome in (constants.PLAYER_WIN, constants.DEALER_WIN, constants.PUSH): # Round ending condition has been met
		if outcome == constants.DEALER_WIN: # Dealer blackjack, hidden card is shown
			utilities.clear_terminal()
			helper.print_hands(player_hands, dealer_hand, wager, player_bank)
			utilities.load_timer(constants.INITIAL) 
			utilities.clear_terminal()
			helper.print_hands(player_hands, dealer_hand, wager, player_bank)
			if insurance: # Payout insurance to the player
				insurance_win = bank_helper.exe_insurance_logic(
					payout, 
					insurance_cost, 
					insurance_win, 
					wager, 
					player_bank
				)
		elif outcome == constants.PUSH: # Return initial wager to the player
			payout = bank_helper.push_payout(wager)
			player_bank.add_chips(payout)
			if insurance: # 'Even' money payout 
				insurance_win = bank_helper.exe_insurance_logic(
					payout, 
					insurance_cost, 
					insurance_win, 
					wager, 
					player_bank
				)
		elif outcome == constants.PLAYER_WIN: # Payout blackjack to the player
			payout = bank_helper.blackjack_payout(wager)
			player_bank.add_chips(bank_helper.blackjack_payout(wager))
		utilities.load_timer(constants.SHOW)
		helper.clear_terminal()
		helper.print_hands(player_hands, dealer_hand, wager, player_bank, is_hidden=False)
		helper.print_initial_insurance_outcome(insurance, payout, insurance_win) # Display insurance outcome
		helper.print_initial_outcome(outcome, payout, wager) # Displays the round outcome
		if helper.is_new_round():
			return True
	utilities.load_timer(constants.INITIAL) # Dealer does not have blackjack
	if insurance: 
		insurance_win = False # Player bought insurance and lost it	
	helper.clear_terminal()
	helper.print_hands(player_hands, dealer_hand, wager, player_bank)
	helper.print_initial_insurance_outcome(insurance, payout, insurance_win)
 
"""
Player turn. Can hit, stand, split, or double down.
"""
def exe_player_control(player_hands, dealer_hand, game_deck, player_bank, wager):
	split_hand = False
	if (
		helper.can_split(player_hands[0])
		and helper.split_or_not() == constants.YES
		and bank_helper.verify_double_bet(player_bank, wager)
	): # User wishes to split & has enough chips
		split_hand = True 
		split_aces = helper.is_split_aces(player_hands[0])
		utilities.create_split_hands(player_hands, game_deck)
		if split_aces:
			return # Cannot hit on split aces, advance to dealer turn           
	helper.clear_terminal()   
	prev_action = None # Stores previous user action for display purposes    
	for i, hand in enumerate(player_hands):
		helper.print_hands(player_hands, dealer_hand, active_index=i)
		if helper.double_or_not() == constants.YES: # User can only double down on the initial hand
			helper.clear_terminal()
			utilities.hit_hand(hand, game_deck)
			helper.print_hands(player_hands, dealer_hand, active_index=i)
			if exe_player_control_helper(split_hand, player_hands, i, True): continue # Switch player hands if applicable
			if exe_player_control_helper(split_hand, player_hands, i, False): break
		else:
			utilities.clear_terminal()
			helper.print_hands(player_hands, dealer_hand, player_hands, active_index=i)
		while helper.hit_or_stand() == constants.HIT: # Player wishes to hit
			utilities.hit_hand(hand, game_deck)
			helper.clear_terminal()
			helper.print_hands(player_hands, dealer_hand, active_index=i) # Display updated hand
			if helper.is_bust(hand): # If the hand busts after the hit
				prev_action = constants.BUST
				print('Hand ' + constants.ROMAN_NUMERALS[i + 1] + ' has Busted\n')
				if exe_player_control_helper(split_hand, player_hands, i, True): break # Switch player hands if applicable
				if exe_player_control_helper(split_hand, player_hands, i, False): break
			elif helper.is_twenty_one(hand): # If the hand is 21 after the hit
				prev_action = constants.STAND
				print('Hand ' + constants.ROMAN_NUMERALS[i + 1] + ' is Standing\n')
				if exe_player_control_helper(split_hand, player_hands, i, True): break # Switch player hands if applicable
				if exe_player_control_helper(split_hand, player_hands, i, False): break
		if prev_action not in (constants.BUST, constants.STAND): # Player is standing on this hand
			helper.clear_terminal()
			helper.print_hands(player_hands, dealer_hand)
			print('Hand ' + constants.ROMAN_NUMERALS[i + 1] + ' is Standing\n')
			if exe_player_control_helper(split_hand, player_hands, i, True): continue # Switch player hands if applicable
			if exe_player_control_helper(split_hand, player_hands, i, False): continue   

""" 
Verifies player hand state and returns true on a successful execution.
"""
def exe_player_control_helper(split_hand, player_hands, i, split_check):
	if (split_check and (split_hand and i != len(player_hands) - 1)): # Switch hands if applicable
		utilities.load_timer(constants.PLAYER)
		utilities.clear_terminal()
		return True
	elif not split_check:
		utilities.load_timer(constants.SWITCH_TURN) # Normal flow, player turn is finished
		utilities.clear_terminal()
		return True
	return False

""" 
Compare the hand values at the end of the round and determine a winner.
"""
def verify_round_end_cond(player_hands, dealer_hand):
	dealer_hand_value, dealer_bust = helper.get_hand_value(dealer_hand), helper.is_bust(dealer_hand)	
	helper.print_hands(player_hands, dealer_hand, is_hidden=False)
	for i, hand in enumerate(player_hands):
		player_hand_value = helper.get_hand_value(hand)
		player_bust = helper.is_bust(hand)
		if player_bust:
			print('Hand ' + constants.ROMAN_NUMERALS[i + 1] + ' Busted & Lost')
			continue # Check next hand if applicable or exit on a bust
		elif not player_bust and dealer_bust:
			print('Hand ' + constants.ROMAN_NUMERALS[i + 1] + ' Win')
		elif not player_bust and not dealer_bust: # Normal comparison, no busts encountered
			helper.compare_hands(player_hand_value, dealer_hand_value, i)
	if helper.is_new_round():
		return True
								
"""
Main blackjack game loop.
"""
def blackjack(game_deck, player_bank):
	while True:
		"""Set Wager"""
		bet_amount = bank_helper.is_valid_bet(player_bank) # Prompt bet from user
		utilities.clear_terminal()
		bank_helper.verify_min_bet(bet_amount)
		player_bank.remove_chips(bet_amount) # Initial bet, remove chips
		utilities.clear_terminal()
		
		hands = GameHands(player=[[]], dealer=[])
		# player_hands, dealer_hand = [], []
		hands.player_hands, hands.dealer_hand = [[Card('Spades', 4), Card('Spades', 2)]], [Card('Spades', 'Ace'), Card('Spades', 10)]
		round_done = False
		
		# utilities.initial_round_deal(player_hands, dealer_hand, game_deck)
		helper.print_hands(hands, bet_amount, player_bank)
		
		"""Check for initial round conditions"""
		round_done = round_done or exe_initial_cond(hands, player_bank, bet_amount)
		break
		# """Execute player control - hit hand, check for busts or 21"""
		# if not round_done: exe_player_control(player_hands, dealer_hand, game_deck, player_bank, bet_amount)
		
		# """Execute dealer control - check for busts or 21"""
		# if not round_done: exe_dealer_control(player_hands, dealer_hand, game_deck)
		
		# """Check hands for end conditions"""
		# if not round_done: 
		# 	utilities.load_timer(constants.CHECK)
		# 	utilities.clear_terminal()
		# 	round_done = verify_round_end_cond(player_hands, dealer_hand)

		# """Player will reuse same game deck on next round iteration"""
		# if not round_done: break
  
def main():
	print('Blackjack Pays 3:2\n' + 
		'Dealer Stands on Soft 17\n' +
		  'Insurance Pays 2:1\n')
	input('Press Any Key to Continue to Betting\n')
	utilities.clear_terminal()
	player_bank = Bank(file_helper.pull_user_info())
	utilities.clear_terminal()
	blackjack(utilities.create_and_shuffle(), player_bank)
 
if __name__ == '__main__':
	main()
