"""
Constants for configuring game information. Does not contain any functions.

Author: Adrien P.
"""

from pathlib import Path

# ==================
# CARD VARIABLES
# ==================

ACE_ALT_VALUE = 1
ACE = 'Ace'
DEFAULT_ACE_VALUE = 11
FACE_CARD_VALUE = 10

CARD_RANKS = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King', 'Ace']
CARD_SUITS = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
NAMED_CARD_RANKS = ['Ace', 'Jack', 'Queen', 'King']
CARD_SUIT_SYMBOLS = {
    'Clubs': '♣', 
    'Diamonds': '♦', 
    'Hearts': '♥', 
    'Spades': '♠',
}

# ==================
# I/O FLAGS
# ==================

HIT = 'H'
STAND = 'S'
NO = 'N'
YES = 'Y'
BUST = 'B'
DOUBLE = 'D'
WIN = 'W'

# ==================
# OUTCOME FLAGS
# ==================

PLAYER_WIN = 1
DEALER_WIN = 2
PUSH = 3

# ==================
# TIMER FLAGS
# ==================

INITIAL = 1
PLAYER = 2
SWITCH_TURN = 3
DEALER = 4
CHECK = 5
SHOW = 6
BROKE = 7
TIMER_MESSAGES = {
    1: 'Dealer is peeking... {}',  
    2: 'Switching active hand... {}',  
    3: 'Switching to dealer... {}',  
    4: 'Dealer is hitting... {}',  
    5: 'Comparing hand values... {}',  
    6: 'Dealer is flipping card... {}', 
    7: 'You cannot afford that... {}',
}

# ==================
# JSON FILE INFO
# ==================

PLAYER_CHIPS = 'player_chips'
FILE_PATH = Path(__file__).parent / 'save_data.json'

# Miscellaneous constants
MIN_WAGER = 15
ROMAN_NUMERALS = {1: 'I', 2: 'II'}
