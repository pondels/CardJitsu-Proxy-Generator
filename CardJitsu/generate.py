from PIL import Image, ImageDraw, ImageFont
import json

set_count = {
    '1': 110,
    '2': 19,
    '3': 68,
    '4': 68,
    '5': 28,
    '6': 110,
    '7': 150,
}

color_key = {
    'tri_color': {
        'f': None,
        's': None,
        'w': None,
    },
    'top_left': {
        'r': None,
        'o': None,
        'y': None,
        'g': None,
        'b': None,
        'p': None,
    },
    'penguin_set': {
        '1':    Image.open('./files/Set/1.png'),
        '2':    Image.open('./files/Set/2.png'),
        '3':    Image.open('./files/Set/3.png'),
        '4':    Image.open('./files/Set/4.png'),
        '5':    Image.open('./files/Set/5.png'),
        '6':    Image.open('./files/Set/6.png'),
        '7':    Image.open('./files/Set/7.png'),
        'rare': Image.open('./files/Set/rare.png'),
    },
    'numbers': {
        'mask': {
            '2':  Image.open('./files/Power/2/shadow.png'),
            '3':  Image.open('./files/Power/3/shadow.png'),
            '4':  Image.open('./files/Power/4/shadow.png'),
            '5':  Image.open('./files/Power/5/shadow.png'),
            '6':  Image.open('./files/Power/6/shadow.png'),
            '7':  Image.open('./files/Power/7/shadow.png'),
            '8':  Image.open('./files/Power/8/shadow.png'),
            '9':  Image.open('./files/Power/9/shadow.png'),
            '10': Image.open('./files/Power/10/shadow.png'),
            '11': Image.open('./files/Power/11/shadow.png'),
            '12': Image.open('./files/Power/12/shadow.png'),
        },
        'number': {
            '2':  Image.open('./files/Power/2/number.png'),
            '3':  Image.open('./files/Power/3/number.png'),
            '4':  Image.open('./files/Power/4/number.png'),
            '5':  Image.open('./files/Power/5/number.png'),
            '6':  Image.open('./files/Power/6/number.png'),
            '7':  Image.open('./files/Power/7/number.png'),
            '8':  Image.open('./files/Power/8/number.png'),
            '9':  Image.open('./files/Power/9/number.png'),
            '10': Image.open('./files/Power/10/number.png'),
            '11': Image.open('./files/Power/11/number.png'),
            '12': Image.open('./files/Power/12/number.png'),
        }
    },
    'symbols': {
        'mask': {
            'f': Image.open('./files/CardType/f/shadow.png'),
            'w': Image.open('./files/CardType/w/shadow.png'),
            's': Image.open('./files/CardType/s/shadow.png'),
        },
        'symbol': {
            'f': Image.open('./files/CardType/f/symbol.png'),
            'w': Image.open('./files/CardType/w/symbol.png'),
            's': Image.open('./files/CardType/s/symbol.png'),
        }
    },
    'abilities': {
        'block': {},
        'convert': {},
        'discard_all': {},
        'discard_one': {},
        'modify': {},
        '': {},
    },
    'basic': {
        'power_outline': Image.open('./files/Basic/power_card_outline.png'),
        'card_outline':  Image.open('./files/Basic/card_outline.png'),
        'power_bg':      Image.open('./files/Basic/power_card_text_background.png'),
    }
}

# Setting up the color key
def setTriColor(key, k1, k2, k3):
    bottom_background = Image.open('./files/Basic/bottom_background.png')
    image = bottom_background.load()
    for x in range(bottom_background.width):
        for y in range(bottom_background.height):
            if image[x, y][0] == 238:
                bottom_background.putpixel((x, y), k1) 
            if image[x, y][0] == 196: 
                bottom_background.putpixel((x, y), k2) 
            if image[x, y][0] == 132: 
                bottom_background.putpixel((x, y), k3)

    color_key['tri_color'][key] = bottom_background

def setTopLeft(key, k1):
    bottom_background = Image.open('./files/Basic/top_left_background.png')
    image = bottom_background.load()
    for x in range(bottom_background.width):
        for y in range(bottom_background.height):
            if image[x, y][0] == 53:
                bottom_background.putpixel((x, y), k1)

    color_key['top_left'][key] = bottom_background

