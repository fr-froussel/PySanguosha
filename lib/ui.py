from lib.backend import Clan, Character, Spell
from lib.TextWrapper import TextWrapper
from lib.utils import *
from math import floor
from PIL import Image, ImageDraw, ImageEnhance, ImageFont


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
            spell_image.paste(skill_desc_up_img, skill_desc_up_pos)
            spell_image.paste(skill_desc_middle_img, skill_desc_middle_pos)
            spell_image.paste(skill_desc_down_img, skill_desc_bottom_pos)
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

    def add_spell(self, spell):
        self.__spells.append(spell)

    def generate_ui(self, spells, clan_ui):
        # Font size possible to write spells text
        font_size_possible = (13, 11)

        # Extract max spell size
        max_height = max_spells_size[1]

        # Loop through all font size possible to generate spell UI
        for font_size in font_size_possible:
            if not self.generate_ui_with_specific_font_size(spells, clan_ui, font_size):
                print("Cannot generate this image with font size {}").format(font_size)

            # Check if all UI generated are within size limits
            self.__cumulated_height = 0
            for spell in self.spells:
                self.__cumulated_height += spell.ui.size[1]

            # If all cumulated height are within max_height, it's ok
            if self.__cumulated_height < max_height:
                self.__generation_status = True
                break

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
        self.__additionals_ui_ready = False

        # If spells generation is ok, go generate character UI
        self.__additionals_ui_ready = self.__spells_ui_manager.generation_status

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
        character_background = Image.open(self.__background)
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
        # # Spells
        spell_base_width = 18
        previous_spell_height = main.size[1] - self.__spells_ui_manager.cumulated_height - 35
        for spell in self.__spells_ui_manager.spells:
            spell_ui = spell.ui
            character_image.paste(spell_ui, (spell_base_width, previous_spell_height), mask=spell_ui)
            previous_spell_height += spell_ui.size[1]

        # Save generated image
        character_image.save('generation/' + self.__character.name.replace(' ', '_') + '.png')
