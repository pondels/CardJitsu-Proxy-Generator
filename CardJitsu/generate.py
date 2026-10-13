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

with open('scrape/new_cards.json', 'r') as file:
    cards_json = json.load(file)

for card_num, data in cards_json.items():

    # Opening the card image
    # NOTE This is a template for now. Get it setup with the actual image later
    image = Image.open('./files/CardImages/template.png')

    # Drawing the bottom 3 colors based on the element
    color_background = color_key['tri_color'][data['element']].copy()
    image.paste(color_background, mask=color_background)

    # TODO Drawing Card Name on inverted mask
    # Getting the bottom image and setting the 3 colors
    {
        'set_id': '1',
        'power_id': '0',
        'element': 'f',
        'name': 'CART SURFER',
        'label': 'CART SURFER',
        'prompt': 'CART SURFER',
        'color': 'b',
        'value': '3',
        'asset': '',
        'description': '',
        'is_active': '1',
        'flavor_text': '"Dude, I\'m totally gonna get like 500 coins this time," says a penguin ripping down the track. "I run through the cave and get sweet air with my 360s and backflips."'
    }

    # TODO Top Left Color
    color_top_left = color_key['top_left'][data['color']].copy()
    image.paste(color_top_left, mask=color_top_left)

    # TODO Top Left Symbol Background on inverted mask
    # TODO Top Left Number Background on inverted mask
    # TODO Card Outline on inverted mask

    # Check if the card is a power card
    # 8a. Power Card Text
    # 8b. Power Card Ability on inverted mask
    # 8c. Ability Text
    # 8d. Ability Symbol
    # Power Number
    # Flavor Text
    # Top Left Symbol
    # Set Symbol in bottom Right
    # X/Y Card Number / Total Cards in Set
    # Apply the negative mask
    image.show()
    break
