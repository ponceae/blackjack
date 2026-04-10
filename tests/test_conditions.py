""" 
Tests for the conditions module.

Author: Adrien P.
"""

from blackjack.bank import Bank
from blackjack import conditions
from blackjack import constants
from blackjack.datatypes import DealerHand, Hand, Player, PlayerHand, Table
from blackjack.card import Card

def test_can_split():
    hand1 = Hand(cards=[Card('Clubs', 8), Card('Hearts', 8)])
    hand2 = Hand(cards=[Card('Spades', 'Ace'), Card('Diamonds', 'Ace')])
    
    hand3 = Hand(cards=[Card('Hearts', 'King'), Card('Clubs', 'Queen')])
    hand4 = Hand(cards=[Card('Hearts', 9), Card('Clubs', 4)])
    
    assert conditions.can_split(hand1) == True
    assert conditions.can_split(hand2) == True
    assert conditions.can_split(hand3) == False
    assert conditions.can_split(hand4) == False

def test_initial_hands():
    table = Table(
        player=Player(
            username='Test', 
            hands=[PlayerHand(cards=[Card('Clubs', 'Ace'), Card('Hearts', 10)])]
        ),
        dealer=DealerHand(cards=[Card('Spades', 'Ace'), Card('Diamonds', 10)])
    )
    
    assert conditions.compare_initial_hands(table) == constants.PUSH
    
    table.player.hands=[PlayerHand(cards=[Card('Clubs', 'Ace'), Card('Hearts', 10)])]
    table.dealer.cards=[Card('Spades', 2), Card('Diamonds', 10)]
    
    assert conditions.compare_initial_hands(table) == constants.PLAYER_WIN
    
    table.player.hands=[PlayerHand(cards=[Card('Clubs', 2), Card('Hearts', 10)])]
    table.dealer.cards=[Card('Spades', 'Ace'), Card('Diamonds', 10)]
    
    assert conditions.compare_initial_hands(table) == constants.DEALER_WIN
    
    table.player.hands=[PlayerHand(cards=[Card('Clubs', 2), Card('Hearts', 10)])]
    table.dealer.cards=[Card('Spades', 4), Card('Diamonds', 10)]
    
    assert conditions.compare_initial_hands(table) == 0
    
def test_is_bust():
    hand1 = Hand(cards=[Card('Clubs', 8), Card('Hearts', 8), Card('Diamonds', 8)])
    hand2 = Hand(cards=[Card('Spades', 'Ace'), Card('Diamonds', 5)])
    
    assert conditions.is_bust(hand1) == True
    assert conditions.is_bust(hand2) == False
    
def test_is_soft():
    hand1 = Hand(cards=[Card('Clubs', 8), Card('Hearts', 4)])
    hand2 = Hand(cards=[Card('Spades', 'Ace'), Card('Diamonds', 5)])
    
    assert conditions.is_soft(hand1) == False
    assert conditions.is_soft(hand2) == True
    
def test_is_split_aces():
    hand1 = Hand(cards=[Card('Clubs', 'Ace'), Card('Hearts', 'Ace')])
    hand2 = Hand(cards=[Card('Spades', 5), Card('Diamonds', 5)])
    hand3 = Hand(cards=[Card('Clubs', 8), Card('Hearts', 10)])
    
    assert conditions.is_split_aces(hand1) == True
    assert conditions.is_split_aces(hand2) == False
    assert conditions.is_split_aces(hand3) == False
    
def test_is_twenty_one():
    hand1 = Hand(cards=[Card('Clubs', 7), Card('Hearts', 8), Card('Clubs', 6)])
    hand2 = Hand(cards=[Card('Spades', 5), Card('Diamonds', 10)])

    assert conditions.is_twenty_one(hand1) == True
    assert conditions.is_twenty_one(hand2) == False
    
def test_is_valid_wager():
    player = Player(username='Test', bank=Bank(25.0))
    
    assert conditions.is_valid_wager(player, 15.0) == True
    assert conditions.is_valid_wager(player, 35) == False
    assert conditions.is_valid_wager(player, -3.20) == False
    assert conditions.is_valid_wager(player, 0) == False
    assert conditions.is_valid_wager(player, 14.99) == False
    
def test_verify_chip_bounds():
    assert conditions.verify_chip_bounds(15) == True
    assert conditions.verify_chip_bounds(1000.0) == True
    assert conditions.verify_chip_bounds(14.99) == False
    assert conditions.verify_chip_bounds(1000.01) == False
    assert conditions.verify_chip_bounds(500) == True
    assert conditions.verify_chip_bounds(27.5) == True
    assert conditions.verify_chip_bounds(-33.6) == False
    
def test_verify_chip_count():
    assert conditions.verify_chip_count(15) == True
    assert conditions.verify_chip_count(27.5) == True
    assert conditions.verify_chip_count(14.99) == False
    assert conditions.verify_chip_count(0) == False
    assert conditions.verify_chip_count(-4.3) == False
    assert conditions.verify_chip_count(5) == False
    
def test_verify_doubled_wager():
    player = Player(username='Test', bank=Bank(50.0))
    player_hand = PlayerHand(wager=25.0)
    
    assert conditions.verify_doubled_wager(player, player_hand) == True  
    player.bank = Bank(25.0)
    player_hand.wager = 50.0
    assert conditions.verify_doubled_wager(player, player_hand) == False
    player.bank = Bank(0.0)
    assert conditions.verify_doubled_wager(player, player_hand) == False
    
def test_verify_insurance_bet():
    player = Player(username='Test', bank=Bank(25.0))
    player_hand = PlayerHand(wager=15.0)
    
    assert conditions.verify_insurance_bet(player, player_hand) == True   
    player.bank = Bank(5.0) 
    assert conditions.verify_insurance_bet(player, player_hand) == False
    
def test_verify_min_bet():
    player_hand = PlayerHand(wager=15.0)  
    assert conditions.verify_min_bet(player_hand) == True   
    player_hand.wager = 10   
    assert conditions.verify_min_bet(player_hand) == False   
    player_hand.wager = 16 
    assert conditions.verify_min_bet(player_hand) == True
    