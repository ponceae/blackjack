""" 
Creates a container to store the game hands.

@author Adrien P.
@version 4.1.26
"""

from dataclasses import dataclass

@dataclass
class GameHands:
    player_hands: list
    dealer_hand: list
    