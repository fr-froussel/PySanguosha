from enum import Enum
from lib.text_wrapper import TextWrapper
from PIL import ImageFont

generation_directory = 'generation/'
spells_base_pos = [87, 375]
max_spells_size = (305, 175)
background_base_pos = (40, 50)
background_size = (285, 345)
main_border = (62, 12, 32, 15)
spell_name_base_pos = (10, 4)
spell_name_size = (41, 16)
spell_arrow_size = 24 # That's a square!
character_name_base_pos = (42, 100)
character_name_size = (25, 260)


class Clan(Enum):
    (
        GOD,
        QUN,
        SHU,
        WEI,
        WU
    ) = range(5)


clan_label_associations = {
  'Demigod': Clan.GOD,
  'Neutral': Clan.QUN,
  'Shu': Clan.SHU,
  'Wei': Clan.WEI,
  'Wu': Clan.WU,
}


def optimize_text_font_size_based_on_max_size(text, font_path, max_size, is_in_vertical_mode=False):
  # Possible font size
  font_size_possible = (27, 25, 23, 21, 19, 17, 15, 13, 11, 9)

  # Extract max size
  max_width = max_size[0]
  max_height = max_size[1]

  # Wrap text and test condition
  for font_size in font_size_possible:
    # Create font
    font = ImageFont.truetype(font_path, size=TextWrapper.pixel_to_points(font_size), encoding='unic')

    # Text wrapper
    lines = TextWrapper.wrap_text_by_width(text, font, max_width)
    _, lines_size = TextWrapper.text_size(lines, font, is_in_vertical_mode)

    # Go write text if condition is ok
    if (TextWrapper.points_to_pixel(lines_size[0]) <= max_width) and\
        (TextWrapper.points_to_pixel(lines_size[1]) <= max_height):
      return True, lines, font, font_size, lines_size

  # If no concordancy, return false
  return False, [''], None, 0, (0, 0)