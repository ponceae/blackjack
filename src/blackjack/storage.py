""" 
JSON data file initialization and modification.

This module provides functionality for reading, writing, and updating data from a 
local JSON file.
"""

__author__ = 'Adrien P.'

import json 

from .conditions import is_valid_chip_bounds
from .constants import FILE_PATH, MAX_BANK, MIN_WAGER, PLAYER_CHIPS

def create_new_user(data: dict, username: str) -> None:
    """
    Prompt the user for an initial chip count and create a new profile.
    
    If the `username` is not found in the `data` dictionary, this function will
    continuously prompt the console until a valid balance is entered, then update
    the dictionary.

    Args:
        data (dict): The dictionary containing all saved player profiles.
        username (str): The username of the profile to create.
    """
    if not data or username not in data:
        print('Creating new user.')

        while True:
            raw_chip_count = input('Enter the amount of chips to add.\n')

            try:
                chip_count = float(raw_chip_count)
                
                if is_valid_chip_bounds(chip_count):
                    data[username] = {PLAYER_CHIPS: chip_count}
                    break
                else:
                    print(
                        f'Invalid input, please enter a number between '
                        f'{MIN_WAGER:.2f} and {MAX_BANK:,.2f}'
                    )

            except ValueError:
                print('Invalid value, please enter a number.')

def load_user_data() -> dict:
    """
    Load the game data from the local JSON file.

    Returns:
        dict: The dictionary containing all saved player profiles.
    """
    with open(FILE_PATH, 'r') as f:
        data = json.load(f)

    return data

def pull_user_info() -> tuple[float, str]:
    """
    Prompt for a username and retrieve or initialize the user's profile.
    
    Checks the data file for an existing profile. If the profile is not found, a 
    new one is created. 

    Returns:
        tuple[float, str]: A tuple containing:
            - float: The player's current chip balance
            - str: The player's associated username.
    """
    username = input(
        'Enter your username to load your profile (or create a new one):\n> '
    )
    data = load_user_data()

    if not data or username not in data:
        create_new_user(data, username)

    chip_count = data[username][PLAYER_CHIPS]
    save_chips(username, chip_count, data)

    return chip_count, username

def save_chips(username: str, chips: float, data: dict) -> None:
    """
    Update the user's chip balance in the data dictionary.

    If the `username` exists in the `data` dictionary, their profile is updated
    with the new chip balance. If the profile does not exist, a new entry is
    created for them automatically.

    Args:
        username (str): The player's username.
        chips (float): The player's current chip balance.
        data (dict): The dictionary containing all saved player profiles.
    """
    if username in data:
        data[username][PLAYER_CHIPS] = chips
    else:
        create_new_user(data, username)

    write_user_data(data)  

def write_user_data(data: dict) -> None:
    """
    Save the given data dictionary to the local JSON file.

    Args:
        data (dict): The dictionary containing all saved player profiles.
    """
    tmp = json.dumps(data, indent=4)

    with open(FILE_PATH, 'w') as f:
        f.write(tmp)
