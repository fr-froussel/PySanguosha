from lib.backend import Clan
from lib.TextWrapper import TextWrapper
from lib.utils import *
from math import floor
from PIL import Image, ImageDraw, ImageEnhance, ImageFont


class ClanUI:
    def __init__(self, main, main_lord, magatama, skill, skill_up, skill_middle, skill_down):
        """
        Construct clan UI resources association
        :param main: main image resource path
        :param main_lord: main lord image resource path
        :param magatama: life point resource path
        :param skill: skill name resource path
        :param skill_up: skill description resource path
        :param skill_middle: skill description resource path
        :param skill_down: skill description resource path
        """
        self.__main = main
        self.__main_lord = main_lord
        self.__magatama = magatama
        self.__skill = skill
        self.__skill_up = skill_up
        self.__skill_middle = skill_middle
        self.__skill_down = skill_down

    @property
    def main(self):
        return self.__main

    @property
    def main_lord(self):
        return self.__main_lord

    @property
    def magatama(self):
        return self.__magatama

    @property
    def skill(self):
        return self.__skill

    @property
    def skill_up(self):
        return self.__skill_up

    @property
    def skill_middle(self):
        return self.__skill_middle

    @property
    def skill_down(self):
        return self.__skill_down


clan_ui_resources = \
    {
        Clan.GOD: ClanUI(
            './resources/cards/front/god.png',
            './resources/cards/front/god.png',
            './resources/cards/front/god-magatama.png',
            './resources/cards/front/god-skill.png',
            './resources/cards/front/god-skill-up.png',
            './resources/cards/front/god-skill-middle.png',
            './resources/cards/front/god-skill-down.png',
        ),
        Clan.QUN: ClanUI(
            './resources/cards/front/qun.png',
            './resources/cards/front/qun-lord.png',
            './resources/cards/front/qun-magatama.png',
            './resources/cards/front/qun-skill.png',
            './resources/cards/front/qun-skill-up.png',
            './resources/cards/front/qun-skill-middle.png',
            './resources/cards/front/qun-skill-down.png',
        ),
        Clan.SHU: ClanUI(
            './resources/cards/front/shu.png',
            './resources/cards/front/shu-lord.png',
            './resources/cards/front/shu-magatama.png',
            './resources/cards/front/shu-skill.png',
            './resources/cards/front/shu-skill-up.png',
            './resources/cards/front/shu-skill-middle.png',
            './resources/cards/front/shu-skill-down.png',
        ),
        Clan.WEI: ClanUI(
            './resources/cards/front/wei.png',
            './resources/cards/front/wei-lord.png',
            './resources/cards/front/wei-magatama.png',
            './resources/cards/front/wei-skill.png',
            './resources/cards/front/wei-skill-up.png',
            './resources/cards/front/wei-skill-middle.png',
            './resources/cards/front/wei-skill-down.png',
        ),
        Clan.WU: ClanUI(
            './resources/cards/front/wu.png',
            './resources/cards/front/wu-lord.png',
            './resources/cards/front/wu-magatama.png',
            './resources/cards/front/wu-skill.png',
            './resources/cards/front/wu-skill-up.png',
            './resources/cards/front/wu-skill-middle.png',
            './resources/cards/front/wu-skill-down.png',
        )
    }


