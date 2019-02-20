from lib.backend import Clan, Character, Spell
from lib.TextWrapper import TextWrapper
from lib.utils import *
from math import floor
from PIL import Image, ImageDraw, ImageFont


class SpellUI:
    def __init__(self, spell, clan_ui):
        """
        Spell class constructor
        :param spell: spell
        """
        self.__spell = spell
        self.__clan_ui = clan_ui

        font = ImageFont.truetype('resources/font/arial.ttf', size=TextWrapper.pixel_to_points(15), encoding='unic')
        self.generate_ui(font, 225, 480)

    def generate_ui(self, font, max_width, max_height):
        lines = TextWrapper.wrap_text_by_width(self.__spell.description, font, max_width)
        _, lines_size = TextWrapper.text_size(lines, font)

        # go write text if condition is ok
        if lines_size[1] < max_height:
            # Skill UI: name and description
            skill_desc_img = Image.open(self.__clan_ui.skill)
            skill_desc_up_img = Image.open(self.__clan_ui.skill_up)
            skill_desc_middle_img = Image.open(self.__clan_ui.skill_middle)
            skill_desc_down_img = Image.open(self.__clan_ui.skill_down)

            # Skill UI middle description height adaption based on description height
            skill_desc_middle_new_size = ((skill_desc_middle_img.size[0],
                                           lines_size[1] - skill_desc_up_img.size[1] - skill_desc_down_img.size[1] + 12))
            skill_desc_middle_img = skill_desc_middle_img.resize(skill_desc_middle_new_size)

            # Skill UI position
            base_pos = [0, 0]
            spacement = -10  # Negative spacement UI combination
            skill_desc_base_pos_x = base_pos[0] + skill_desc_img.size[0] + spacement
            skill_desc_up_pos = (skill_desc_base_pos_x, base_pos[1])
            skill_desc_middle_pos = (skill_desc_base_pos_x, base_pos[1] + skill_desc_up_img.size[1])
            skill_desc_bottom_pos = (skill_desc_base_pos_x,
                                     base_pos[1] + skill_desc_middle_pos[1] + skill_desc_middle_img.size[1])

            # Generate skill UI
            spell_size = (skill_desc_img.size[0] + skill_desc_middle_img.size[0] + spacement,
                          skill_desc_up_img.size[1] + skill_desc_middle_img.size[1] + skill_desc_down_img.size[1])
            spell_image = Image.new('RGBA', spell_size)
            spell_draw = ImageDraw.Draw(spell_image)

            # Add skill UI description
            spell_image.paste(skill_desc_up_img, skill_desc_up_pos, mask=skill_desc_up_img)
            spell_image.paste(skill_desc_middle_img, skill_desc_middle_pos, mask=skill_desc_middle_img)
            spell_image.paste(skill_desc_down_img, skill_desc_bottom_pos, mask=skill_desc_down_img)
            # Add skill UI name
            spell_image.paste(skill_desc_img, base_pos, mask=skill_desc_img)

            # Add skill name text
            _, spell_name_size = TextWrapper.text_size(self.__spell.name, font)
            spell_name_pos = (10, floor(skill_desc_img.size[1] / 2) - floor(spell_name_size[1] / 2) - 2)
            spell_draw.text(spell_name_pos, self.__spell.name, (0, 0, 0), font=font)

            # Add skill description text
            current_text_pos = [skill_desc_base_pos_x, base_pos[0]]
            for line in lines:
                spell_draw.text((current_text_pos[0] + 16, current_text_pos[1] + 5), line, (0, 0, 0), font=font)
                _, text_size = TextWrapper.text_size(line, font)
                current_text_pos[1] += text_size[1]

            # Write spell image
            spell_image.save('generation/spell_' + self.__spell.name.replace(' ', '_') + '.png')


class CharacterUI:
    def __init__(self, character, background):
        """
        CharacterUI constructor
        :param character: Character object
        :param background: Background associated
        """
        self.__character = character
        self.__background = background
        self.__clan_ui = clan_ui_resources.get(character.clan)
        self.__spells_ui_manager = SpellsUIManager(character.spells, self.__clan_ui)


class SpellsUIManager:
    def __init__(self, spells, clan_ui):
        """
        Spells UI manager
        :param spells: spells list
        """
        self.__spells = []
        for spell in spells:
            self.__spells.append(SpellUI(spell, clan_ui))

    @property
    def spells(self):
        return self.__spells

    def add_spell(self, spell):
        self.__spells.append(spell)

