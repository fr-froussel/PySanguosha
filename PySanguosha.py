from lib.backend import CharactersManager
from lib.ui import CharacterUI
from lib.utils import *
import json
import os

# Create generation directory if doesn't exists
if not os.path.exists(generation_directory):
  os.makedirs(generation_directory)

# Read JSON characters file
with open('characters.json', mode='r', encoding='utf-8') as characters_file:
  characters_data = json.load(characters_file)
  characters_manager = CharactersManager.from_json(characters_data)
  test = CharactersManager()

  for character in characters_manager.characters:
    # Create character UI associated to the character
    character_ui = CharacterUI(character)

    if character_ui.additionals_ui_ready:
      print('{}: Generation'.format(character_ui.character.name))
      character_ui.generate_ui()
    else:
      print('{}: Error'.format(character_ui.character.name))