# Setting up the bottom color images
setTriColor('f', (230, 130, 55),  (229, 90, 59),   (219, 42, 50))
setTriColor('s', (244, 244, 246), (230, 233, 234), (217, 220, 221))
setTriColor('w', (67, 127, 182),  (65, 102, 165),  (55, 69, 128))

# Setting up the top left colors
setTopLeft('p', (163, 153, 202))
setTopLeft('o', (248, 149, 43))
setTopLeft('g', (98, 184, 71))
setTopLeft('y', (251, 234, 44))
setTopLeft('b', (16, 72, 160))
setTopLeft('r', (227, 60, 37))

def getAbilityImage(description):
    description = description.lower()
    if 'cannot be played next round' in description:
        blocked_element = description.split('cannot')[0].split(',')[1].strip()[0]
        return Image.open(f'./files/Ability/Block/{blocked_element}.png')
    elif f"discard one" in description:
        discard_type = description.split('opponent\'s')[1].strip()[0]
        return Image.open(f'./files/Ability/DiscardOne/{discard_type}.png')
    elif 'cards become' in description:
        split_desc = description.split('cards become')
        first = split_desc[0].strip().split(' ')[-1]
        second = split_desc[1].strip().split(' ')[0]
        return Image.open(f'./files/Ability/Convert/{first}_to_{second}.png')
    elif 'discard all' in description:
        discard_type = description.split('opponent\'s')[1].strip()[0]
        return Image.open(f'./files/Ability/DiscardAll/{discard_type}.png')
    elif '-2' in description:
        return Image.open(f'./files/Ability/Modify/-2.png')
    elif '+2' in description:
        return Image.open(f'./files/Ability/Modify/+2.png')
    elif 'lower values win' in description:
        return Image.open(f'./files/Ability/Modify/reverse_value.png')
    else: print(f'SOMETHING WENT WRONG: {description}')

def mapPowerCard(image: Image, white_mask: Image, data: dict):
    # Drawing Black Ability Background
    ability_bg = color_key['basic']['power_bg'].copy()
    image.paste(ability_bg, mask=ability_bg)

    # Ability white bar to mask
    ability_outline = color_key['basic']['power_outline'].copy()
    white_mask.paste(ability_outline, mask=ability_outline)

    mask_data = white_mask.load()
    for x in range(white_mask.width):
        for y in range(white_mask.height):
            # We found pixel data, nuke it from the original
            if mask_data[x, y][0] != 0 or mask_data[x, y][1] != 0 or mask_data[x, y][2] != 0:
                image.putpixel((x, y), (0, 0, 0, 0))

    # Adding ability image in top right
    ability_image = getAbilityImage(data['description'])
    image.paste(ability_image, mask=ability_image)

def getFlavorText(data: dict):
    final_text = ['']
    for word in data['flavor_text'].split(' '):
        if flavor_font.getlength(final_text[-1] + word) > 650:
            final_text.append('')

        final_text[-1] += f'{word} '

    return '\n'.join(final_text)

with open('scrape/new_cards.json', 'r') as file:
    cards_json = json.load(file)

title_font  = ImageFont.truetype('./fonts/candombe.otf', 75)
flavor_font = ImageFont.truetype('./fonts/candombe.otf', 37)

# Some cards need slight offsets. This is a generic template of those offsets
tiny_down = 25
low_down = 50
med_down = 100
high_down = 150
tiny_up = -25
low_up = -50
med_up = -100
high_up = -150
offset_lookup = {

    # Set 1 custom offsets
    '2': med_down,
    '4': low_down,
    '7': low_down,
    '13': low_down,
    '62': low_down,
    '64': low_down,
    '71': med_up,
    '73': low_up,
    '74': tiny_up,
    '75': low_up,
    '76': low_up,
    '90': low_up,

    # Set 2 custom offsets
    '98': med_down,

    # Set 3 custom offsets
    '202': low_down,
    '206': low_down,
    '211': low_down,
    '225': low_down,
    '227': low_down,
    '228': low_down,
    '230': low_down,
    '231': med_down,
    '232': low_down,
    '235': low_down,
    '245': low_down,
    '246': low_down,
    '253': med_up,
    '254': med_up,
    '255': med_up,
    '256': low_down,
    '257': med_down,
}

