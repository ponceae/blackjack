"""
Tests for the deck module.

Author: Adrien P
"""

from blackjack.deck import create_deck, shuffle_deck

def test_create_deck_success():   
    test_deck = create_deck()

    for i in range(len(test_deck)):
        assert test_deck[i].to_string() == test_deck[i].to_string()

def test_shuffle_deck_is_valid():
    test_deck = create_deck()
    shuffled = shuffle_deck(test_deck)
    assert len(shuffled) == 52

    standard_set = set((card.suit, card.rank) for card in test_deck)
    shuffled_set = set((card.suit, card.rank) for card in shuffled)

    assert standard_set == shuffled_set
    assert len(shuffled) == len(shuffled_set)
    