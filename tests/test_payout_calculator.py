"""
Tests for the payout calculator module.

Author: Adrien P.
"""

import pytest

from blackjack.bank import Bank
from blackjack import payout_calculator
from blackjack.datatypes import Insurance, Player, PlayerHand

def test_blackjack_payouts():
    hand = PlayerHand(wager=15.0)
    assert payout_calculator.blackjack_payout(hand) == 37.5
    hand.wager = 1000
    assert payout_calculator.blackjack_payout(hand) == 2500.0
    hand.wager = 534.25
    assert payout_calculator.blackjack_payout(hand) == 1335.625

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

def test_get_insurance_cost():
    hand = PlayerHand(wager=15)
    assert payout_calculator.get_insurance_cost(hand) == 7.5
    hand.wager = 27.5
    assert payout_calculator.get_insurance_cost(hand) == 13.5

def test_push_payout():
    hand = PlayerHand(wager=15)
    assert payout_calculator.push_payout(hand) == 15.0
    hand.wager = 345.75
    assert payout_calculator.push_payout(hand) == 345.75

def test_standard_win_payout():
    hand = PlayerHand(wager=15)
    assert payout_calculator.standard_payout(hand) == 30.0
    hand.wager = 345.75
    assert payout_calculator.standard_payout(hand) == 691.50
    