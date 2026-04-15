""" 
This function tests the game module including main game loop.
"""

import pytest

from blackjack.bank import Bank
from blackjack.card import Card
from blackjack.datatypes import Player, PlayerHand, Table
from blackjack import game

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
        )
    )
def test_handle_insurance_on_init_deal():
    pass