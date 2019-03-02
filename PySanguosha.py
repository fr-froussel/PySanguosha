from lib.backend import *
from lib.ui import CharacterUI
import json
import os

# Create generation directory if doesn't exists
generation_dir = 'generation'
if not os.path.exists(generation_dir):
    os.makedirs(generation_dir)

# Read JSON characters file
with open('characters.json', mode='r', encoding='utf-8') as characters_file:
  characters_data = json.load(characters_file)
  characters_manager = CharactersManager.from_json(characters_data)
  test = CharactersManager()

  for character in characters_manager.characters:
    # Create character UI associated to the character
    character_ui = CharacterUI(character)

    if character_ui.additionals_ui_ready:
      character_ui.generate_ui()
