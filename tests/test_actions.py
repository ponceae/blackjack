""" 
Tests for the actions module.

Author: Adrien P.
"""

import pytest

from blackjack.card import Card
from blackjack import actions
from blackjack.datatypes import Hand, Player, PlayerHand, Table

@pytest.mark.parametrize(
    'cards, expected_value',
    [
        ([Card('Clubs', 2), Card('Hearts', 3), Card('Spades', 4)], 9),
        ([Card('Clubs', 10), Card('Hearts', 'Jack')], 20),
        ([Card('Clubs', 7), Card('Hearts', 8), Card('Spades', 9)], 24),
        ([Card('Clubs', 'Ace'), Card('Hearts', 5)], 16),
        ([Card('Clubs', 'Ace'), Card('Spades', 'King')], 21),
        ([Card('Clubs', 'Ace'), Card('Hearts', 2), Card('Spades', 3)], 16),
        ([Card('Clubs', 2), Card('Hearts', 9), Card('Spades', 'Ace')], 12),
        ([Card('Clubs', 'Ace'), Card('Hearts', 'Ace')], 12),
        ([Card('Clubs', 'Ace'), Card('Hearts', 'Ace'), Card('Spades', 9)], 21),
        ([Card('Clubs', 'Ace'), Card('Hearts', 'Ace'), Card('Spades', 'King')], 12),
        (
            [
                Card('Clubs', 'Ace'), 
                Card('Hearts', 'Ace'), 
                Card('Spades', 'Ace'), 
                Card('Diamonds', 'Ace')
            ], 
            14
        ),
        ([Card('Clubs', 'Ace'), Card('Hearts', 9)], 20),
        ([Card('Clubs', 'Ace'), Card('Hearts', 4), Card('Spades', 6)], 21),
        ([Card('Clubs', 'Ace'), Card('Hearts', 5), Card('Spades', 6)], 12),
    ],   
    ids=[
        'two_pip_cards',
        'one_pip_one_face_card',
        'three_pips',
        'ace_one_pip_card_a',
        'ace_one_pip_one_face_card',
        'ace_two_pip_cards_a',
        'ace_two_pip_cards_b',
        'two_aces',
        'two_aces_one_pip_card',
        'two_aces_one_face_card',
        'four_aces',
        'ace_one_pip_card_b',
        'ace_two_pip_cards_c',
        'ace_two_pip_cards_d',
    ]
)
def test_hard_hand_values(cards, expected_value):
    hand = Hand(cards=cards)
    assert actions.get_hand_value(hand) == expected_value

@pytest.mark.parametrize(
    'cards, expected_value',
    [
        ([Card('Clubs', 'Ace'), Card('Hearts', 5)], 6),
        ([Card('Clubs', 'Ace'), Card('Spades', 'King')], 11),
        ([Card('Clubs', 'Ace'), Card('Hearts', 2), Card('Spades', 3)], 6),
        ([Card('Clubs', 2), Card('Hearts', 9), Card('Spades', 'Ace')], 12),
        ([Card('Clubs', 'Ace'), Card('Hearts', 'Ace')], 2),
        ([Card('Clubs', 'Ace'), Card('Hearts', 'Ace'), Card('Spades', 9)], 11),
        ([Card('Clubs', 'Ace'), Card('Hearts', 'Ace'), Card('Spades', 'King')], 12),
        (
            [
                Card('Clubs', 'Ace'), 
                Card('Hearts', 'Ace'), 
                Card('Spades', 'Ace'), 
                Card('Diamonds', 'Ace')
            ], 
            4,
        ),
        ([Card('Clubs', 'Ace'), Card('Hearts', 9)], 10),
        ([Card('Clubs', 'Ace'), Card('Hearts', 4), Card('Spades', 6)], 11),
        ([Card('Clubs', 'Ace'), Card('Hearts', 5), Card('Spades', 6)], 12),
    ],
    ids=[
        'ace_one_pip_card_a',
        'ace_one_face_card',
        'ace_two_pip_cards_a',
        'ace_two_pip_cards_b',
        'two_aces',
        'two_aces_one_pip_card',
        'two_aces_one_face_card',
        'four_aces',
        'ace_one_pip_card_b',
        'ace_two_pip_cards_c',
        'ace_two_pip_cards_d',
    ]
)
def test_soft_hand_values(cards, expected_value):
    hand = Hand(cards=cards)
    assert actions.get_soft_value(hand) == expected_value

def test_copy_deck():
    deck1 = actions.create_and_shuffle()
    deck2 = []
    actions._copy_deck(deck2, deck1)
    
    assert len(deck1) == 52
    assert len(deck2) == 52
    
def test_create_split_hands():
    table = Table(
        player=Player(
            username='Test', 
            hands=[PlayerHand(cards=[Card('Clubs', 6), Card('Hearts', 6)])]
        ),
        deck=actions.create_and_shuffle()
    )
    actions.create_split_hands(table)
    assert len(table.player.hands) == 2
    assert table.player.hands[0].cards[0].to_string() == '♣6'
    assert table.player.hands[1].cards[0].to_string() == '♥6'
    
def test_hit_hand():
    table = Table(
        player=Player(
            username='Test', 
            hands=[PlayerHand(cards=[Card('Clubs', 4), Card('Hearts', 6)])]
        ),
        deck=actions.create_and_shuffle()
    )
    actions.hit_hand(table, table.player.hands[0])
    assert len(table.player.hands[0].cards) == 3

def test_hit_hand_empty_deck():
    table = Table(
        player=Player(
            username='Test', 
            hands=[PlayerHand(cards=[])]
        ),
        deck=actions.create_and_shuffle()
    )
    for i in range(100):
        actions.hit_hand(table, table.player.hands[0])
    assert len(table.player.hands[0].cards) == 100
    
def test_initial_round_deal():
    table = Table(player=Player(username='Test'), deck=actions.create_and_shuffle())
    actions.initial_round_deal(table)
    assert len(table.player.hands) == 1
    assert len(table.player.hands[0].cards) == 2
    assert len(table.dealer.cards) == 2

def test_initial_round_deal_empty_deck():
    table = Table(player=Player(username='Test'), deck=actions.create_and_shuffle())
    for i in range(52):
        table.deck.pop()
    actions.initial_round_deal(table)
    assert len(table.player.hands) == 1
    assert len(table.player.hands[0].cards) == 2
    assert len(table.dealer.cards) == 2

def test_create_and_shuffle():
    deck = actions.create_and_shuffle()
    assert len(deck) == 52