for card_num, data in cards_json.items():

    if data['set_id'] != '3': continue

    # Opening the card image
    image = Image.new(mode='RGBA', size=(750, 1050))
    card_image = Image.open(f'./downloaded_cards/{card_num}.png')
    card_image = card_image.resize((850, 850))
    y_offset = offset_lookup.get(card_num, 0)
    image.paste(card_image, (-50, -100+y_offset))

    # Drawing the bottom 3 colors based on the element
    color_background = color_key['tri_color'][data['element']].copy()
    image.paste(color_background, mask=color_background)

    # Top Left Color
    color_top_left = color_key['top_left'][data['color']].copy()
    image.paste(color_top_left, mask=color_top_left)

    # Drawing the Set Penguin
    penguin_set = color_key['penguin_set'][data['set_id']].copy()
    image.paste(penguin_set, mask=penguin_set)

    # Symbol and number shadow to mask
    white_mask = Image.new('RGBA', (750, 1050))

    # Adding card frame to mask
    card_outline = color_key['basic']['card_outline'].copy()
    white_mask.paste(card_outline, mask=card_outline)

    # Adding element and power background to mask
    element_mask = color_key['symbols']['mask'][data['element']].copy()
    white_mask.paste(element_mask, mask=element_mask)
    power_mask = color_key['numbers']['mask'][data['value']].copy()
    white_mask.paste(power_mask, mask=power_mask)

    # Card title to mask if not snow, otherwise, black text to original
    reg_text_drawer = ImageDraw.Draw(image)
    mask_text_drawer = ImageDraw.Draw(white_mask)
    text_radius = title_font.getlength(data['label'].upper()) // 2

    flavor_text = getFlavorText(data)
    if data['element'] == 's':
        reg_text_drawer.text((375-text_radius, 710), data['label'].upper(), font=title_font, fill=(0, 0, 0))
        reg_text_drawer.text((50, 790), flavor_text, font=flavor_font, fill=(0, 0, 0))
    else:
        mask_text_drawer.text((375-text_radius, 710), data['label'].upper(), font=title_font, fill=(255, 255, 255))
        reg_text_drawer.text((50, 790), flavor_text, font=flavor_font, fill=(255, 255, 255))

    reg_text_drawer.text((615, 960), f'{data["card_id"] if len(data["card_id"]) < 3 else data["card_id"][1:]}/{set_count[data["set_id"]]}', font=flavor_font, fill=(0, 0, 0))
    description = data.get('description').upper()
    if description:
        if data['element'] == 's':
            reg_text_drawer.text((560, 925), 'POWER CARD', font=flavor_font, fill=(0, 0, 0))
        else:
            mask_text_drawer.text((560, 925), 'POWER CARD', font=flavor_font, fill=(255, 255, 255))

        mapPowerCard(image, white_mask, data)
        desc_split = description.split(', ')
        top_radius = flavor_font.getlength(f'{desc_split[0]},') // 2
        bot_radius = flavor_font.getlength(desc_split[1]) // 2
        reg_text_drawer.text((375-top_radius, 610), f'{desc_split[0]},', font=flavor_font, fill=(255, 255, 255))
        reg_text_drawer.text((375-bot_radius, 645), desc_split[1],       font=flavor_font, fill=(255, 255, 255))
    else:
        # Pasting the mask on
        image.paste(white_mask, mask=white_mask)

    # Adding Symbol and Power images
    element_mask = color_key['symbols']['symbol'][data['element']].copy()
    image.paste(element_mask, mask=element_mask)
    power_mask = color_key['numbers']['number'][data['value']].copy()
    image.paste(power_mask, mask=power_mask)

    # Saving the image to our generated cards
    image.save(f'./generated_cards/set{data["set_id"]}/{card_num}.png')

# Automating placing all the cards on sheets of paper.

# 300 pixels per inch
# width  = int(8.5 * 300)
# height = int(11 * 300)
# while True:
#     sheet = Image.new('RGBA', (width, height))
#     # 50px offset to start
#     x = 50
#     y = 50
#     break