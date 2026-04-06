""" 
Create a container to store player and dealer data and game state information.

Author: Adrien P.
"""

from enum import Enum
from typing import NamedTuple

from dataclasses import dataclass, field
from .bank import Bank
from .card import Card    

# ==============================
# MISCELLANEOUS GAME STATE DATA.
# ==============================
class Buffers(NamedTuple):
	dealer: list
	player: list
	main: list

class PlayerAction(Enum):
    NEXT_HAND = 1
    END_TURN = 2

# =======================
# GAME STATE INFORMATION.
# =======================

@dataclass
class Insurance():
    active: bool = False
    win: bool = False
    payout: int | float = 0
    cost: int | float = 0

@dataclass
class Outcome():
     flag: int = 0
     payout: int | float = 0

@dataclass
class SplitHands:
    split_hand: bool = False
    split_aces: bool = False

# ============================================
# DEALER, PLAYER, AND GAME TABLE INFORMATION.
# ============================================

@dataclass
class Hand:
    value: int = 0
    cards: list[Card] = field(default_factory=list)    

@dataclass
class DealerHand(Hand):
    is_hidden: bool = True

@dataclass
class PlayerHand(Hand):
    wager: float = 0.0
    insurance_wager: float = 0.0
    is_active: bool = False
 
@dataclass
class Player:
    bank: Bank = field(default_factory=lambda: Bank(0))
    hands: list[PlayerHand] = field(default_factory=list)

@dataclass
class Table:
    player: Player
    dealer: DealerHand = field(default_factory=DealerHand)
    deck: list[Card] = field(default_factory=list)
    