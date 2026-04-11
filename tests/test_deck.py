"""
Tests for the deck module.

Author: Adrien P
"""

from blackjack.deck import create_deck, shuffle_deck

TEST_DECK = create_deck()
SHUFFLED = shuffle_deck(TEST_DECK)

def test_create_deck():   
    test_deck = create_deck()

    for i in range(len(test_deck)):
        assert test_deck[i].to_string() == test_deck[i].to_string()

def test_shuffle_deck():
    assert len(SHUFFLED) == 52

    standard_set = set((card.suit, card.rank) for card in TEST_DECK)
    shuffled_set = set((card.suit, card.rank)for card in SHUFFLED)

    assert standard_set == shuffled_set
    assert len(SHUFFLED) == len(shuffled_set)
    