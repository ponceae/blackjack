""" 
This function tests the game module including main game loop.

Author: Adrien P.
"""

import pytest
import time

from blackjack.actions import create_and_shuffle, hit_hand
from blackjack.bank import Bank
from blackjack.card import Card
from blackjack import constants
from blackjack.datatypes import (
	DealerHand, 
	Insurance, 
	Outcome, 
	PlayerAction,
	Player, 
	PlayerHand, 
	SplitHands,
	Table,
)
from blackjack import game
from blackjack import interface

@pytest.fixture
def mock_inputs(monkeypatch):
	def _mock_inputs(values):
		inputs = iter(values)
		def mock_input(prompt):
			try:
				return next(inputs)
			except StopIteration:
				pytest.fail(f'Test ran out of mock inputs.\nLast Prompt: {prompt}\n')
		monkeypatch.setattr('builtins.input', mock_input)
	return _mock_inputs

# ==================================================
# INITIAL ROUND TESTS
# ==================================================

@pytest.fixture
def init_table():
	return Table(
		player=Player(
			username='Test',
			bank=Bank(25.0),
			hands=[
				PlayerHand(
					cards=[Card('Hearts', 6), Card('Clubs', 4)],
					wager= 15.0,
				), 
			],
		),
		dealer=DealerHand(cards=[Card('Diamonds', 'Ace'), Card('Spades', 5)]),
	)

@pytest.mark.parametrize(
		'insurance, inputs, bank, is_active, expected_cost, expected_chips',
		[
			(Insurance(), ['y'], 25.0, True, 7.5, 17.5),
			(Insurance(), ['n'], 5.0, False, 0.0, 5.0),
			(Insurance(), ['n'], 25.0, False, 0.0, 25.0),
		],
		ids=[
			'insurance_purchased',
			'invalid_bank',
			'insurance_denied',
		],
)
def test_handle_insurance_on_init_deal_not_broke_bank(
		monkeypatch, 
		mock_inputs, 
		init_table,
		insurance,
		inputs,
		bank,
		is_active,
		expected_cost,
		expected_chips,
):
	init_table.player.bank = Bank(bank)
	mock_inputs(inputs)
	monkeypatch.setattr(time, 'sleep', lambda x: None)
	game.handle_insurance(insurance, init_table)
	
	assert insurance.active == is_active
	assert init_table.player.hands[0].insurance_wager == expected_cost
	assert init_table.player.bank.chips == expected_chips

def test_insurance_helper_on_init_deal(monkeypatch, mock_inputs, init_table):
	insurance = Insurance(active=True)
	mock_inputs(['y'])
	monkeypatch.setattr(time, 'sleep', lambda x: None)
	
	game.handle_insurance(insurance, init_table)
	game.insurance_helper(insurance, init_table)
	assert init_table.player.bank.chips == 32.5

@pytest.mark.parametrize(
		'outcome_flag, expected_payout, expected_chips',
		[
			(constants.DEALER_WIN, 0.0, 25.0),
			(constants.PUSH, 15.0, 40.0),
			(constants.PLAYER_WIN, 37.5, 62.5),
		],
)
def test_handle_outcomes_on_init_deal(
		monkeypatch,
		init_table,
		outcome_flag,
		expected_payout,
		expected_chips,
):
	outcome = Outcome(flag=outcome_flag)
	monkeypatch.setattr(game, 'insurance_helper', lambda *args, **kwargs: None)
	game.handle_outcomes(outcome, Insurance(), init_table)
	
	assert outcome.payout == expected_payout
	assert init_table.player.bank.chips == expected_chips

def test_exe_init_cond_insurance_no_blackjack(monkeypatch, mock_inputs, init_table):
	mock_inputs(['y'])
	monkeypatch.setattr(time, 'sleep', lambda x: None)
	game.exe_initial_cond(init_table)
	assert init_table.player.bank.chips == 17.5

def test_exe_init_cond_player_blackjack(monkeypatch, mock_inputs, init_table):
	init_table.player.hands[0].cards = [Card('Spades', 10), Card('Spades', 'Ace')]
	mock_inputs(['n'])
	monkeypatch.setattr(time, 'sleep', lambda x: None)
	monkeypatch.setattr(interface, 'is_new_round', lambda *args, **kwargs: None)
	
	game.exe_initial_cond(init_table)
	assert init_table.player.bank.chips == 62.5
 
