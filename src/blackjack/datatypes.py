""" 
Creates a container to store the game hands.

@author Adrien P.
@version 4.1.26
"""

from dataclasses import dataclass, field
from .bank import Bank
from .card import Card    

@dataclass
class Hand:
    cards: list[Card] = field(default_factory=list)    
    
@dataclass
class PlayerHand(Hand):
    wager: float = 0.0
    insurance_wager: float = 0.0
    is_active: bool = False

@dataclass
class DealerHand(Hand):
    is_hidden: bool = True
 
@dataclass
class Player:
    bank: Bank = field(default_factory=lambda: Bank(0))
    hands: list[PlayerHand] = field(default_factory=list)

@dataclass
class Table:
    player: Player
    dealer: DealerHand = field(default_factory=DealerHand)
    game_deck: list[Card] = field(default_factory=list)
    