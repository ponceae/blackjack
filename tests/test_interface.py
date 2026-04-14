""" 
Tests for the interface module.

Author: Adrien P.
"""

import pytest

from blackjack.bank import Bank
from blackjack.card import Card
from blackjack import constants
from blackjack.datatypes import (
	DealerHand, 
	Insurance, 
	Outcome, 
	Player, 
	PlayerHand, 
	Table
)
from blackjack import interface
from blackjack import payout_calculator

@pytest.fixture
def mock_inputs(monkeypatch):
	def _mock_inputs(values):
		inputs = iter(values)
		def mock_input(_):
			return next(inputs)
		monkeypatch.setattr('builtins.input', mock_input)
	return _mock_inputs

@pytest.mark.parametrize(
	'func, args, expected_choice',
	[
		(interface.double_or_not, [], 'Y'),
		(interface.request_chips, [], 'Y'),
		(interface.request_insurance, [7.5], 'Y'),
		(interface.request_new_round, [], 'Y'),
		(interface.split_or_not, [], 'Y'),
	]
)
def test_yes_flow(mock_inputs, capsys, func, args, expected_choice):
	mock_inputs(['yes', '0', 'sadf', 'y'])

	choice = func(*args)

	console = capsys.readouterr()
	assert console.out.count('Invalid Choice, (Y) YES / (N) NO\n') == 3
	assert choice == expected_choice

@pytest.mark.parametrize(
	'func, args, expected_choice',
	[
		(interface.double_or_not, [], 'N'),
		(interface.request_chips, [], 'N'),
		(interface.request_insurance, [7.5], 'N'),
		(interface.request_new_round, [], 'N'),
		(interface.split_or_not, [], 'N'),
	]
)
def test_no_flow(mock_inputs, capsys, func, args, expected_choice):
	mock_inputs(['no', '0', 'sadf', 'n'])

	choice = func(*args)

	console = capsys.readouterr()
	assert console.out.count('Invalid Choice, (Y) YES / (N) NO\n') == 3
	assert choice == expected_choice

def test_compare_hands_output():
	player_hand1 = PlayerHand(
		cards=[Card('Spades', 5), Card('Clubs', 5)],
		wager=15.0
	)
	player_hand2 = PlayerHand(
		cards=[Card('Diamonds', 4), Card('Spades', 6), Card('Hearts', 'Ace')],
		wager=30.0
	)
	dealer_hand = DealerHand(
		cards=[Card('Diamonds', 4), Card('Hearts', 6), Card('Spades', 7)]
	)
	table = Table(
		player=Player(username='Test', hands=[player_hand1, player_hand2]), 
		dealer=dealer_hand
	)

	msg, flag = interface.compare_hands(table, table.player.hands[0], 0)
	assert msg == 'Hand I Lost\n'
	assert flag == constants.DEALER_WIN
	
	table.player.hands[0].cards = [Card('Spades', 5), Card('Clubs', 5)]
	table.dealer.cards = [Card('Diamonds', 5), Card('Hearts', 5)]
	msg, flag = interface.compare_hands(table, table.player.hands[0], 0)
	assert msg == 'Hand I Push, Returned $15.00\n'
	assert flag == constants.PUSH
	
	table.dealer.cards = [Card('Diamonds', 5), Card('Hearts', 5), Card('Spades', 7)]
	msg, flag = interface.compare_hands(table, table.player.hands[1], 1)
	assert msg == 'Hand II Win, You Won $60.00\n'
	assert flag == constants.PLAYER_WIN
	
	table.player.hands[0].cards = [Card('Spades', 5), Card('Clubs', 5)]
	table.dealer.cards = [Card('Diamonds', 5), Card('Hearts', 5)]
	msg, flag = interface.compare_hands(table, table.player.hands[0], 0)
	assert msg == 'Hand I Push, Returned $15.00\n'
	assert flag == constants.PUSH

def test_print_player_hands_init_deal(capsys):
	# Test initial deal no insurance display. 
	table = Table (
		player=Player(
			username='Test',
			bank=Bank(30.0),
			hands=[
				PlayerHand(cards=[Card('Spades', 4), Card('Hearts', 6)], wager=15.0)]
			),
		dealer=DealerHand(cards=[Card('Clubs', 7), Card('Diamonds', 3)])
	)
	interface.clear_and_print(table)
	console = capsys.readouterr()   
	assert console.out == (
		'Dealer: 7\n'
		'♣7\n'
		'?\n'
		'--------------------\n'
		'Hand I: 10 [$15.00]\n'
		'♠4\n'
		'♥6\n'
		'--------------------\n'
		'Chips: $30.00\n'
	)
	
	# Test initial deal with insurance display.
	table.player.hands[0].insurance_wager = 7.5
	table.player.bank.chips = 22.5
	table.dealer.cards = [Card('Clubs', 'Ace'), Card('Diamonds', 3)]
	interface.clear_and_print(table)
	console = capsys.readouterr() 
	assert console.out == (
		'Dealer: 11\n'
		'♣Ace\n'
		'?\n'
		'Insurance [$7.50]\n'
		'--------------------\n'
		'Hand I: 10 [$15.00]\n'
		'♠4\n'
		'♥6\n'
		'--------------------\n'
		'Chips: $22.50\n'
	)

