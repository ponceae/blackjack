""" 
Global constants for the testing modules, such as error message displays.
"""

__author__ = 'Adrien P.'

from blackjack.constants import MAX_BANK

BANK_BOUNDS_ERR_MSG = (
    f'Invalid value, `chips` must be a number between 0 and {MAX_BANK:,.2f}'
)
BANK_INVALID_VALUE_ERR_MSG = 'Invalid value, `value` must be a number.'
BANK_NEGATIVE_VALUE_ERR_MSG = 'Invalid value, `value` is less than 0.'