from TextWrapper import TextWrapper
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

border = Image.open('./resources/cards/front/god.png')
border_w, border_h = border.size

magatama = Image.open('./resources/cards/front/god-magatama.png')
magatama_w, magatama_h = magatama.size

character = Image.open('./resources/cards/skins/2601.jpg')
character = character.resize((border_w-20, border_h-50))

img_final = Image.new('RGBA', (border_w, border_h))

img_final.paste(character, (20, 50))
img_final.paste(border, (0, 0), mask=border)

magamatame_heigth_position = 18
magatama_width_base_position = 85
magatama_previous_width_position = magatama_width_base_position
magatama_spacement = 3
for magatama_number in range(8):
  magatama_previous_width_position = magatama_width_base_position + (int(magatama_w * (magatama_number * 0.5))) + (magatama_number * magatama_spacement)
  img_final.paste(magatama, (magatama_previous_width_position, magamatame_heigth_position), mask=magatama)

# img_name = Image.new('RGB', (100, 100))
# draw = ImageDraw.Draw(img_name)
# font = ImageFont.truetype('arial.ttf', 16)
# draw.text((0, 0), "Sample Text", (255,255,255), font=font)
# img_name.save('out_name.png')

spells_base_pos = [85, 375]
spells_max_size = (250, 480)

spell_name_test = '司敵'
spell_text_test = 'Whenever Cao Zhen uses an escape or any other player uses an escape during Cao Zhen\'s turn, he puts the top card of the deck on his general card. At the beginning of any other players action phase, Cao Zhen can discard one of these cards to reduce the number of attacks that the current player can use by one.'

# create the ImageFont instance
font = ImageFont.truetype('resources/font/arial.ttf', size=TextWrapper.pixel_to_points(15), encoding='unic')
lines = TextWrapper.wrap_text_by_width(spell_text_test, font, spells_max_size[0])
_, lines_size = TextWrapper.text_size(lines, font)

# go write text if condition is ok
if lines_size[1] < spells_max_size[1]:
    current_text_pos = spells_base_pos
    draw = ImageDraw.Draw(img_final)

    # skill name UI
    skill = Image.open('./resources/cards/front/god-skill-new.png')
    skill_size = skill.size
    skill_pos = (current_text_pos[0] - skill_size[0], current_text_pos[1])
    img_final.paste(skill, skill_pos, mask=skill)

    # skill name
    spell_font = ImageFont.truetype('resources/font/SimSun.ttf', size=TextWrapper.pixel_to_points(20), encoding='unic')
    _, spell_name_size = TextWrapper.text_size(spell_name_test, spell_font)
    spell_name_pos = (skill_pos[0] + 7,
                      skill_pos[1] + int(skill_size[1] / 2) + 1 - int(spell_name_size[1] / 2))

    draw.text(spell_name_pos, spell_name_test, (255, 255, 255), font=spell_font)

    # skill text middle UI
    skill_middle = Image.open('./resources/cards/front/god-skill-middle.png')
    skill_middle = skill_middle.resize((skill_middle.size[0], lines_size[1]))
    img_final.paste(skill_middle, current_text_pos, mask=skill_middle)

    # skill text up UI
    skill_up = Image.open('./resources/cards/front/god-skill-up.png')
    img_final.paste(skill_up, (current_text_pos[0], current_text_pos[1] - skill_up.size[1]), mask=skill_up)

    # skill text down UI
    skill_down = Image.open('./resources/cards/front/god-skill-down.png')
    img_final.paste(skill_down, (current_text_pos[0], current_text_pos[1] + skill_middle.size[1]), mask=skill_down)

    # loop through lines to draw
    for line in lines:
        draw.text((current_text_pos[0] + 7, current_text_pos[1]), line, (0, 0, 0), font=font)
        _, text_size = TextWrapper.text_size(line, font)
        current_text_pos[1] += text_size[1]

# save final composition
img_final.save('out.png')
