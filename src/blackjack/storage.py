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
        data (dict): The dictionary containing the saved player profiles.
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
                        f'Invalid Input, Please enter a number between '
                        f'{MIN_WAGER:.2f} - ' 
                        f'{MAX_BANK:,.2f}'
                    )

            except ValueError:
                print('Invalid Value, Please enter a number.')

def load_user_data() -> dict:
    """
    Read the JSON file and return the JSON object as a dictionary.

    Returns:
        dict: The JSON data.
    """
    with open(FILE_PATH, 'r') as f:
        data = json.load(f)

    return data

def pull_user_info() -> tuple[float, str]:
    """
    Prompt the user for a username and pull or modify data from the JSON file and 
    return the chip count from the JSON.

    Returns:
        tuple[float, str]: The chip count from the JSON and the associated username.
    """
    username = input('Enter a username to store/pull your chips: \n')
    data = load_user_data()
 
    if not data or username not in data:
        create_new_user(data, username)
  
    chip_count = data[username][PLAYER_CHIPS]
    save_chips(username, chip_count, data)

    return chip_count, username

def save_chips(username: str, chips: float | int, data: dict) -> None:
    """
    Verify that the username exists and store the data in the JSON. Create a new
    user if the username does not exist by creating a new JSON entry.

    Args:
        username (str): The username of the user to check.
        chips (float | int): The chip count to store in the JSON.
        data (dict): The JSON data represented as a dictionary.

    Returns:
        None
    """
    if username in data:
        data[username][PLAYER_CHIPS] = chips
    else:
        create_new_user(data, username)

    write_user_data(data)  

def write_user_data(data: dict) -> None:
    """
    Initialize a JSON object from the data dictionary and write to the JSON.

    Args:
        data (dict): The JSON data represented as a dictionary.
    """
    tmp = json.dumps(data, indent=4)

    with open(FILE_PATH, 'w') as f:
        f.write(tmp)
