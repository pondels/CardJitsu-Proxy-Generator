from PIL import Image
import json

sets = {
    # 1: 0,
    2: 1,
    # 3: 0,
    # 4: 0,
    5: 5,
    # 6: 0,
    # 7: 0,
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

def getColor(description): pass

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

with open('scrape/new_cards.json', 'r') as file:
    cards_json = json.load(file)

for card_num, data in cards_json.items():

    if data['set_id'] != '6' or not data.get('description'): continue

    # Opening the card image
    image = Image.new(mode='RGBA', size=(750, 1050))
    card_image = Image.open(f'./generated_cards/{card_num}.png')
    card_image = card_image.resize((850, 850))
    image.paste(card_image, (-50, -100))

    # Drawing the bottom 3 colors based on the element
    color_background = color_key['tri_color'][data['element']].copy()
    image.paste(color_background, mask=color_background)

    # Top Left Color
    color_top_left = color_key['top_left'][data['color']].copy()
    image.paste(color_top_left, mask=color_top_left)

    # Drawing the Set Penguin
    penguin_set = color_key['penguin_set'][data['set_id']].copy()
    image.paste(penguin_set, mask=penguin_set)

    # {
    # 'label': 'FLOORING UPGRADE',
    # flavor_text': '"I\'m rollin\' out some burgundy/a> style," says the interior decorator. "I\'ve got some brand new igloo vibe picked out – a totally awesome empurpled cabin/a> of chic. It\'s gonna be a partay!"'}

    # TODO X/Y Set number and total
    # TODO Flavor text black text

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

    # TODO Card title to mask if not snow, otherwise, black text to original
    if data['element'] == 's': pass
    else: pass

    if data.get('description'):
        # Drawing Black Ability Background
        ability_bg = color_key['basic']['power_bg'].copy()
        image.paste(ability_bg, mask=ability_bg)

        # TODO Adding white ability text


        # Ability white bar to mask
        ability_outline = color_key['basic']['power_outline'].copy()
        white_mask.paste(ability_outline, mask=ability_outline)

        # TODO Cut mask out from main image if power card, otherwise paste it on
        mask_data = white_mask.load()
        for x in range(white_mask.width):
            for y in range(white_mask.height):
                # We found pixel data, nuke it from the original
                if mask_data[x, y][0] != 0 or mask_data[x, y][1] != 0 or mask_data[x, y][2] != 0:
                    image.putpixel((x, y), (0, 0, 0, 0))

        # Adding ability image in top right
        ability_image = getAbilityImage(data['description'])
        image.paste(ability_image, mask=ability_image)

    else:
        # Pasting the mask on
        image.paste(white_mask, mask=white_mask)

    # Adding Symbol and Power images
    element_mask = color_key['symbols']['symbol'][data['element']].copy()
    image.paste(element_mask, mask=element_mask)
    power_mask = color_key['numbers']['number'][data['value']].copy()
    image.paste(power_mask, mask=power_mask)

    image.show()