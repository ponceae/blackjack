""" 
Tests for the conditions module.

Author: Adrien P.
"""

import pytest

from blackjack.bank import Bank
from blackjack import conditions
from blackjack import constants
from blackjack.datatypes import DealerHand, Hand, Player, PlayerHand, Table
from blackjack.card import Card

@pytest.mark.parametrize(
        'cards, expected_bool',
        [
            ([Card('Clubs', 8), Card('Hearts', 8)], True),
            ([Card('Spades', 'Ace'), Card('Diamonds', 'Ace')], True),
            ([Card('Hearts', 'King'), Card('Clubs', 'Queen')], False),
            ([Card('Hearts', 9), Card('Clubs', 4)], False),
        ],
)
def test_can_split_hand(cards, expected_bool):
    test_hand = Hand(cards=cards)
    assert conditions.can_split(test_hand) == expected_bool

@pytest.mark.parametrize(
        'player_cards, dealer_cards, expected_flag',
        [
            (
                [Card('Clubs', 'Ace'), Card('Hearts', 10)], 
                [Card('Spades', 'Ace'), Card('Diamonds', 10)], 
                constants.PUSH
            ),
            (
                [Card('Clubs', 'Ace'), Card('Hearts', 10)],
                [Card('Spades', 2), Card('Diamonds', 10)],
                constants.PLAYER_WIN,
            ),
            (
                [Card('Clubs', 2), Card('Hearts', 10)],
                [Card('Spades', 'Ace'), Card('Diamonds', 10)],
                constants.DEALER_WIN,
            ),
            (
                [Card('Clubs', 2), Card('Hearts', 10)],
                [Card('Spades', 4), Card('Diamonds', 10)],
                0,
            ),
        ],
        ids=[
            'test_initial_push',
            'test_initial_player_win',
            'test_initial_dealer_win',
            'test_no_initial_winner',
        ],
)
def test_initial_hands_outcome_flags(player_cards, dealer_cards, expected_flag):
    test_table = Table(
        player=Player(
            username='Test',
            hands=[PlayerHand(cards=player_cards)]
        ),
        dealer=DealerHand(cards=dealer_cards)
    )
    assert conditions.compare_initial_hands(test_table) == expected_flag

@pytest.mark.parametrize(
        'cards, expected_bool',
        [
            ([Card('Clubs', 8), Card('Hearts', 8), Card('Diamonds', 8)], True),
            ([Card('Spades', 'Ace'), Card('Diamonds', 5)], False),
            ([Card('Spades', 10), Card('Clubs', 5), Card('Hearts', 10)], True),
            ([Card('Hearts', 'Ace'), Card('Clubs', 'Ace'), Card('Spades', 10)], False),
            (
                [
                    Card('Clubs', 3), 
                    Card('Hearts', 4), 
                    Card('Spades', 7), 
                    Card('Clubs', 4),
                ], 
            False
            ),
        ],
        ids=[
            'three_card_bust_a',
            'ace_two_card_nonbust',
            'three_card_bust_b',
            'two_ace_three_card_nonbust',
            'four_card_nonbust',
        ],
)
def test_is_bust_hand(cards, expected_bool):
    test_hand = Hand(cards=cards)
    assert conditions.is_bust(test_hand) == expected_bool

@pytest.mark.parametrize(
    'cards, expected_bool',
    [
        ([Card('Clubs', 8), Card('Hearts', 4)], False),
        ([Card('Spades', 'Ace'), Card('Diamonds', 5)], True),
    ],
    ids=[
        'is_not_soft_a',
        'is_soft_a',
    ],
)
def test_is_soft_hand(cards, expected_bool):
    test_hand = Hand(cards=cards)
    assert conditions.is_soft(test_hand) == expected_bool

@pytest.mark.parametrize(
        'cards, expected_bool',
        [
            ([Card('Clubs', 'Ace'), Card('Hearts', 'Ace')], True),
            ([Card('Spades', 5), Card('Diamonds', 5)], False),
            ([Card('Clubs', 8), Card('Hearts', 10)], False),
        ],
        ids=[
            'is_split_ace_hand_a',
            'not_split_ace_hand_a',
            'not_split_ace_hand_b',
        ],
)
def test_hand_is_split_aces(cards, expected_bool):
    test_hand = Hand(cards=cards)
    assert conditions.is_split_aces(test_hand) == expected_bool

@pytest.mark.parametrize(
        'cards, expected_bool',
        [
            ([Card('Clubs', 7), Card('Hearts', 8), Card('Clubs', 6)], True),
            ([Card('Spades', 5), Card('Diamonds', 10)], False),
        ],
        ids=[
            'hand_is_twenty_one_a',
            'hand_not_twenty_one_b',
        ],
)  
def test_is_twenty_one_hand(cards, expected_bool):
    test_hand = Hand(cards=cards)
    assert conditions.is_twenty_one(test_hand) == expected_bool

@pytest.fixture
def player():
    return Player(username='Test', bank=Bank(25.0)) 

@pytest.mark.parametrize(
        'wager, expected_bool',
        [
            (15.0, True),
            (35, False),
            (-3.2, False),
            (0, False),
            (14.99, False),
        ],
)
def test_is_valid_wager(player, wager, expected_bool):
    assert conditions.is_valid_wager(player, wager) == expected_bool

@pytest.mark.parametrize(
        'chips, expected_bool',
        [
            (15, True),
            (1000.0, True),
            (14.99, False),
            (1000.01, False),
            (500, True),
            (27.5, True),
            (-33.6, False),
        ],
)
def test_verify_chip_bounds(chips, expected_bool):
    assert conditions.verify_chip_bounds(chips) == expected_bool

@pytest.mark.parametrize(
    'chips, expected_bool',
    [
        (15, True),
        (27.5, True),
        (14.99, False),
        (0, False),
        (-4.3, False),
        (5, False),
    ],
)
def test_verify_chip_count(chips, expected_bool):
    assert conditions.verify_chip_count(chips) == expected_bool

@pytest.mark.parametrize(
    'bank, wager, expected_bool',
    [
        (50.0, 25.0, True),
        (25.0, 50.0, False),
        (0.0, 50.0, False),
    ],
)   
def test_verify_doubled_wager(bank, wager, expected_bool):
    player = Player(username='Test', bank=Bank(bank))
    player_hand = PlayerHand(wager=wager)   
    assert conditions.verify_doubled_wager(player, player_hand) == expected_bool 

@pytest.mark.parametrize(
    'bank, wager, expected_bool',
    [
        (25.0, 15.0, True),
        (5.0, 15.0, False),
    ],
)  
def test_verify_insurance_bet(bank, wager, expected_bool):
    player = Player(username='Test', bank=Bank(bank))
    player_hand = PlayerHand(wager=wager)
    assert conditions.verify_insurance_bet(player, player_hand) == expected_bool

@pytest.mark.parametrize(
    'wager, expected_bool',
    [
        (15.0, True),
        (10, False),
        (16, True),
    ],
)  
def test_verify_min_bet(wager, expected_bool):
    player_hand = PlayerHand(wager=wager)  
    assert conditions.verify_min_bet(player_hand) == expected_bool
    