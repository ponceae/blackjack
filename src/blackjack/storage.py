""" 
Contains functions for reading, writing, and updating a JSON file.

@author Adrien P.
@version 3/28/26
"""

from pathlib import Path 
import json 

from .bank_helper import verify_chip_bounds
from .constants import PLAYER_CHIPS

FILE_PATH = Path(__file__).parent / 'save_data.json'

""" 
Creates a new user if it does not exist in the JSON file. When prompting for chips,
this gets added to the JSON immediately.
"""
def create_new_user(data, username):
	if not data or username not in data.keys():
		print('Creating new user.')
		while True:
			chip_count = float(input('How many chips would you like to add?\n'))
			if verify_chip_bounds(chip_count):
				data[username] = {PLAYER_CHIPS: chip_count}
				break
			print('Invalid Input. Must be a number between 15 - 1000.')

""" 
Reads a JSON file and returns the JSON object as a dictionary.
"""
def load_user_data():
	with open(FILE_PATH, 'r') as data_file:
		data = json.load(data_file)
	return data

""" 
Get information from the user in order to pull or modify
the JSON file.
""" 
def pull_user_info():
	username = input('Enter a username to store/pull your chips: \n')
	data = load_user_data()
	if not data or username not in data.keys():
		create_new_user(data, username)
	chip_count = data[username][PLAYER_CHIPS]
	save_chips(username, chip_count, data)
	return chip_count

""" 
Verify username and store the chip count into the JSON. If the
username does not yet exist, create a new JSON entry.
Adds an additional check in case the username became corrupt.
"""
def save_chips(username, chip_count, data):
	if username in data.keys():
		data[username][PLAYER_CHIPS] = chip_count
	else:
		create_new_user(data, username)
	write_user_data(data)  

"""
Initialize a JSON object from the data dictionary and write to the 
JSON file.
"""
def write_user_data(data):
	tmp = json.dumps(data, indent=4)
	with open(FILE_PATH, 'w') as data_file:
		data_file.write(tmp)
