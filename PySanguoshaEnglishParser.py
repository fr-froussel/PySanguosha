from bs4 import BeautifulSoup
import certifi
import codecs
import json
import mtranslate
import os
import pinyin
import urllib3

# Json data
json_CharactersManager__characters = '_CharactersManager__characters'
json_Character__background = '_Character__background'
json_Character__clan = '_Character__clan'
json_Character__life_points = '_Character__life_points'
json_Character__lord = '_Character__lord'
json_Character__name = '_Character__name'
json_Character__spells = '_Character__spells'
json_Character__url = '_Character__url'
json_Spell__description = '_Spell__description'
json_Spell__name = '_Spell__name'
characters_json_data = {json_CharactersManager__characters: []}

# Listing characters where we found error(s)
characters_with_errors = []

# Parse main sanguoshaenglish.com characters page
print('Parsing sanguoshaenglish.com')
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
base_url = 'https://www.sanguoshaenglish.com'
url = base_url + '/characters/all'
response = http.request('GET', url)
soup = BeautifulSoup(response.data, 'html.parser')
for a in soup.find_all('a', {'class': 'thumbnail thumbnail-no-border'}, href=True):
    character_url = base_url + a['href']
    character_response = http.request('GET', character_url)
    character_soup = BeautifulSoup(character_response.data, 'html.parser')

    # Name
    name = character_soup.find(
        'h1', {'class': 'character-name'}).getText().replace(' [DEMIGOD]', '')
    name = name.replace('ǔ', 'u').replace('ǐ', 'i').replace(
        'ǎ', 'a').replace('ě', 'e').replace('ǒ', 'o')

    print('{}: Parsing'.format(name.encode('ascii', 'ignore')))

    # Characteristics
    clan = ""
    life_points = 0
    lord = False

    table = character_soup.find('table', {'class': 'table character-info'})
    rows = table.findAll('tr')
    data = [[td.findChildren(text=True)
             for td in tr.findAll("td")] for tr in rows]
    data = [[u"".join(d).strip() for d in l] for l in data]
    for table_data in data:
        if len(table_data) != 2:
            continue

        if table_data[0] == 'Kingdom':
            clan = table_data[1]
        if table_data[0] == 'Health':
            life_points = int(table_data[1])
        if table_data[0] == 'Ruler':
            if table_data[1] == 'Yes':
                lord = True

    # Skins
    skins_map = []
    skins = character_soup.findAll('img', {'class': 'center-block'}, src=True)
    for skin in skins:
        background = '.' + skin['src']
        if os.path.isfile(background):
            skins_map.append(background)
    if len(skins_map) == 0:
        characters_with_errors.append(
            'No background found for {} ({})'.format(name, character_url))

    # Spells
    spells_data = {}
    spells = character_soup.findAll('li', {'class': 'list-group-item'})
    for spell in spells:
        spell_name_span = spell.find('span')
        if spell_name_span is None:
            characters_with_errors.append(
                ' > Check spell(s) data for {} ({}), may be inconsistent'.format(name, character_url))
            continue
        spell_name_extracted = spell_name_span.getText()
        if spell_name_extracted is None:
            characters_with_errors.append(
                ' > Check spell(s) data for {} ({}), may be inconsistent'.format(name, character_url))
            continue

        try:
            spell_name_extracted_splitted = spell_name_extracted.split(' ')
            maximum_words_authorized_for_spell_desc = 2
            if len(spell_name_extracted_splitted) > maximum_words_authorized_for_spell_desc:
                spell_name_extracted = ' '.join(
                    spell_name_extracted_splitted[0:maximum_words_authorized_for_spell_desc])
            translation = mtranslate.translate(spell_name_extracted, 'zh')
            if len(translation) > maximum_words_authorized_for_spell_desc:
                translation = translation[0:maximum_words_authorized_for_spell_desc]
            # Split translation to better pinyin translation
            pinyin_translation = pinyin.get(translation)
            spell_name = pinyin_translation.capitalize()

            spell_desc = ''
            # Parse spell description
            for spell_desc_item in spell.findAll('p'):
                spell_desc += spell_desc_item.getText() + ' '

            # If we have extracted spell description, go add association
            if len(spell_desc) != 0:
                spells_data[spell_name] = spell_desc[:-1]
        except:
            characters_with_errors.append(
                'Spell name {} has been encountered an error during translation for {}'.format(spell_name_extracted, name))

    character_json = {}
    character_json[json_Character__background] = skins_map
    character_json[json_Character__clan] = clan
    character_json[json_Character__life_points] = life_points
    character_json[json_Character__lord] = lord
    character_json[json_Character__name] = name
    character_json[json_Character__url] = character_url
    spells_json = []
    for spell_name, spell_desc in spells_data.items():
        spell_json = {}
        spell_json[json_Spell__name] = spell_name
        spell_json[json_Spell__description] = spell_desc
        spells_json.append(spell_json)
    character_json[json_Character__spells] = spells_json

    # Adding character in the main list
    characters_json_data[json_CharactersManager__characters].append(
        character_json)

# Write output characters JSON file
print('Writing characters.json file')
characters_json_file = codecs.open('characters.json', 'w', 'utf-8')
characters_json_file.write(json.dumps(
    characters_json_data, sort_keys=True, indent=4, ensure_ascii=False))
characters_json_file.close()

# Output error(s)
print('--- Errors found ---')
for error in characters_with_errors:
    print(error.encode('ascii', 'ignore'))
