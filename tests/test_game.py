""" 
This function tests the game module including main game loop.
"""

import pytest
import time

from blackjack.bank import Bank
from blackjack.card import Card
from blackjack import constants
from blackjack.datatypes import (
    DealerHand, 
    Insurance, 
    Outcome, 
    Player, 
    PlayerHand, 
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
					wager= 15.0
				) 
			]
		),
		dealer=DealerHand(cards=[Card('Diamonds', 'Ace'), Card('Spades', 5)])
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
		]
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
		]
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