class SpellUI:
    def __init__(self, spell, clan_ui):
        """
        Spell class constructor
        :param spell: spell
        """
        self.__spell = spell
        self.__clan_ui = clan_ui
        self.__ui = ''

    @property
    def spell(self):
        return self.__spell

    @property
    def clan_ui(self):
        return self.__clan_ui

    @property
    def ui(self):
        return self.__ui

    def generate_ui(self, font):
        # Generation status
        generation_status = False

        # Extract max spell size
        max_width = max_spells_size[0]
        max_height = max_spells_size[1]

        lines = TextWrapper.wrap_text_by_width(self.__spell.description, font, max_width)
        _, lines_size = TextWrapper.text_size(lines, font)

        # go write text if condition is ok
        if lines_size[1] < max_height:
            # Skill data
            skill_name_img = Image.open(self.__clan_ui.skill)
            _, first_line_text_size = TextWrapper.text_size(lines[0], font)

            # Generate skill UI
            spell_size = (skill_name_img.size[0] + max_width,
                          lines_size[1] + floor(spell_arrow_size/2) - floor(first_line_text_size[1]/2))
            spell_image = Image.new('RGBA', spell_size)
            spell_draw = ImageDraw.Draw(spell_image)

            # Add skill name text
            _, spell_name_size = TextWrapper.text_size(self.__spell.name, font)
            spell_name_pos = (spell_name_base_pos[0], floor(spell_name_base_pos[1]/2) + floor(spell_name_size[1]/2))
            spell_name_draw = ImageDraw.Draw(skill_name_img)
            spell_name_draw.text(spell_name_pos, self.__spell.name, (0, 0, 0), font=font)

            # Add skill UI name
            spell_image.paste(skill_name_img, mask=skill_name_img)

            # Add skill description text
            current_text_pos = [skill_name_img.size[0] - floor(spell_arrow_size/2),
                                floor(spell_arrow_size/2) - floor(first_line_text_size[1]/2)]
            desc_offset_after_arrow = 2
            for line in lines:
                spell_draw.text((current_text_pos[0] + floor(spell_arrow_size/2) + desc_offset_after_arrow,
                                 current_text_pos[1]),
                                line,
                                (0, 0, 0),
                                font=font)
                _, text_size = TextWrapper.text_size(line, font)
                current_text_pos[1] += text_size[1]

            # Write spell image
            self.__ui = spell_image

            # Status is ok
            generation_status = True

        return generation_status

class SpellsUIManager:
    def __init__(self, spells, clan_ui):
        """
        Spells UI manager
        :param spells: spells list
        :param clan_ui: general clan
        """
        self.__spells = []
        self.__generation_status = False
        self.__cumulated_height = 0
        self.__ui = None

        # Launch UI generation
        if not self.generate_ui(spells, clan_ui):
            print('Error during spells UI generation')

    @property
    def spells(self):
        return self.__spells

    @property
    def generation_status(self):
        return self.__generation_status

    @property
    def cumulated_height(self):
        return self.__cumulated_height

    @property
    def ui(self):
        return self.__ui

    def add_spell(self, spell):
        self.__spells.append(spell)

    def generate_ui(self, spells, clan_ui):
        # Font size possible to write spells text
        font_size_possible = (13, 11)

        # Extract max spell size
        max_width = max_spells_size[0]
        max_height = max_spells_size[1]

        # Loop through all font size possible to generate spell UI
        for font_size in font_size_possible:
            if not self.generate_ui_with_specific_font_size(spells, clan_ui, font_size):
                print("Cannot generate this image with font size {}").format(font_size)

            # Check if all UI generated are within size limits
            self.__cumulated_height = 0
            spell_width = 0
            for spell in self.spells:
                self.__cumulated_height += spell.ui.size[1]
                if spell_width == 0:
                    spell_width = spell.ui.size[0]

            # If all cumulated height are within max_height, it's ok
            if self.cumulated_height < max_height:
                skill_name_img = Image.open(clan_ui.skill)
                skill_desc_up_img = Image.open(clan_ui.skill_up)
                skill_desc_middle_img = Image.open(clan_ui.skill_middle)
                skill_desc_middle_img = skill_desc_middle_img.resize((skill_desc_middle_img.size[0], self.cumulated_height))
                skill_desc_down_img = Image.open(clan_ui.skill_down)

                spells_size = (skill_name_img.size[0] + skill_desc_middle_img.size[0]- floor(spell_arrow_size/2),
                               skill_desc_up_img.size[1] + self.cumulated_height + skill_desc_down_img.size[1])
                spells_image = Image.new('RGBA', spells_size)

                base_pos = (0, 0)
                skill_desc_middle_base_x = base_pos[0] + skill_name_img.size[0] - floor(spell_arrow_size/2)
                skill_desc_up_img_pos = (skill_desc_middle_base_x, base_pos[1])
                skill_desc_middle_img_pos = (skill_desc_middle_base_x, base_pos[1] + skill_desc_up_img.size[1])
                spells_img_base_pos = (base_pos[0],
                                  skill_desc_up_img_pos[1] + skill_desc_up_img.size[1])
                skill_desc_down_img_pos = (skill_desc_middle_base_x,
                                  spells_img_base_pos[1] + self.cumulated_height)

                spells_image.paste(skill_desc_up_img, skill_desc_up_img_pos)
                spells_image.paste(skill_desc_middle_img, skill_desc_middle_img_pos)
                previous_spell_height = spells_img_base_pos[1]
                for spell in self.spells:
                    spell_ui = spell.ui
                    spells_image.paste(spell_ui, (spells_img_base_pos[0], previous_spell_height), mask=spell_ui)
                    previous_spell_height += spell_ui.size[1]
                spells_image.paste(skill_desc_down_img, skill_desc_down_img_pos)

                self.__ui = spells_image

                self.__generation_status = True
                break
            # Condition not satisfied, clear all SpellUI
            else:
                self.__spells.clear()

        return self.__generation_status

    def generate_ui_with_specific_font_size(self, spells, clan_ui, font_size):
        generation_status = True

        # Loop through all spells to generate UI
        for spell in spells:
            font = ImageFont.truetype('resources/font/arial.ttf',
                                      size=TextWrapper.pixel_to_points(font_size),
                                      encoding='unic')

            self.__spells.append(SpellUI(spell, clan_ui))
            generation_status = (generation_status and self.__spells[-1].generate_ui(font))

        return generation_status