def test_exe_init_cond_no_dealer_blackjack_insurance_lost(
		monkeypatch, 
		 mock_inputs, 
		  init_table
):
	mock_inputs(['y'])
	monkeypatch.setattr(time, 'sleep', lambda x: None)
	monkeypatch.setattr(interface, 'is_new_round', lambda *args, **kwargs: None)
	
	game.exe_initial_cond(init_table)
	assert init_table.player.bank.chips == 17.5

# ==================================================
# PLAYER TURN TESTS
# ==================================================

@pytest.fixture
def pt_table():
	return Table(
		player=Player(
			username='Test',
			bank=Bank(25.0),
			hands=[
				PlayerHand(
					cards=[Card('Hearts', 5), Card('Clubs', 5)],
					wager= 15.0,
				), 
			],
		),
		dealer=DealerHand(cards=[Card('Diamonds', 4), Card('Spades', 5)]),
		deck=create_and_shuffle()
	)

@pytest.mark.parametrize(
	'cards, expected_chips, str_a, str_b, split_ace',
	[
		([Card('Hearts', 5), Card('Clubs', 5)], 10.0, '♥5', '♣5', False),
		([Card('Hearts', 'Ace'), Card('Clubs', 'Ace')], 10.0, '♥Ace', '♣Ace', True)
	],
)
def test_handle_split_hands_normal_path(
		mock_inputs, 
		pt_table,
		cards,
		expected_chips,
		str_a,
		str_b,
		split_ace,
):
	mock_inputs(['y'])
	split_status = SplitHands()
	pt_table.player.hands[0].cards = cards
 
	game.handle_split(pt_table, split_status)
	assert pt_table.player.bank.chips == expected_chips
	assert pt_table.player.hands[0].cards[0].to_string() == str_a
	assert pt_table.player.hands[1].cards[0].to_string() == str_b
	assert pt_table.player.hands[1].wager == pt_table.player.hands[0].wager
	assert split_status.split_hand == True
	assert split_status.split_aces == split_ace

@pytest.mark.parametrize(
	'input, bank',
	[
		(['n'], 25.0),
		(['y'], 10.0),
	],
	ids=[
		'split_hand_deny',
		'cannot_afford_split',
	],
)
def test_handle_split_hands_unhappy_path(
		monkeypatch,
		mock_inputs, 
		pt_table, 
		input, 
		bank
):
	split_status = SplitHands()
	pt_table.player.bank = Bank(bank)
	mock_inputs(input)
	monkeypatch.setattr(time, 'sleep', lambda x: None)
	game.handle_split(pt_table, split_status)
	
	assert pt_table.player.bank.chips == bank
	assert pt_table.player.hands[0].cards[0].to_string() == '♥5'
	assert pt_table.player.hands[0].cards[1].to_string() == '♣5'
	assert len(pt_table.player.hands) == 1
	assert split_status.split_hand == False


@pytest.mark.parametrize(
	'is_split, index, hands, expected_bool',
	[
		(
			True, 
			0, 
			[
       			[Card('Clubs', 4), Card('Hearts', 5)], 
          		[],
            ],
			True,
		),
		(
			False,
			0, 
			[
       			[Card('Clubs', 4), Card('Hearts', 5)],
				[Card('Spades', 6), Card('Clubs', 7)],
			],
			False
		),
		(
			True,
			1,
			[
       			[], 
				[Card('Spades', 6), Card('Clubs', 7)],
			],
			False
		),
	],
	ids=[
		'split_hands_hand_left',
		'non_split_hand_no_more_hands',
		'split_hand_no_hands_left'
	]
)
def test_hands_left(monkeypatch, is_split, index, hands, expected_bool):
	hands = hands
	split_status = SplitHands(split_hand=is_split)
	monkeypatch.setattr(time, 'sleep', lambda x: None)
	
	assert game.hands_left(split_status, hands, index) == expected_bool

@pytest.mark.parametrize(
	'is_split, hand1, hand2, index, expected_action',
	[
		(
			True,
       		[], 
			[Card('Clubs', 4), Card('Hearts', 5)],
			1,
			PlayerAction.END_TURN,
       	),
		(
			True,
			[Card('Clubs', 5), Card('Hearts', 6)], 
			[],
			0,
			PlayerAction.NEXT_HAND,	
		),
		(
			False,
			[Card('Clubs', 5), Card('Hearts', 6)], 
			[],
			0,
			PlayerAction.END_TURN,	
		),
	],
	ids=[
		'split_hand_double_down_no_hands_left',
		'split_hand_double_down_hand_left',
		'non_split_hand_double_down',
	]
)
def test_handle_double_down(monkeypatch, pt_table, is_split, hand1, hand2, index, expected_action):
	# Main PT function handles affordability of doubling down.
	pt_table.player.hands = [
    	PlayerHand(cards=hand1, wager=15.0), 
     	PlayerHand(cards=hand2, wager=15.0),
    ]
	split_status = SplitHands(split_hand=is_split)
	monkeypatch.setattr(time, 'sleep', lambda x: None)
	action = game.handle_double_down(pt_table, index, split_status)

	assert pt_table.player.hands[index].wager == 30.0
	assert pt_table.player.bank.chips == 10.0
	assert action == expected_action
	assert len(pt_table.player.hands[index].cards) == 3

