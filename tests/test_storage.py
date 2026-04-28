""" 
Tests for the `storage.py` module.

Contains tests for validating data management, inlcuding:
- Loading game state from the local JSON file.
- Creating and initializing new user profiles.
- Updating existing user chip balances in memory.
- Saving modified data back to memory.
"""

__author__ = 'Adrien P.'

import json
import pytest

from blackjack.constants import PLAYER_CHIPS
from blackjack import storage

@pytest.mark.parametrize(
    'data, username, inputs, expected_chips',
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
def test_create_new_user_success(mock_inputs, data, username, inputs, expected_chips):
    mock_inputs(inputs)
    storage.create_new_user(data, username)

    assert data[username] == {PLAYER_CHIPS: expected_chips}

def _generate_test_data_params():
    return [
        ({'Test': {PLAYER_CHIPS: 500.0}}, 500.0),
        ({'Test': {PLAYER_CHIPS: 250.0}}, 250.0),
        ({'Test': {PLAYER_CHIPS: 120.5}}, 120.5),
    ]

@pytest.mark.parametrize(
    'data, expected_chips',
    [
        *_generate_test_data_params()
    ]
)
def test_load_data_from_json_success(monkeypatch, tmp_path, data, expected_chips):
    """Test that valid user data is successfully loaded from the JSON file."""
    tmp_file = tmp_path / 'test_file.json'
    with open(tmp_file, 'w') as f:
        json.dump(data, f)

    monkeypatch.setattr('blackjack.storage.FILE_PATH', str(tmp_file))

    loaded_data = storage.load_user_data()

    assert loaded_data == data
    assert loaded_data['Test'][PLAYER_CHIPS] == expected_chips

@pytest.mark.parametrize(
    'data, expected_chips',
    [
        *_generate_test_data_params()
    ]
)
def test_write_user_data_success(monkeypatch, tmp_path, data, expected_chips):
    """Test that user data is successfully saved to the JSON file."""
    tmp_file = tmp_path / 'test_file.json'

    monkeypatch.setattr('blackjack.storage.FILE_PATH', str(tmp_file))

    storage.write_user_data(data)

    assert tmp_file.exists()

    with open(tmp_file, 'r') as f:
        loaded_data = json.load(f)

    assert loaded_data == data
    assert loaded_data['Test'][PLAYER_CHIPS] == expected_chips

def test_save_chips_with_existing_user(monkeypatch):
    """
    Test that user data is successfully updated to the JSON when the user's profile
    already exists.
    """
    username = 'Test'
    data = {'Test': {PLAYER_CHIPS: 15.0}}
    chips = 37.5

    monkeypatch.setattr(storage, 'write_user_data', lambda *args, **kwargs: None)
    monkeypatch.setattr(storage, 'create_new_user', lambda *args, **kwargs: None)

    storage.save_chips(username, chips, data)

    assert data[username][PLAYER_CHIPS] == chips

def test_save_chips_with_new_user(monkeypatch):
    """
    Test that a new user is created and their data is successfully updated to 
    the JSON.
    """
    username = 'New Test'
    test_data = {'Test': {PLAYER_CHIPS: 15.0}}
    chips = 37.5

    monkeypatch.setattr(storage, 'write_user_data', lambda *args, **kwargs: None)

    create_user_calls = []
    def spy_create_new_user(data, username):
        create_user_calls.append((data, username))

    monkeypatch.setattr(storage, 'create_new_user', spy_create_new_user)

    storage.save_chips(username, chips, test_data)

    assert len(create_user_calls) == 1
    assert create_user_calls[0] == (test_data, 'New Test')

def test_pull_user_info_existing_user_success(monkeypatch, mock_inputs):
    """ 
    Test loading an existing user's game data from a local JSON file.
    """
    test_data = {'Test': {PLAYER_CHIPS: 15.0}}

    monkeypatch.setattr(storage, 'load_user_data', lambda: test_data)
    monkeypatch.setattr(storage, 'create_new_user', lambda *args, **kwargs: None)

    save_calls = []
    def spy_save_chips(username, chips, data):
        save_calls.append((username, chips, data))

    monkeypatch.setattr(storage, 'save_chips', spy_save_chips)

    mock_inputs(['Test'])

    chips, username = storage.pull_user_info()

    assert len(save_calls) == 1
    assert save_calls[0] == ('Test', 15.0, test_data)

    assert chips == 15.0
    assert username == 'Test'

def test_pull_user_info_new_user_creation(monkeypatch, mock_inputs):
    """ 
    Test creating a new user when attempting to load a non-existing user's game
    data from a local JSON file.
    """
    test_data = {'Test': {PLAYER_CHIPS: 15.0}}

    monkeypatch.setattr(storage, 'load_user_data', lambda: test_data)

    create_user_calls = []
    def spy_create_new_user(data_a, username):
        create_user_calls.append((data_a, username))
        data_a[username] = {PLAYER_CHIPS: 20.0}

    monkeypatch.setattr(storage, 'create_new_user', spy_create_new_user)

    mock_inputs(['New Test'])

    save_calls = []
    def spy_save_chips(username, chips, data_b):
        save_calls.append((username, chips, data_b))  

    monkeypatch.setattr(storage, 'save_chips', spy_save_chips) 

    chips, username = storage.pull_user_info()

    assert len(create_user_calls) == 1
    assert create_user_calls[0] == (test_data, 'New Test')

    assert len(save_calls) == 1
    assert save_calls[0] == ('New Test', 20.0, test_data)

    assert chips == 20.0
    assert username == 'New Test'
