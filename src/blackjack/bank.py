"""
Store and manage a player's virtual chips.

Author: Adrien P.
"""

class Bank:
    """Represents a player's bank (or wallet)"""

    def __init__(self, chips: float):
        """
        Initialize a player Bank with the given chips.

        Args:
            chips (float): The amount of chips in the player's bank.
        """
        try:
            chips = float(chips)
        except ValueError:
            raise ValueError('Invalid Chip Count. Must be a number')
        if not (15 <= chips <= 1000):
            raise ValueError('Invalid Chip Count. Must be a number between 15 - 1000')
        self.chips = chips
        
    def get_chip_count(self):
        """
        Return the bank chip count.

        Returns:
            float | int: The bank's chip count.
        """
        return self.chips
    
    def set_chip_count(self, value: float | int):
        """
        Set the `chips` to the given value.

        Args:
            value (float | int): The value to set `chips` to.

        Returns:
            None
        """
        self.chips = value

    def add_chips(self, value: float | int):
        """
        Add the value to `chips`.

        Args:
            value (float | int): The value to add to `chips`.

        Returns:
            None
        """
        self.chips += value

    def remove_chips(self, value: float | int):
        """
        Remove the value from `chips`.

        Args:
            value (float | int): The value to remove from `chips`.

        Returns:
            None
        """
        self.chips -= value
    
    def to_string(self):
        """
        Return the string representation of the bank.

        Returns:
            The string representation (e.g., Chips $15.00).
        """
        return f'Chips ${self.chips:.2f}'
    