@pytest.mark.parametrize(
	'inputs, is_split, hand1, hand2, index, card, expected_prev, expected_action',
	[
		(
      		['h', 's'], 
        	True, 
         	[Card('Spades', 6), Card('Hearts', 4)], 
          	[], 
           	0,
            Card('Hearts', 8),
            constants.STAND,
            PlayerAction.NEXT_HAND
        ),
		(
			['h'],
			True,
			[],
			[Card('Spades', 10), Card('Hearts', 5)],
			1,
			Card('Hearts', 9),
			constants.BUST,
			PlayerAction.END_TURN,
       	),
		(
			['h'],
			True,
			[Card('Spades', 10), Card('Hearts', 5)],
			[],
			0,
			Card('Hearts', 9),
			constants.BUST,
			PlayerAction.NEXT_HAND,
      	),
		(
			['h'],
			True,
			[Card('Spades', 10), Card('Hearts', 5)],
			[],
			0,
			Card('Hearts', 6),
			constants.STAND,
			PlayerAction.NEXT_HAND,
      	),
		(
			['h'],
			False,
			[Card('Spades', 10), Card('Hearts', 5)],
			[],
			0,
			Card('Hearts', 6),
			constants.STAND,
			PlayerAction.END_TURN,
      	),
	],
	ids=[
		'hit_once_then_stand_on_split_hand',
		'hit_once_and_bust_on_non_split',
		'hit_once_and_bust_on_split_hand_left',
		'hit_once_and_stand_on_split_hand_left',
		'hit_once_and_stand_on_non_split_no_hand_left',
	],
)
def test_handle_hitting(
		monkeypatch, 
		mock_inputs, 
		pt_table, 
		inputs, 
  		is_split, 
    	hand1, 
     	hand2, 
      	index, 
		card,
       	expected_prev, 
        expected_action
):
    pt_table.player.hands = [PlayerHand(cards=hand1), PlayerHand(cards=hand2)]
    split_status = SplitHands(split_hand=is_split)
    mock_inputs(inputs)
    
    def rigged_hit(a, b):
        pt_table.player.hands[index].cards.append(card)
        
    monkeypatch.setattr(time, 'sleep', lambda x: None)
    monkeypatch.setattr('blackjack.actions.hit_hand', rigged_hit)
    
    prev_action, action = game.handle_hitting(
        						pt_table, 
              					split_status, 
                   				pt_table.player.hands[index], 
                       			index,
                        )
    
    assert prev_action == expected_prev
    assert action == expected_action
 
def test_exe_player_control_split_ace_early_exit(mock_inputs, pt_table):
    pt_table.player.hands = [
        PlayerHand(cards=[Card('Spades', 'Ace'), Card('Diamonds', 'Ace')])
    ]
    mock_inputs(['y'])    
    game.exe_player_control(pt_table)
    
    assert pt_table.player.hands[0].cards[0].rank == 'Ace'
    assert pt_table.player.hands[1].cards[0].rank == 'Ace'
    assert len(pt_table.player.hands[0].cards) == 2
    assert len(pt_table.player.hands[1].cards) == 2

# @pytest.mark.parametrize(
# 	'inputs, hand1, hand2, action',
# 	[
# 		(
# 			['y'],
# 			[Card('Diamonds', 'Ace'), Card('Hearts', 4)],
# 			[],
# 			PlayerAction.END_TURN
#       	),
# 	],
# 	ids=[
# 		'double_down_on_hand1',
# 		'double_down_on_hand2',
# 	],
# )
# def test_exe_player_control(monkeypatch, mock_inputs, inputs, hand1, hand2, action):
# 	split_status = SplitHands()
# 	monkeypatch.setattr(game, 'handle_split', lambda *args, **kwargs: None)
# 	curr_action = None
# 	def dummy_double_down():
# 		curr_action = action
 
# 	monkeypatch.setattr(game, 'handle_double_down', lambda *args, **kwargs: None)