class CharacterUI:
    def __init__(self, character):
        """
        CharacterUI constructor
        :param character: Character object
        """
        self.__character = character
        self.__clan_ui = clan_ui_resources.get(character.clan)
        self.__spells_ui_manager = SpellsUIManager(character.spells, self.__clan_ui)
        self.__additionals_ui_ready = False

        # If spells generation is ok, go generate character UI
        self.__additionals_ui_ready = self.__spells_ui_manager.generation_status

    @property
    def character(self):
        return self.__character

    @property
    def additionals_ui_ready(self):
        return self.__additionals_ui_ready

    def generate_ui(self):
        # Main UI border
        main = ''
        if not self.__character.lord:
            main = Image.open(self.__clan_ui.main)
        else:
            main = Image.open(self.__clan_ui.main_lord)
        main_w, main_h = main.size

        # Life points UI
        magatama = Image.open(self.__clan_ui.magatama)
        magatama_w, magatama_h = magatama.size

        # Character background UI
        character_background = Image.open(self.__character.background)
        # # Resize background to fit with main UI
        desired_character_background_width = 309
        desired_character_background_height = 445
        left_crop = ((character_background.size[0] - desired_character_background_width) / 2)
        top_crop = ((character_background.size[1] - desired_character_background_height) / 2)
        character_background.crop((left_crop,
                                  top_crop,
                                  left_crop + desired_character_background_width,
                                  top_crop + desired_character_background_height))
        enhancer = ImageEnhance.Brightness(character_background)
        character_background = enhancer.enhance(0.80)

        # Composition
        character_image = Image.new('RGBA', (main_w, main_h))

        # Start compose the image
        # # Background
        character_image.paste(character_background, (50, 50))
        # # Main border
        character_image.paste(main, (0, 0), mask=main)
        # # Life points
        magamatame_heigth_position = 20
        magatama_width_base_position = 100
        for magatama_number in range(self.__character.life_points):
            magatama_previous_width_position = magatama_width_base_position + (int(magatama_w * magatama_number))
            character_image.paste(magatama, (magatama_previous_width_position, magamatame_heigth_position), mask=magatama)
        # Spells
        spells_base_pos = (21, main.size[1] - self.__spells_ui_manager.cumulated_height - 60)
        character_image.paste(self.__spells_ui_manager.ui, spells_base_pos, mask=self.__spells_ui_manager.ui)

        # Save generated image
        character_image.save('generation/' + self.__character.name.replace(' ', '_') + '.png')
