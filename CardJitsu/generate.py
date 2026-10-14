from PIL import Image
import json

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
        1:      Image.open('./files/Set/1.png'),
        2:      Image.open('./files/Set/2.png'),
        3:      Image.open('./files/Set/3.png'),
        4:      Image.open('./files/Set/4.png'),
        5:      Image.open('./files/Set/5.png'),
        6:      Image.open('./files/Set/6.png'),
        7:      Image.open('./files/Set/7.png'),
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
        'block': {}
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
    pass
    # if 'cannot be played next round' in description:
    #     print('Block')
    # elif 'discard one' in description:
    #     print('Discard One')
    # elif 'cards become' in description:
    #     print('Convert')
    # elif '' in description:
    #     print('Discard All')
    # elif '' in description:
    #     print('Discard Element')
    # elif '-2' in description:
    #     print('Modify -2')
    # elif '+2' in description:
    #     print('Modify +2')
    # elif 'lower values win' in description:
    #     print('Modify reverse')
    # else:
    #     print(description)

with open('scrape/new_cards.json', 'r') as file:
    cards_json = json.load(file)

for card_num, data in cards_json.items():

    if not data.get('description'): continue

    if card_num == "349": print(data)

    # Opening the card image
    image = Image.new(mode='RGBA', size=(750, 1050))
    card_image = Image.open(f'./generated_cards/{card_num}.png')
    card_image = card_image.resize((850, 850))
    image.paste(card_image, (-60, -20))

    # Drawing the bottom 3 colors based on the element
    color_background = color_key['tri_color'][data['element']].copy()
    image.paste(color_background, mask=color_background)

    if data.get('description'):
        ability_image = getAbilityImage(data['description'])

    # Top Left Color
    color_top_left = color_key['top_left'][data['color']].copy()
    image.paste(color_top_left, mask=color_top_left)

    color_top_left = color_key['top_left'][data['color']].copy()
