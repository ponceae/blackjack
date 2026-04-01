""" 
Creates a container to store the game hands.

@author Adrien P.
@version 4.1.26
"""

from dataclasses import dataclass
from .bank import Bank
from .card import Card    

@dataclass
class Hand:
    cards: list[Card]
    wager: float
    insurance_wager: float
    is_active: bool
    
@dataclass
class Player:
    player_bank: Bank
    player_hands: list

@dataclass
class Table:
    player: Player
    dealer_hand: Hand
    game_deck: list
    