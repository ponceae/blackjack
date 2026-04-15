""" 
Tests for the storage module.

Author: Adrien P.
"""

import json
import pytest

from blackjack.constants import FILE_PATH, PLAYER_CHIPS
from blackjack import storage

@pytest.fixture
def mock_inputs(monkeypatch):
    def _mock_inputs(values):
        inputs = iter(values)
        def mock_input(prompt):
            try:
                return next(inputs)
            except StopIteration:
                pytest.fail(f'Test ran out of mock inputs.\nLast Prompt: {prompt}\n')
        monkeypatch.setattr('builtins.input', mock_input)
    return _mock_inputs

@pytest.mark.parametrize(
    'data, username, inputs, expected_value',
    [
        ({}, 'Test', ['50'], 50.0),
        ({}, 'Test', ['25'], 25.0),
        ({'Test': {PLAYER_CHIPS: 15.0}}, 'Test', [], 15.0),
        ({}, 'Test', ['10', '20.0'], 20.0),
        ({}, 'Test', ['abc', '30'], 30.0),
    ],
    ids=[
        'data_setting_a_success',
        'data_setting_b_success',
        'data_already_exists_failure',
        'data_setting_out_of_bounds_caught',
        'data_setting_invalid_input_caught'
    ]
)
def test_create_new_user(mock_inputs, data, username, inputs, expected_value):
    mock_inputs(inputs)
    storage.create_new_user(data, username)
    assert data[username] == {PLAYER_CHIPS: expected_value}

def _generate_test_data_params():
    return [
        ({'Test': {PLAYER_CHIPS: 500.0}}, 500.0),
        ({'Test': {PLAYER_CHIPS: 250.0}}, 250.0),
        ({'Test': {PLAYER_CHIPS: 120.5}}, 120.5),
    ]

@pytest.mark.parametrize(
    'test_data, expected_chips',
    [
        *_generate_test_data_params()
    ]
) 
def test_load_data_from_json_success(monkeypatch, tmp_path, test_data, expected_chips):
    test_file = tmp_path / 'test_file.json'
    with open(test_file, 'w') as data_file:
        json.dump(test_data, data_file)
    monkeypatch.setattr('blackjack.storage.FILE_PATH', str(test_file))
    loaded_data = storage.load_user_data()
    assert loaded_data == test_data
    assert loaded_data['Test'][PLAYER_CHIPS] == expected_chips

@pytest.mark.parametrize(
    'test_data, expected_chips',
    [
        *_generate_test_data_params()
    ]
)
def test_write_user_data_success(monkeypatch, tmp_path, test_data, expected_chips):
    test_file = tmp_path / 'test_file.json'
    monkeypatch.setattr('blackjack.storage.FILE_PATH', str(test_file))
    storage.write_user_data(test_data)
    assert test_file.exists()
    with open(test_file, 'r') as data_file:
        loaded_data = json.load(data_file)
    assert loaded_data == test_data
    assert loaded_data['Test'][PLAYER_CHIPS] == expected_chips
    