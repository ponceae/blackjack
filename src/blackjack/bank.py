"""
This file contains the functionality for storing and updating
a player's virtual chips.

@author Adrien P.
@version 3.26.26
"""

class Bank:
    
    def __init__(self, chip_count):
        try:
            chip_count = float(chip_count)
        except ValueError:
            raise ValueError('Invalid Chip Count. Must be a number')
        if not (15 <= chip_count <= 1000):
            raise ValueError('Invalid Chip Count. Must be a number between 15 - 1000')
        self.chip_count = chip_count
        
    def get_chip_count(self):
        return self.chip_count
    
    def set_chip_count(self, value):
        self.chip = value

    def add_chips(self, value):
        self.chip_count += value

    def remove_chips(self, value):
        self.chip_count -= value
    
    def to_string(self):
        return f'Chips ${self.chip_count:.2f}'
    