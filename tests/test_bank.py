""" 
Tests for the bank class module.

Author: Adrien P.
"""

import pytest

from blackjack.bank import Bank

B1 = Bank(15)
B2 = Bank(1000)
B3 = Bank(34.5)
B4 = Bank(14.99)
B5 = Bank(0)
B6 = Bank('15') # type: ignore
B7 = Bank('7.5') # type: ignore

def test_init_and_get_chips():
    assert B1.chips == 15.0
    assert B1.get_chip_count() == 15.0
    assert B2.chips == 1000.0
    assert B2.get_chip_count() == 1000.0
    assert B3.chips == 34.5 
    assert B3.get_chip_count() == 34.5
    assert B4.chips == 14.99
    assert B4.get_chip_count() == 14.99
    assert B5.chips == 0.0
    assert B5.get_chip_count() == 0.0
    assert B6.chips == 15.0
    assert B6.get_chip_count() == 15.0
    assert B7.chips == 7.5
    assert B7.get_chip_count() == 7.5
    
def test_init_valueerror():
    with pytest.raises(ValueError):
        Bank(1000.01)
    with pytest.raises(ValueError):
        Bank(-3)
    with pytest.raises(ValueError):
        Bank(-2.56)
    with pytest.raises(ValueError):
        Bank('4a') # type: ignore
    with pytest.raises(ValueError):
        Bank('4.56num') # type: ignore
        
def test_add_set_and_remove_chips():
    bank = Bank(0)
    bank.set_chip_count(15)
    assert bank.get_chip_count() == 15.0
    bank.add_chips(30)
    assert bank.get_chip_count() == 45.0
    bank.remove_chips(45.0)
    assert bank.get_chip_count() == 0.0
    bank.add_chips(34.5)
    assert bank.get_chip_count() == 34.5
    
def test_to_string():
    assert B1.to_string() == 'Chips: $15.00'
    assert B2.to_string() == 'Chips: $1000.00'
    assert B3.to_string() == 'Chips: $34.50'
    assert B4.to_string() == 'Chips: $14.99'
    assert B5.to_string() == 'Chips: $0.00'
    assert B6.to_string() == 'Chips: $15.00'
    assert B7.to_string() == 'Chips: $7.50'
