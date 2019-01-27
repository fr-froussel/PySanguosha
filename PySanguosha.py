import TextWrapper
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

# Nom
img_name = Image.new("RGB", (100, 100))
draw = ImageDraw.Draw(img_name)
font = ImageFont.truetype("arial.ttf", 16)
draw.text((0, 0), "Sample Text", (255,255,255), font=font, direction='ttb')
#
img_name.save('out_name.png')

img_final.save('out.png')

lines = TextWrapper.draw_text("coucou ceci est un test", 500)
print("Lines wrapped:", lines)