from lib.backend import Clan
from lib.TextWrapper import TextWrapper
from lib.utils import *
from math import floor
from PIL import Image, ImageDraw, ImageEnhance, ImageFont


class ClanUI:
    def __init__(self, main, main_lord, magatama, magatama_lord,
                 skill, skill_name_text_color, skill_up, skill_middle, skill_down):
        """
        Construct clan UI resources association
        :param main: main image resource path
        :param main_lord: main lord image resource path
        :param magatama: life point resource path
        :param skill: skill name resource path
        :param skill_name_text_color: skill name text color
        :param skill_up: skill description resource path
        :param skill_middle: skill description resource path
        :param skill_down: skill description resource path
        """
        self.__main = main
        self.__main_lord = main_lord
        self.__magatama = magatama
        self.__magatama_lord = magatama_lord
        self.__skill = skill
        self.__skill_name_text_color = skill_name_text_color
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
    def magatama_lord(self):
        return self.__magatama_lord

    @property
    def skill(self):
        return self.__skill

    @property
    def skill_name_text_color(self):
        return self.__skill_name_text_color

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
            './resources/cards/front/god-magatama.png',
            './resources/cards/front/god-skill.png',
            'white',
            './resources/cards/front/god-skill-up.png',
            './resources/cards/front/god-skill-middle.png',
            './resources/cards/front/god-skill-down.png',
        ),
        Clan.QUN: ClanUI(
            './resources/cards/front/qun.png',
            './resources/cards/front/qun-lord.png',
            './resources/cards/front/qun-magatama.png',
            './resources/cards/front/god-magatama.png',
            './resources/cards/front/qun-skill.png',
            'black',
            './resources/cards/front/qun-skill-up.png',
            './resources/cards/front/qun-skill-middle.png',
            './resources/cards/front/qun-skill-down.png',
        ),
        Clan.SHU: ClanUI(
            './resources/cards/front/shu.png',
            './resources/cards/front/shu-lord.png',
            './resources/cards/front/shu-magatama.png',
            './resources/cards/front/god-magatama.png',
            './resources/cards/front/shu-skill.png',
            'black',
            './resources/cards/front/shu-skill-up.png',
            './resources/cards/front/shu-skill-middle.png',
            './resources/cards/front/shu-skill-down.png',
        ),
        Clan.WEI: ClanUI(
            './resources/cards/front/wei.png',
            './resources/cards/front/wei-lord.png',
            './resources/cards/front/wei-magatama.png',
            './resources/cards/front/god-magatama.png',
            './resources/cards/front/wei-skill.png',
            'black',
            './resources/cards/front/wei-skill-up.png',
            './resources/cards/front/wei-skill-middle.png',
            './resources/cards/front/wei-skill-down.png',
        ),
        Clan.WU: ClanUI(
            './resources/cards/front/wu.png',
            './resources/cards/front/wu-lord.png',
            './resources/cards/front/wu-magatama.png',
            './resources/cards/front/god-magatama.png',
            './resources/cards/front/wu-skill.png',
            'black',
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

    def generate_ui(self, font_description, font_name):
        # Skill description text wrap
        description_lines = TextWrapper.wrap_text_by_width(self.__spell.description,
                                                           font_description,
                                                           TextWrapper.pixel_to_points(max_spells_size[0]))
        _, description_lines_size = TextWrapper.text_size(description_lines, font_description)
        _, first_description_line_text_size = TextWrapper.text_size(description_lines[0], font_description)
        # Skill name text wrap
        name_lines = TextWrapper.wrap_text_by_width(self.__spell.name,
                                                    font_name,
                                                    TextWrapper.pixel_to_points(spell_name_size[0]))
        _, name_lines_size = TextWrapper.text_size(name_lines, font_name)

        # Skill name image
        skill_name_img = Image.open(self.__clan_ui.skill)

        # Generate skill UI
        desc_offset_after_arrow = 2
        spell_size = (skill_name_img.size[0] + max_spells_size[0] + desc_offset_after_arrow,
                      description_lines_size[1] + floor(spell_arrow_size/2))
        spell_image = Image.new('RGBA', spell_size)
        spell_draw = ImageDraw.Draw(spell_image)

        # Add skill UI name
        spell_name_draw = ImageDraw.Draw(skill_name_img)
        spell_name_pos = (spell_name_base_pos[0],
                          spell_name_base_pos[1] + floor(name_lines_size[1] / 4))
        spell_name_text_color = 'black'
        spell_name_draw.text(spell_name_pos, self.__spell.name, self.__clan_ui.skill_name_text_color, font=font_name)
        spell_image.paste(skill_name_img, mask=skill_name_img)

        # Add skill description text
        current_text_pos = [skill_name_img.size[0] - floor(spell_arrow_size/2),
                            floor(spell_arrow_size/2) - floor(first_description_line_text_size[1]/2)]
        for line in description_lines:
            spell_draw.text((current_text_pos[0] + floor(spell_arrow_size/2) + desc_offset_after_arrow,
                             current_text_pos[1]),
                            line,
                            'black',
                            font=font_description)
            _, text_size = TextWrapper.text_size(line, font_description)
            current_text_pos[1] += text_size[1]

        # Write spell image
        self.__ui = spell_image

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
        generation_status = False

        # Font size possible to write spells text
        font_size_possible = [13, 11, 9]

        have_found_font_description = False
        have_found_font_name = False
        # Loop through all font size possible to generate spell UI
        for font_size in font_size_possible:
            # Cumulated height for all spells for a specific font size
            self.__cumulated_height = 0

            # Create description if not found
            if not have_found_font_description:
                font_description = ImageFont.truetype('resources/font/arial.ttf',
                                                      size=TextWrapper.pixel_to_points(font_size),
                                                      encoding='unic')

                # Loop through spells to calculate the best font size
                for spell in spells:
                    # Text wrapper
                    description_lines = TextWrapper.wrap_text_by_width(spell.description,
                                                                       font_description,
                                                                       TextWrapper.pixel_to_points(max_spells_size[0]))
                    _, description_lines_size = TextWrapper.text_size(description_lines, font_description)

                    # Adding cumulated_height
                    self.__cumulated_height += description_lines_size[1] + floor(spell_arrow_size/2)

            # Create description if not found
            if not have_found_font_name:
                font_name = ImageFont.truetype('resources/font/arial.ttf',
                                               size=TextWrapper.pixel_to_points(font_size),
                                               encoding='unic')

                # Loop through spells to calculate the best font size
                for spell in spells:
                    # Text wrapper
                    name_lines = TextWrapper.wrap_text_by_width(spell.name,
                                                                font_name,
                                                                TextWrapper.pixel_to_points(spell_name_size[0]))
                    _, name_lines_size = TextWrapper.text_size(name_lines, font_name)

                    # Check if we have respect the maximum width
                    if name_lines_size[0] < spell_name_size[0]:
                        have_found_font_name = True
                    else:
                        have_found_font_name = False

            # If cumulated_heigth < max_height, it's ok, go generate all spell UI with this font
            self.__cumulated_height += floor(spell_arrow_size/2)
            if (self.__cumulated_height < max_spells_size[1]) and have_found_font_name:
                have_found_font_description = True
                generation_status = True

                # Loop through spells to generate UI
                for spell in spells:
                    self.__spells.append(SpellUI(spell, clan_ui))
                    self.__spells[-1].generate_ui(font_description, font_name)
                break

        if generation_status:
            skill_name_img = Image.open(clan_ui.skill)
            skill_desc_up_img = Image.open(clan_ui.skill_up)
            skill_desc_middle_img = Image.open(clan_ui.skill_middle)
            skill_desc_middle_img = skill_desc_middle_img.resize((skill_desc_middle_img.size[0],
                                                                  self.__cumulated_height - floor(spell_arrow_size/2)))
            skill_desc_down_img = Image.open(clan_ui.skill_down)

            spells_size = (skill_name_img.size[0] + skill_desc_middle_img.size[0] - floor(spell_arrow_size/2),
                           skill_desc_up_img.size[1] + skill_desc_middle_img.size[1] + skill_desc_down_img.size[1])
            spells_image = Image.new('RGBA', spells_size)

            base_pos = (0, 0)
            skill_desc_middle_base_x = base_pos[0] + skill_name_img.size[0] - floor(spell_arrow_size/2)
            skill_desc_up_img_pos = (skill_desc_middle_base_x, base_pos[1])
            skill_desc_middle_img_pos = (skill_desc_middle_base_x, base_pos[1] + skill_desc_up_img.size[1])
            skill_desc_down_img_pos = (skill_desc_middle_base_x,
                                       base_pos[1] + \
                                       skill_desc_middle_img_pos[1] + skill_desc_middle_img.size[1])

            # Paste spells UI
            spells_image.paste(skill_desc_up_img, skill_desc_up_img_pos)
            spells_image.paste(skill_desc_middle_img, skill_desc_middle_img_pos)
            spells_image.paste(skill_desc_down_img, skill_desc_down_img_pos)

            # Write spells text
            spells_img_base_pos = (base_pos[0], skill_desc_up_img.size[1])
            previous_spell_height = spells_img_base_pos[1]
            for spell in self.spells:
                spells_image.paste(spell.ui, (spells_img_base_pos[0], previous_spell_height), mask=spell.ui)
                previous_spell_height += spell.ui.size[1]

            # Write final data in variables
            self.__ui = spells_image
            self.__generation_status = True
        # Condition not satisfied, clear all SpellUI
        else:
            self.__spells.clear()

        self.__generation_status = generation_status

        return self.__generation_status


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
        if not self.character.lord:
            magatama = Image.open(self.__clan_ui.magatama)
        else:
            magatama = Image.open(self.__clan_ui.magatama_lord)
        magatama_w, magatama_h = magatama.size

        # Character background UI
        character_background = Image.open(self.__character.background)
        # # Resize background to fit with main UI
        desired_character_background_width = background_size[0]
        desired_character_background_height = background_size[1]
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
        character_image.paste(character_background, background_base_pos)
        # # Main border
        character_image.paste(main, (0, 0), mask=main)
        # # Life points
        magamatame_heigth_position = 20
        magatama_width_base_position = 100
        for magatama_number in range(self.__character.life_points):
            magatama_previous_width_position = magatama_width_base_position + (int(magatama_w * magatama_number))
            character_image.paste(magatama, (magatama_previous_width_position, magamatame_heigth_position), mask=magatama)
        # # Character name
        character_image_draw = ImageDraw.Draw(character_image)
        character_name_formatted = ''
        for letter in self.character.name:
            character_name_formatted += letter + '\n'

        # # # Find the best font size for the text
        status, _, font, font_size, _ = optimize_text_font_size_based_on_max_size(character_name_formatted,
                                                                                  'resources/font/ComicSansMSBold.ttf',
                                                                                  character_name_size,
                                                                                  True)
        if status:
            character_name_pos = (
            character_name_base_pos[0] + floor(character_name_base_pos[0] / 2) - floor(font_size / 2) - 2,
            character_name_base_pos[1])

            if self.__character.god:
                character_name_pos = (
                character_god_name_base_pos[0] + floor(character_god_name_base_pos[0] / 2) - floor(font_size / 2) - 2,
                character_god_name_base_pos[1])

            add_thicker_border_to_text(character_image_draw,
                                       character_name_pos,
                                       character_name_formatted,
                                       font,
                                       'white',
                                       'black')
        else:
            print('Cannot insert character name for {}'.format(self.character.name))

        # # Spells
        skill_desc_up_img = Image.open(self.__clan_ui.skill_up)
        skill_desc_down_img = Image.open(self.__clan_ui.skill_down)
        spells_base_pos = (20,
                           main.size[1] - main_border[2] - skill_desc_up_img.size[1]
                           - floor(skill_desc_down_img.size[1]/2) - self.__spells_ui_manager.cumulated_height)
        character_image.paste(self.__spells_ui_manager.ui, spells_base_pos, mask=self.__spells_ui_manager.ui)

        # Save generated image
        character_image.save(generation_directory + self.__character.name.replace(' ', '_') + '.png')
