"""
Define the Bank class for the storage and management of a player's chips.

Author: Adrien P.
"""

class Bank:
    """Represent a player's bank (or wallet)."""

    def __init__(self, chips: float):
        """
        Initialize a Bank with the given chips.

        Args:
            chips (float): The amount of chips in the player's bank.
        """
        chips = self._to_float(chips)

        if not (0 <= chips <= 1000):
            raise ValueError('Invalid Chip Count, must be a number between 0 - 1000')
        
        self._chips = chips
    
    @staticmethod
    def _to_float(value) -> float:
        """ 
        Helper, validate value type and float conversion.
        
        Args:
            value (float): The value to validate and convert.
            
        Returns:
            float: The converted value.
        """
        try:
            return float(value)
        except (ValueError, TypeError):
            raise ValueError('Invalid Chip Count, must be a number.')
    
    @property
    def chips(self) -> float:
        """
        The current chip balance of the bank.
        
        Returns:
            The current chip balance.
        """
        return self._chips
    
    @chips.setter
    def chips(self, value: float) -> None:
        value = self._to_float(value)

        if value < 0:
            raise ValueError('Invalid Value, `value` is less than 0.')
        
        self._chips = value
    
    def to_string(self):
        """
        Return the string representation of the bank.

        Returns:
            The string representation (e.g., Chips: $15.00).
        """
        return f'Chips: ${self.chips:.2f}'
    