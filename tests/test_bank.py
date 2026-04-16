""" 
Tests for the bank class module.

Author: Adrien P.
"""

import pytest

from blackjack.bank import Bank

@pytest.mark.parametrize(
    'chips, expected_amount',
    [
        (15, 15.0),
        (1000, 1000.0),
        (34.5, 34.5),
        (14.99, 14.99),
        (0, 0.0),
        ('15', 15.0),
        ('7.5', 7.5),
    ]
)
def test_initial_bank_state(chips, expected_amount):
    test_bank = Bank(chips)
    assert test_bank.chips == expected_amount

@pytest.mark.parametrize(
    'invalid_input, expected_err_msg',
    [
        (1000.01, 'Invalid Chip Count, must be a number between 0 - 1000'),
        (-3, 'Invalid Chip Count, must be a number between 0 - 1000'),
        (-2.56, 'Invalid Chip Count, must be a number between 0 - 1000'),
        ('4a', 'Invalid Chip Count, must be a number.'),
        ('4.56num', 'Invalid Chip Count, must be a number.'),
    ],
    ids=[
        'one_over_hundredth_place',
        'negative_int',
        'negative_float',
        'string_invalid_a',
        'string_invalid_b',
    ]
)
def test_init_raises_valueerror_on_invalid_input(invalid_input, expected_err_msg):
    with pytest.raises(ValueError, match=expected_err_msg):
        Bank(invalid_input)

@pytest.fixture
def start_bank():
    return Bank(225.50)

@pytest.mark.parametrize(
    'add_amount, expected_balance',
    [
        (25, 250.5),
        (7.5, 233.0),
        (32.5, 258.0),
    ]
)
def test_adding_chips_to_bank(start_bank, add_amount, expected_balance):
    start_bank.chips += add_amount
    assert start_bank.chips == expected_balance

@pytest.mark.parametrize(
    'remove_amount, expected_balance',
    [
        (22.5, 203.0),
        (7.5, 218.0),
        (225.5, 0.0),
    ]
)
def test_removing_chips_from_bank(start_bank, remove_amount, expected_balance):
    start_bank.chips -= remove_amount
    assert start_bank.chips == expected_balance

@pytest.mark.parametrize(
    'set_amount, expected_balance',
    [
        (0, 0.0),
        (525.75, 525.75),
        (105.5, 105.5),
    ]
)
def test_setting_chips_to_bank(start_bank, set_amount, expected_balance):
    start_bank.chips = set_amount
    assert start_bank.chips == expected_balance

@pytest.mark.parametrize(
    'invalid_value, expected_err_msg',
    [
        (-5.5, 'Invalid Value, `value` is less than 0.'),
        (-0.01, 'Invalid Value, `value` is less than 0.'),
        ('number string', 'Invalid Chip Count, must be a number.'),
        (None, 'Invalid Chip Count, must be a number.'),
        ([], 'Invalid Chip Count, must be a number.'),
    ]
)
def test_bank_chips_setter_raises_valueerror_on_invalid_value(
        start_bank, 
        invalid_value, 
        expected_err_msg
):
    with pytest.raises(ValueError, match=expected_err_msg):
        start_bank.chips = invalid_value

@pytest.mark.parametrize(
    'chips, expected_display',
    [
        (15.0, 'Chips: $15.00'),
        (1000.0, 'Chips: $1000.00'),
        (34.5, 'Chips: $34.50'),
        (14.99, 'Chips: $14.99'),
        (0.0, 'Chips: $0.00'),
    ]
)
def test_bank_chips_to_string(chips, expected_display):
    test_bank = Bank(chips)
    assert test_bank.to_string() == expected_display
