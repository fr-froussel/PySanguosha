from lib.backend import CharactersManager
from lib.ui import CharacterUI
from lib.utils import *
import json
import os

# Create generation directories if doesn't exists
if not os.path.exists(generation_directory):
  os.makedirs(generation_directory)
for clan_label_association in clan_label_associations:
  clan_generation_directory = generation_directory + clan_label_association
  if not os.path.exists(clan_generation_directory):
    os.makedirs(clan_generation_directory)

# Read JSON characters file
print('Open characters configuration file')
with open('characters.json', mode='r', encoding='utf-8') as characters_file:
  print('Parsing characters configuration file')
  characters_data = json.load(characters_file)
  characters_manager = CharactersManager.from_json(characters_data)

  print('Loop through characters parsed successfully')
  print('------')
  for character in characters_manager.characters:
    print('{}'.format(character.name))
    # Create character UI associated to the character
    print(' > Creation')
    character_ui = CharacterUI(character)
    if character_ui.additionals_ui_ready:
      print(' > Generation')
      character_ui.generate_ui()
    else:
      print('{}: Error creation'.format(character_ui.character.name))

  characters_file.close()