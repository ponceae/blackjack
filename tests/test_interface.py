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

def test_initial_outcome_display():
    pass

def test_initial_insurance_outcome_display():
    pass