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

@pytest.fixture
def mock_inputs(monkeypatch):
	def _mock_inputs(values):
		inputs = iter(values)
		def mock_input(prompt):
			try:
				return next(inputs)
			except StopIteration:
				pytest.fail(f'Test ran out of mock inputs.\nPrompt: {prompt}\n'
				)
		monkeypatch.setattr('builtins.input', mock_input)
	return _mock_inputs

@pytest.mark.parametrize(
	'function, args, expected_choice',
	[
		(interface.double_or_not, [], 'Y'),
		(interface.request_chips, [], 'Y'),
		(interface.request_insurance, [7.5], 'Y'),
		(interface.request_new_round, [], 'Y'),
		(interface.split_or_not, [], 'Y'),
	]
)
def test_yes_flow(mock_inputs, capsys, function, args, expected_choice):
	mock_inputs(['yes', '0', 'sadf', 'y'])
	choice = function(*args)
	console = capsys.readouterr()
	assert console.out.count('Invalid Choice, (Y) YES / (N) NO\n') == 3
	assert choice == expected_choice

@pytest.mark.parametrize(
	'function, args, expected_choice',
	[
		(interface.double_or_not, [], 'N'),
		(interface.request_chips, [], 'N'),
		(interface.request_insurance, [7.5], 'N'),
		(interface.request_new_round, [], 'N'),
		(interface.split_or_not, [], 'N'),
	]
)
def test_no_flow(mock_inputs, capsys, function, args, expected_choice):
	mock_inputs(['no', '0', 'sadf', 'n'])
	choice = function(*args)
	console = capsys.readouterr()
	assert console.out.count('Invalid Choice, (Y) YES / (N) NO\n') == 3
	assert choice == expected_choice

@pytest.mark.parametrize(
	'player_cards, player_wager, index, dealer_cards, expected_msg, expected_flag',
	[
		(
			[Card('Spades', 5), Card('Clubs', 5)], 
			15.0,
			0,
			[Card('Diamonds', 4), Card('Hearts', 6), Card('Spades', 7)],
			'Hand I Lost\n',
			constants.DEALER_WIN,
		),
		(
			[Card('Spades', 5), Card('Clubs', 5), Card('Hearts', 7)], 
			15.0,
			1,
			[Card('Diamonds', 4), Card('Hearts', 6), Card('Spades', 7)],
			'Hand II Push, Returned $15.00\n',
			constants.PUSH,
		),
		(
			[Card('Spades', 5), Card('Clubs', 5), Card('Hearts', 8)], 
			15.0,
			1,
			[Card('Diamonds', 4), Card('Hearts', 6), Card('Spades', 7)],
			'Hand II Win, You Won $30.00\n',
			constants.PLAYER_WIN,	
		),
	]
)
def test_compare_hands_output(
	player_cards, player_wager, index, dealer_cards, expected_msg, expected_flag
):
	if index == 0:
		player_hand1 = PlayerHand(cards=player_cards, wager=player_wager)
		player_hand2 = PlayerHand(cards=[], wager=0.0)
	elif index == 1:
		player_hand1 = PlayerHand(cards=[], wager=0.0)
		player_hand2 = PlayerHand(cards=player_cards, wager=player_wager)
	table = Table(
		player=Player(username='Test', hands=[player_hand1, player_hand2]),
		dealer=DealerHand(cards=dealer_cards)
	)
	msg, flag = interface.compare_hands(table, table.player.hands[index], index)
	assert msg == expected_msg
	assert flag == expected_flag

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
def test_print_player_hands_init_deal_with_insurance(capsys):
	# Test initial deal with insurance display.
	table = Table (
		player=Player(
			username='Test',
			bank=Bank(22.5),
			hands=[
					PlayerHand(
						cards=[Card('Spades', 4), Card('Hearts', 6)], 
						wager=15.0,
						insurance_wager=7.5,
					)
				]
			),
		dealer=DealerHand(cards=[Card('Clubs', 'Ace'), Card('Diamonds', 3)])
	)
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

@pytest.mark.parametrize(
	'cards, bank, wager, dealer_cards, expected_display',
	[
		(
			[Card('Clubs', 4), Card('Spades', 6), Card('Hearts', 9)],
			50.0,
			30.0,
			[Card('Diamonds', 4), Card('Hearts', 6), Card('Spades', 7)],
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
			'Chips: $50.00\n',
		),
		(
			[Card('Clubs', 6), Card('Spades', 4), Card('Hearts', 9)],
			50.0,
			30.0,
			[Card('Diamonds', 4), Card('Hearts', 'Ace')],
			'Dealer: 5 / 15\n'
			'♦4\n'
			'♥Ace\n'
			'--------------------\n'
			'Hand I: 19 [$30.00]\n'
			'♣6\n'
			'♠4\n'
			'♥9\n'
			'--------------------\n'
			'Chips: $50.00\n'
		),
	],
	ids=[
		'dealer_non_soft_hand',
		'dealer_soft_hand',
	]
)
def test_print_player_hands_dealer_showing_soft_and_non_soft(
		capsys, cards, bank, wager, dealer_cards, expected_display
):
	# Test dealer showing both cards, non-soft.
	player_hand1 = PlayerHand(
		cards=cards,
		wager=wager
	)
	table = Table(
		player=Player(username='Test', hands=[player_hand1], bank = Bank(bank)), 
		dealer=DealerHand(cards=dealer_cards, is_hidden=False)
	)
	interface.clear_and_print(table)
	console = capsys.readouterr()   
	assert console.out == expected_display

