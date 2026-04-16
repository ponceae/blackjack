"""
Tests for the payout calculator module.

Author: Adrien P.
"""

import pytest

from blackjack.bank import Bank
from blackjack import payout_calculator
from blackjack.datatypes import Insurance, Player, PlayerHand

@pytest.mark.parametrize(
    'wager, expected_payout',
    [
        (15.0, 37.5),
        (1000, 2500.0),
        (534.25, 1335.625),
    ]
)
def test_blackjack_payouts(wager, expected_payout):
    hand = PlayerHand(wager=wager)
    assert payout_calculator.blackjack_payout(hand) == expected_payout

def test_insurance_logic_and_bank_update_low_cost():
    insurance = Insurance(cost=7.5)
    player = Player(username='Test', bank=Bank(15.0))
    payout_calculator.insurance_logic(insurance, player)
    
    assert insurance.payout == 15.0
    assert player.bank.chips == 30.0

def test_insurance_logic_and_bank_update_high_cost():
    insurance = Insurance(cost=27.5)
    player = Player(username='Test', bank=Bank(25.0))
    payout_calculator.insurance_logic(insurance, player)
    
    assert insurance.payout == 55.0
    assert player.bank.chips == 80.0

@pytest.mark.parametrize(
    'wager, expected_cost',
    [
        (15, 7.5),
        (27.5, 13.5),
        (346.34, 173.0),
        (4635.32, 2317.5), 
    ]
)
def test_get_insurance_cost(wager, expected_cost):
    hand = PlayerHand(wager=wager)
    assert payout_calculator.get_insurance_cost(hand) == expected_cost

@pytest.mark.parametrize(
    'wager, expected_payout',
    [
        (15, 15.0),
        (345.75, 345.75),
    ]
)
def test_push_payout(wager, expected_payout):
    hand = PlayerHand(wager=wager)
    assert payout_calculator.push_payout(hand) == expected_payout

@pytest.mark.parametrize(
    'wager, expected_payout',
    [
        (15, 30.0),
        (345.75, 691.5),
    ]
)
def test_standard_win_payout(wager, expected_payout):
    hand = PlayerHand(wager=wager)
    assert payout_calculator.standard_payout(hand) == expected_payout
    