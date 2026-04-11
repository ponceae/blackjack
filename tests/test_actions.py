""" 
Tests for the actions module.

Author: Adrien P.
"""

from blackjack.card import Card
from blackjack import actions
from blackjack.datatypes import Hand, Player, PlayerHand, Table

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

def test_hand_value_base():
    hand1 = Hand(cards=[Card('Clubs', 2), Card('Hearts', 3), Card('Spades', 4)])
    assert actions.get_hand_value(hand1) == 9
    hand1 = Hand(cards=[Card('Clubs', 10), Card('Hearts', 'Jack')])
    assert actions.get_hand_value(hand1) == 20
    hand1 = Hand(cards=[Card('Clubs', 7), Card('Hearts', 8), Card('Spades', 9)])
    assert actions.get_hand_value(hand1) == 24

def test_hard_and_soft_hand_values():
    hand1 = Hand(cards=[Card('Clubs', 'Ace'), Card('Hearts', 5)])
    assert actions.get_hand_value(hand1) == 16
    assert actions.get_soft_value(hand1) == 6
    hand1.cards = [Card('Clubs', 'Ace'), Card('Spades', 'King')]
    assert actions.get_hand_value(hand1) == 21
    assert actions.get_soft_value(hand1) == 11
    hand1.cards = [Card('Clubs', 'Ace'), Card('Hearts', 2), Card('Spades', 3)]
    assert actions.get_hand_value(hand1) == 16
    assert actions.get_soft_value(hand1) == 6
    hand1.cards = [Card('Clubs', 2), Card('Hearts', 9), Card('Spades', 'Ace')]
    assert actions.get_hand_value(hand1) == 12
    assert actions.get_soft_value(hand1) == 12
    hand1.cards = [Card('Clubs', 'Ace'), Card('Hearts', 'Ace')]
    assert actions.get_hand_value(hand1) == 12
    assert actions.get_soft_value(hand1) == 2
    hand1.cards = [Card('Clubs', 'Ace'), Card('Hearts', 'Ace'), Card('Spades', 9)]
    assert actions.get_hand_value(hand1) == 21
    assert actions.get_soft_value(hand1) == 11
    hand1.cards = [Card('Clubs', 'Ace'), Card('Hearts', 'Ace'), Card('Spades', 'King')]
    assert actions.get_hand_value(hand1) == 12
    assert actions.get_soft_value(hand1) == 12
    hand1.cards = [
        Card('Clubs', 'Ace'), 
        Card('Hearts', 'Ace'), 
        Card('Spades', 'Ace'), 
        Card('Diamonds', 'Ace')
    ]
    assert actions.get_hand_value(hand1) == 14
    assert actions.get_soft_value(hand1) == 4
    hand1.cards = [Card('Clubs', 'Ace'), Card('Hearts', 9)]
    assert actions.get_hand_value(hand1) == 20
    assert actions.get_soft_value(hand1) == 10
    hand1.cards = [Card('Clubs', 'Ace'), Card('Hearts', 4), Card('Spades', 6)]
    assert actions.get_hand_value(hand1) == 21
    assert actions.get_soft_value(hand1) == 11
    hand1.cards = [Card('Clubs', 'Ace'), Card('Hearts', 5), Card('Spades', 6)]
    assert actions.get_hand_value(hand1) == 12
    assert actions.get_soft_value(hand1) == 12

def test_create_and_shuffle():
    deck = actions.create_and_shuffle()
    assert len(deck) == 52
