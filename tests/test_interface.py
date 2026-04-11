""" 
Tests for the interface module.

Author: Adrien P.
"""

from blackjack.bank import Bank
from blackjack.card import Card
from blackjack import constants
from blackjack.datatypes import DealerHand, Player, PlayerHand, Table
from blackjack import interface

def test_compare_hands_output():
    table = Table(
        player=Player(
            username='Test',
            hands=[PlayerHand(
                        cards=[Card('Spades', 5), Card('Clubs', 5)],
                        wager=15.0
                    ),
                    PlayerHand(
                        cards=[
                                Card('Diamonds', 4), 
                                Card('Spades', 6), 
                                Card('Hearts', 'Ace')
                            ],
                        wager=30.0
                    )
                ]
        ),
        dealer=DealerHand(cards=[
                Card('Diamonds', 4), 
                Card('Hearts', 6), 
                Card('Spades', 7)
            ]
        )
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
            hands=[PlayerHand(
                cards=[Card('Spades', 4), Card('Hearts', 6)],
                wager=15.0
            )]
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
    table.player.bank.set_chip_count(22.5)
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
        