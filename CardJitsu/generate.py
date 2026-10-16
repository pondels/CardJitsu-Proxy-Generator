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
    '8': 4,
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
        '8':    Image.open('./files/Set/7.png'),
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
            if mask_data[x, y][0] > 50 or mask_data[x, y][1] > 50 or mask_data[x, y][2] > 50:
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

def regularCardBuild(data: dict, set_num: int, card_num: str):
    # Opening the card image
    image = Image.new(mode='RGBA', size=(750, 1050))

    # With the data changes, it is now misaligned to downloaded content
    # This realigns that information
    if not data.get('png_override'):
        print('CARD FAILED THE VIBE CHECK!')
        return

    card_image = Image.open(f'./downloaded_cards/{data['png_override']}.png')
    card_image = card_image.resize((850, 850))
    y_offset = offset_lookup[set_num].get(card_num, 0)
    image.paste(card_image, (-50, -100+y_offset))

    # Drawing the bottom 3 colors based on the element
    color_background = color_key['tri_color'][data['element']].copy()
    image.paste(color_background, mask=color_background)

    # Top Left Color
    color_top_left = color_key['top_left'][data['color']].copy()
    image.paste(color_top_left, mask=color_top_left)


    # Symbol and number shadow to mask
    white_mask = Image.new('RGBA', (750, 1050))

    # Drawing the Set Penguin
    if data.get('rare'):
        penguin_set = color_key['penguin_set']['rare'].copy()
    else:
        penguin_set = color_key['penguin_set'][data['set_id']].copy()
    
    if data.get('rare') and data.get('description'):
        white_mask.paste(penguin_set, mask=penguin_set)
    else:
        image.paste(penguin_set, mask=penguin_set)

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

    # This removes any leading 0's
    card_id = str(int(card_num))

    if data['element'] == 's':
        reg_text_drawer.text((375-text_radius, 720), data['label'].upper(), font=title_font, fill=(0, 0, 0))
        reg_text_drawer.text((50, 790), flavor_text, font=flavor_font, fill=(0, 0, 0))
        reg_text_drawer.text((600, 960), f'{card_id}/{set_count[data["set_id"]]}', font=flavor_font, fill=(0, 0, 0))
    else:
        mask_text_drawer.text((375-text_radius, 720), data['label'].upper(), font=title_font, fill=(255, 255, 255))
        reg_text_drawer.text((50, 790), flavor_text, font=flavor_font, fill=(255, 255, 255))
        reg_text_drawer.text((600, 960), f'{card_id}/{set_count[data["set_id"]]}', font=flavor_font, fill=(255, 255, 255))

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

    # TODO See what the cards would look like borderless.
    # Just stretch the cards and offset them. idk

    # Saving the image to our generated cards
    image.save(f'./generated_cards/set{set_num}/{card_num}.png')

def customizePenguin():
    pass

with open('scrape/new_cards.json', 'r') as file:
    cards_json = json.load(file)

# title_font  = ImageFont.truetype('./fonts/candombe.otf', 75)
# flavor_font = ImageFont.truetype('./fonts/candombe.otf', 37)
title_font  = ImageFont.truetype('./fonts/boogaloo.ttf', 44)
flavor_font = ImageFont.truetype('./fonts/boogaloo.ttf', 30)

# TODO When done generating the cards, make sure they line up with the ones on the website

# NOTE Images that use the wrong cards for whatever reason
# 668 is completely busted
# 723 is just the wrong image
# Puffle partying is not accounted for
# Puffle science is not accounted for

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
    '1': {
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
    },
    '2': {
        '4': med_down,
    },
    '3': {
        '2': low_down,
        '6': low_down,
        '7': low_down,
        '11': low_down,
        '25': low_down,
        '27': low_down,
        '28': low_down,
        '30': low_down,
        '31': med_down,
        '32': low_down,
        '35': low_down,
        '45': low_down,
        '46': low_down,
        '53': med_up,
        '54': med_up,
        '55': med_up,
        '56': low_down,
        '57': med_down,
    },
    '4': {
        '2': low_down,
        '7': low_down,
        '8': low_down,
        '12': low_down,
        '17': med_down,
        '19': low_down,
        '21': low_down,
        '22': low_down,
        '26': med_down,
        '28': low_down,
        '33': low_down,
        '37': low_down,
        '39': low_down,
        '42': low_down,
        '60': low_down,
    },
    '5': {
        '4': low_down,
        '19': low_down,
        '23': low_down,
        '24': low_down,
        '26': low_down,
        '27': low_down,
    },
    '6': {
        '8': low_down,
        '11': med_down,
        '20': med_down,
        '23': med_down,
        '25': med_down,
        '27': med_down,
        '28': med_down,
        '35': low_down,
        '37': med_down,
        '38': low_down,
        '42': low_down,
        '44': low_down,
        '48': low_down,
        '53': low_down,
        '55': low_down,
        '56': low_down,
        '61': low_down,
        '67': low_down,
        '70': low_down,
        '74': low_down,
        '75': low_down,
        '77': low_down,
        '79': low_down,
        '81': med_up,
        '87': low_down,
        '88': low_down,
        '92': low_down,
        '94': low_down,
        '95': low_down,
    },
    '7': {
        '2': low_down,
        '3': low_down,
        '5': low_down,
        '7': med_down,
        '15': low_down,
        '17': low_down,
        '18': low_down,
        '20': med_down,
        '22': low_down,
        '34': low_down,
        '38': low_down,
        '42': low_down,
        '44': low_down,
        '48': low_down,
        '49': low_down,
        '53': low_down,
        '55': low_down,
        '57': low_down,
        '58': low_down,
        '61': low_down,
        '62': low_down,
        '64': low_down,
        '68': low_down,
        '73': low_down,
        '74': low_down,
        '81': low_down,
        '82': med_down,
        '85': low_down,
        '86': low_down,
        '87': low_down,
        '88': low_down,
        '90': low_down,
        '91': low_down,
        '107': low_down,
        '115': med_down,
        '117': low_down,
        '119': tiny_down,
        '120': tiny_down,
        '124': low_up,
        '136': med_down,
        '139': low_up,
        '140': low_down,
        '143': low_up,
        '146': low_up,
    },
    '8': {},
}

for set_num, card_list in cards_json.items():
    for card_num, data in card_list.items():
        
        # Custom penguin card
        if data['label'].lower() == 'customize your penguin':
            customizePenguin()
            continue

        if set_num != '8': continue

        # Creating normal card
        regularCardBuild(data, set_num, card_num)

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