def test_print_split_player_hands_hand_one_active(capsys):
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
def test_print_split_player_hands_hand_two_active(capsys):
	# Split when hand II is active.
	player_hand1 = PlayerHand(
		cards=[Card('Clubs', 6), Card('Spades', 'Jack')],
		wager=40.0,
	)
	player_hand2 = PlayerHand(
		cards=[Card('Spades', 6), Card('Spades', 'Ace')],
		wager=40.0,
		is_active=True,
	)
	dealer_hand = DealerHand(
		cards=[Card('Diamonds', 4), Card('Hearts', 6), Card('Spades', 7)],
		is_hidden=False,
	)
	table = Table(
		player=Player(
			username='Test', 
			hands=[player_hand1, player_hand2], 
			bank = Bank(50.0),
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

@pytest.mark.parametrize(
	'wager, flag, expected_display, expected_payout',
	[
		(15.0, constants.PUSH, 'Round Push, Returned $15.00\n', 0.0),
		(15.0, constants.PLAYER_WIN, 'Player Blackjack, You Won $37.50\n', 37.5),
		(15.0, constants.DEALER_WIN, 'Dealer Blackjack, You Lose\n', 0.0),
		(15.0, 0, '', 0.0),
	]
)
def test_initial_outcome_display(
		capsys, wager, flag, expected_display, expected_payout
):
	hand = PlayerHand(wager=wager)
	outcome = Outcome(flag=flag, payout=expected_payout)
	interface.print_initial_outcome(outcome, hand)    
	console = capsys.readouterr()
	assert console.out == expected_display

@pytest.mark.parametrize(
	'active, win, payout, expected_display',
	[
		(True, True, 15.0, 'You Won $15.00 With Insurance.\n'),
		(True, False, 0.0, 'No Dealer Blackjack, Insurance Lost.\n'),
		(False, False, 0.0, ''),
	]
)
def test_initial_insurance_outcome_display(
		capsys, active, win, payout, expected_display
):
	insurance = Insurance(active=active, win=win, payout=payout)
	interface.print_initial_insurance_outcome(insurance)
	console = capsys.readouterr()
	assert console.out == expected_display

def test_hit_hand_decision(mock_inputs, capsys):
	mock_inputs(['hit', 'n', '4', 'h'])

	choice = interface.hit_or_stand()

	console = capsys.readouterr()
	assert 'Invalid Choice, (H) HIT / (S) STAND\n' in console.out
	assert console.out.count('Invalid Choice, (H) HIT / (S) STAND\n') == 3
	assert choice == 'H'

def test_stand_hand_decision(mock_inputs, capsys):
	mock_inputs(['t', 'g', 'sadfa', 'stand', 's'])

	choice = interface.hit_or_stand()

	console = capsys.readouterr()
	assert 'Invalid Choice, (H) HIT / (S) STAND\n' in console.out
	assert console.out.count('Invalid Choice, (H) HIT / (S) STAND\n') == 4
	assert choice == 'S'

@pytest.mark.parametrize(
	'input_list, bank, expected_chips',
	[
		(
			['y', '10', '35'],
			10.0,
			45.0,
		),
		(
			['n', '10', '10'],
			10.0,
			10.0
		)
	]
)
def test_add_chips_to_player_bank(mock_inputs, input_list, bank, expected_chips):
	test_player = Player(username='Test', bank=Bank(bank))
	mock_inputs(input_list)
	interface._add_chips(test_player)
	assert test_player.bank.chips == expected_chips
 
def test_is_new_round_continue(mock_inputs):
	table = Table(Player(username='Test'))
	mock_inputs(['y'])
	assert interface.is_new_round(table) == True
	
def test_exit_round_and_save_to_json(mock_inputs, monkeypatch):
	table = Table(Player(username='Test'))
	mock_inputs(['n', '50'])
	monkeypatch.setattr('json.dumps', lambda data, **kwargs: '{}')
	with pytest.raises(SystemExit) as exe_info:
		interface.is_new_round(table)
	assert exe_info.value.code is None

# def test_new_round_decision(mock_inputs, capsys):

# def test_wager_prompt(mock_inputs, capsys):

# def test_wager_prompt_helper():

# def test_clear_terminal():

# def test_load_timer():

# def test_display_dealer_state

# def test_get_round_outcome_msg

# def test_get_round_outcome_payout_msg

# def test_print_stand_or_bust():