def test_print_player_hands_dealer_showing(capsys):
	# Test dealer showing both cards, non-soft.
	player_hand1 = PlayerHand(
		cards=[Card('Clubs', 4), Card('Spades', 6), Card('Hearts', 9)],
		wager=30.0
	)
	dealer_hand = DealerHand(
		cards=[Card('Diamonds', 4), Card('Hearts', 6), Card('Spades', 7)],
		is_hidden=False
	)
	table = Table(
		player=Player(username='Test', hands=[player_hand1], bank = Bank(50.0)), 
		dealer=dealer_hand
	)
	interface.clear_and_print(table)
	console = capsys.readouterr()   
	assert console.out == (
		'Dealer: 17\n'
		'♦4\n'
		'♥6\n'
		'♠7\n'
		'--------------------\n'
		'Hand I: 19 [$30.00]\n'
		'♣4\n'
		'♠6\n'
		'♥9\n'
		'--------------------\n'
		'Chips: $50.00\n'
	)

	# Test dealer showing both cards, soft.
	table.dealer.cards = [Card('Diamonds', 4), Card('Spades', 'Ace')]
	interface.clear_and_print(table)
	console = capsys.readouterr()   
	assert console.out == (
		'Dealer: 5 / 15\n'
		'♦4\n'
		'♠Ace\n'
		'--------------------\n'
		'Hand I: 19 [$30.00]\n'
		'♣4\n'
		'♠6\n'
		'♥9\n'
		'--------------------\n'
		'Chips: $50.00\n'
	)

def test_print_split_player_hands(capsys):
	# Split when hand I is active.
	player_hand1 = PlayerHand(
		cards=[Card('Clubs', 6), Card('Spades', 'Jack')],
		wager=40.0,
		is_active=True
	)
	player_hand2 = PlayerHand(
		cards=[Card('Spades', 6), Card('Spades', 'Ace')],
		wager=40.0
	)
	dealer_hand = DealerHand(
		cards=[Card('Diamonds', 4), Card('Hearts', 6), Card('Spades', 7)],
		is_hidden=False
	)
	table = Table(
		player=Player(
			username='Test', 
			hands=[player_hand1, player_hand2], 
			bank = Bank(50.0)
		), 
		dealer=dealer_hand
	)
	interface.clear_and_print(table)
	console = capsys.readouterr()   
	assert console.out == (
		'Dealer: 17\n'
		'♦4\n'
		'♥6\n'
		'♠7\n'
		'--------------------\n'
		'Hand I: 16 [$40.00] <- Active\n'
		'♣6\n'
		'♠Jack\n'
		'--------------------\n'
		'Hand II: 7 / 17 [$40.00]\n'
		'♠6\n'
		'♠Ace\n'
		'--------------------\n'
		'Chips: $50.00\n'
	)

	# Split when hand II is active.
	table.player.hands[1].is_active = True
	table.player.hands[0].is_active = False
	interface.clear_and_print(table)
	console = capsys.readouterr()   
	assert console.out == (
		'Dealer: 17\n'
		'♦4\n'
		'♥6\n'
		'♠7\n'
		'--------------------\n'
		'Hand I: 16 [$40.00]\n'
		'♣6\n'
		'♠Jack\n'
		'--------------------\n'
		'Hand II: 7 / 17 [$40.00] <- Active\n'
		'♠6\n'
		'♠Ace\n'
		'--------------------\n'
		'Chips: $50.00\n'
	)

def test_initial_outcome_display(capsys):
	hand = PlayerHand(wager=15.0)
	outcome = Outcome(flag=constants.PUSH)
	interface.print_initial_outcome(outcome, hand)    
	console = capsys.readouterr()
	assert console.out == 'Round Push, Returned $15.00\n'
	outcome.flag = constants.PLAYER_WIN
	outcome.payout = payout_calculator.blackjack_payout(hand)
	interface.print_initial_outcome(outcome, hand)
	console = capsys.readouterr()
	assert console.out == 'Player Blackjack, You Won $37.50\n'
	outcome.flag = constants.DEALER_WIN
	interface.print_initial_outcome(outcome, hand)
	console = capsys.readouterr()
	assert console.out == 'Dealer Blackjack, You Lose\n'
	outcome.flag = 0
	interface.print_initial_outcome(outcome, hand)
	console = capsys.readouterr()
	assert console.out == ''


def test_initial_insurance_outcome_display(capsys):
	insurance = Insurance(active=True, win=True, payout=15.0)
	interface.print_initial_insurance_outcome(insurance)
	console = capsys.readouterr()
	assert console.out == 'You Won $15.00 With Insurance.\n'
	insurance.active = True
	insurance.win = False
	interface.print_initial_insurance_outcome(insurance)
	console = capsys.readouterr()
	assert console.out == 'No Dealer Blackjack, Insurance Lost.\n'
	insurance.active = False
	interface.print_initial_insurance_outcome(insurance)
	console = capsys.readouterr()
	assert console.out == ''

def test_hit_or_stand(mock_inputs, capsys):
	mock_inputs(['hit', 'n', '4', 'h'])

	choice = interface.hit_or_stand()

	console = capsys.readouterr()
	assert 'Invalid Choice, (H) HIT / (S) STAND\n' in console.out
	assert console.out.count('Invalid Choice, (H) HIT / (S) STAND\n') == 3
	assert choice == 'H'

	mock_inputs(['t', 'g', 'sadfa', 'stand', 's'])

	choice = interface.hit_or_stand()

	console = capsys.readouterr()
	assert 'Invalid Choice, (H) HIT / (S) STAND\n' in console.out
	assert console.out.count('Invalid Choice, (H) HIT / (S) STAND\n') == 4
	assert choice == 'S'

# def test_add_chips()

# def test_new_round_decision(mock_inputs, capsys):

# def test_wager_prompt(mock_inputs, capsys):

# def test_wager_prompt_helper():

# def test_clear_terminal():

# def test_load_timer():

# def test_display_dealer_state

# def test_get_round_outcome_msg

# def test_get_round_outcome_payout_msg

# def test_print_stand_or_bust():

