from PIL import Image, ImageDraw, ImageFont
import json
import os
import numpy as np

set_count = {
    '1': 110,
    '2': 30,
    '3': 68,
    '4': 68,
    '5': 28,
    '6': 110,
    '7': 150,
    '8': 4,
}

# Setting up the color key
def convertImageColor(
    image: Image,
    from_color: tuple[int, int, int],
    to_color: tuple[int, int, int]
) -> Image:
    data = np.array(image)
    red, green, blue, _ = data.T
    white_areas = (red == from_color[0]) & (blue == from_color[2]) & (green == from_color[1])
    data[..., :-1][white_areas.T] = to_color
    return Image.fromarray(data)

def setTriColor(top, mid, bot, card_type) -> Image:
    image = Image.open(f'./files/Basic/bottom_background_{card_type}.png')
    image = convertImageColor(image, (238, 238, 238), top)
    image = convertImageColor(image, (196, 196, 196), mid)
    image = convertImageColor(image, (132, 132, 132), bot)
    return image

def setTopLeft(k1) -> Image:
    image = Image.open('./files/Basic/top_left_background.png')
    image = convertImageColor(image, (53, 53, 53), k1)
    return image

image_key = {
    'tri_color': {
        'regular': {
            'f': setTriColor((230, 130, 55),  (229,  90,  59), (219,  42,  50), 'regular'),
            's': setTriColor((244, 244, 246), (230, 233, 234), (217, 220, 221), 'regular'),
            'w': setTriColor(( 67, 127, 182), ( 65, 102, 165), ( 55,  69, 128), 'regular'),
        },
        'custom': {
            'f': setTriColor((230, 130,  55), (229,  90,  59), (219,  42,  50), 'custom'),
            's': setTriColor((244, 244, 246), (230, 233, 234), (217, 220, 221), 'custom'),
            'w': setTriColor(( 67, 127, 182), ( 65, 102, 165), ( 55,  69, 128), 'custom'),
        },
    },
    'top_left': {
        'r': setTopLeft((227, 60, 37)),
        'o': setTopLeft((248, 149, 43)),
        'y': setTopLeft((251, 234, 44)),
        'g': setTopLeft((98, 184, 71)),
        'b': setTopLeft((16, 72, 160)),
        'p': setTopLeft((163, 153, 202)),
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
    'basic': {
        'power_outline':        Image.open('./files/Basic/power_card_outline.png'),
        'card_outline_regular': Image.open('./files/Basic/card_outline_regular.png'),
        'card_outline_custom':  Image.open('./files/Basic/card_outline_custom.png'),
        'power_bg':             Image.open('./files/Basic/power_card_text_background.png'),
    }
}

class CardCreator():

    COLOR_LOOKUP = {
        'maroon':       (128,  33,  75),
        'green':        (  0, 153,   0),
        'dark_green':   (  0, 102,   0),
        'lime_green':   (138, 227,   2),
        'brown':        (153, 102,   0),
        'arctic_white': (240, 240, 216),
        'peach':        (255, 102, 102),
        'dark_purple':  (102,   0, 153),
        'yellow':       (255, 204,   0),
        'pink':         (255,  51, 153),
        'black':        ( 51,  51,  51),
        'orange':       (255, 102,   0),
        'light_blue':   (  0, 153, 204),
        'red':          (204,   0,   0),
        'aqua':         (  2, 167, 151),
        'sensei_gray':  (142, 154, 158),
        'dot_lavender': (195, 120, 208),
        'default_blue': ( 46,  71, 170),
        'dark_black':   (  0,   0,   0),
        'lavender':     (174, 159, 200),
        'blue':         (  0,  51, 102),
    }

    TITLE_FONT = ImageFont.truetype('./fonts/boogaloo.ttf', 44)
    CUSTOM_TITLE_FONT = ImageFont.truetype('./fonts/boogaloo.ttf', 35)
    FLAVOR_FONT = ImageFont.truetype('./fonts/boogaloo.ttf', 30)
    # CardCreator.TITLE_FONT  = ImageFont.truetype('./fonts/candombe.otf', 75)
    # CardCreator.FLAVOR_FONT = ImageFont.truetype('./fonts/candombe.otf', 37)
    TINY_DOWN = 25
    LOW_DOWN = 50
    MED_DOWN = 100
    HIGH_DOWN = 150
    TINY_UP = -25
    LOW_UP = -50
    MED_UP = -100
    HIGH_UP = -150
    # Some cards need slight offsets. This is a generic template of those offsets
    OFFSET_LOOKUP = {
        '1': {
            '2': MED_DOWN,
            '4': LOW_DOWN,
            '7': LOW_DOWN,
            '13': LOW_DOWN,
            '62': LOW_DOWN,
            '64': LOW_DOWN,
            '71': MED_UP,
            '73': LOW_UP,
            '74': TINY_UP,
            '75': LOW_UP,
            '76': LOW_UP,
            '90': LOW_UP,
        },
        '2': {
            '4': MED_DOWN,
            '21': LOW_DOWN,
            '23': LOW_DOWN,
            '30': LOW_UP
        },
        '3': {
            '2': LOW_DOWN,
            '6': LOW_DOWN,
            '7': LOW_DOWN,
            '11': LOW_DOWN,
            '25': LOW_DOWN,
            '27': LOW_DOWN,
            '28': LOW_DOWN,
            '30': LOW_DOWN,
            '31': MED_DOWN,
            '32': LOW_DOWN,
            '35': LOW_DOWN,
            '45': LOW_DOWN,
            '46': LOW_DOWN,
            '53': MED_UP,
            '54': MED_UP,
            '55': MED_UP,
            '56': LOW_DOWN,
            '57': MED_DOWN,
        },
        '4': {
            '2': LOW_DOWN,
            '7': LOW_DOWN,
            '8': LOW_DOWN,
            '12': LOW_DOWN,
            '17': MED_DOWN,
            '19': LOW_DOWN,
            '21': LOW_DOWN,
            '22': LOW_DOWN,
            '26': MED_DOWN,
            '28': LOW_DOWN,
            '33': LOW_DOWN,
            '37': LOW_DOWN,
            '39': LOW_DOWN,
            '42': LOW_DOWN,
            '60': LOW_DOWN,
        },
        '5': {
            '4': LOW_DOWN,
            '19': LOW_DOWN,
            '23': LOW_DOWN,
            '24': LOW_DOWN,
            '26': LOW_DOWN,
            '27': LOW_DOWN,
        },
        '6': {
            '8': LOW_DOWN,
            '11': MED_DOWN,
            '20': MED_DOWN,
            '23': MED_DOWN,
            '25': MED_DOWN,
            '27': MED_DOWN,
            '28': MED_DOWN,
            '35': LOW_DOWN,
            '37': MED_DOWN,
            '38': LOW_DOWN,
            '42': LOW_DOWN,
            '44': LOW_DOWN,
            '48': LOW_DOWN,
            '53': LOW_DOWN,
            '55': LOW_DOWN,
            '56': LOW_DOWN,
            '61': LOW_DOWN,
            '67': LOW_DOWN,
            '70': LOW_DOWN,
            '74': LOW_DOWN,
            '75': LOW_DOWN,
            '77': LOW_DOWN,
            '79': LOW_DOWN,
            '81': MED_UP,
            '87': LOW_DOWN,
            '88': LOW_DOWN,
            '92': LOW_DOWN,
            '94': LOW_DOWN,
            '95': LOW_DOWN,
        },
        '7': {
            '2': LOW_DOWN,
            '3': LOW_DOWN,
            '5': LOW_DOWN,
            '7': MED_DOWN,
            '15': LOW_DOWN,
            '17': LOW_DOWN,
            '18': LOW_DOWN,
            '20': MED_DOWN,
            '22': LOW_DOWN,
            '34': LOW_DOWN,
            '38': LOW_DOWN,
            '42': LOW_DOWN,
            '44': LOW_DOWN,
            '48': LOW_DOWN,
            '49': LOW_DOWN,
            '53': LOW_DOWN,
            '55': LOW_DOWN,
            '57': LOW_DOWN,
            '58': LOW_DOWN,
            '61': LOW_DOWN,
            '62': LOW_DOWN,
            '64': LOW_DOWN,
            '68': LOW_DOWN,
            '73': LOW_DOWN,
            '74': LOW_DOWN,
            '81': LOW_DOWN,
            '82': MED_DOWN,
            '85': LOW_DOWN,
            '86': LOW_DOWN,
            '87': LOW_DOWN,
            '88': LOW_DOWN,
            '90': LOW_DOWN,
            '91': LOW_DOWN,
            '107': LOW_DOWN,
            '115': MED_DOWN,
            '117': LOW_DOWN,
            '119': TINY_DOWN,
            '120': TINY_DOWN,
            '124': LOW_UP,
            '136': MED_DOWN,
            '139': LOW_UP,
            '140': LOW_DOWN,
            '143': LOW_UP,
            '146': LOW_UP,
        },
        '8': {},
    }

    @staticmethod
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

    @staticmethod
    def mapPowerCard(image: Image, white_mask: Image, data: dict):
        # Drawing Black Ability Background
        ability_bg = image_key['basic']['power_bg'].copy()
        image.paste(ability_bg, mask=ability_bg)

        # Ability white bar to mask
        ability_outline = image_key['basic']['power_outline'].copy()
        white_mask.paste(ability_outline, mask=ability_outline)

        mask_data = white_mask.load()
        for x in range(white_mask.width):
            for y in range(white_mask.height):
                # We found pixel data, nuke it from the original
                if mask_data[x, y][0] > 50 or mask_data[x, y][1] > 50 or mask_data[x, y][2] > 50:
                    image.putpixel((x, y), (0, 0, 0, 0))

        # Adding ability image in top right
        ability_image = CardCreator.getAbilityImage(data['description'])
        image.paste(ability_image, mask=ability_image)

    @staticmethod
    def getFlavorText(data: dict):
        final_text = ['']
        for word in data['flavor_text'].split(' '):
            if CardCreator.FLAVOR_FONT.getlength(final_text[-1] + word) > 650:
                final_text.append('')

            final_text[-1] += f'{word} '

        return '\n'.join(final_text)

    @staticmethod
    def maxAlpha(image: Image):
        image_data = image.load()
        for x in range(image.width):
            for y in range(image.height):
                # We found pixel data, nuke it from the original
                pixel = image_data[x, y]
                if pixel[3] > 0:
                    image.putpixel((x, y), (pixel[0], pixel[1], pixel[2], 255))

    @staticmethod
    def saveImage(image: Image, set_num: int, card_num: int):
        # Saving the image to our generated cards
        if not os.path.exists('./generated_cards'):
            os.mkdir('./generated_cards')

        if not os.path.exists(f'./generated_cards/set{set_num}'):
            os.mkdir(f'./generated_cards/set{set_num}')

        image.save(f'./generated_cards/set{set_num}/{card_num}.png')

    @staticmethod
    def getBaseImage(): return Image.new(mode='RGBA', size=(750, 1050))

    @staticmethod
    def regularCardBuild(data: dict, set_num: int, card_num: str):
        # Opening the card image
        image = CardCreator.getBaseImage()

        # With the data changes, it is now misaligned to downloaded content
        # This realigns that information
        if not data.get('png_override'):
            print('CARD FAILED THE VIBE CHECK!')
            return

        card_image = Image.open(f'./downloaded_cards/{data['png_override']}.png')
        # We don't want to scale the image
        if data.get('scale_image') is None or data['scale_image'] == True:
            card_image = card_image.resize((850, 850))

        offset = (0, 0)
        if data.get('offset_image') is None or data['offset_image']:
            y_offset = CardCreator.OFFSET_LOOKUP[set_num].get(card_num, 0)
            offset = (-50, -100+y_offset)

        image.paste(card_image, offset)

        # If the card has a fix to it, paste it on
        card_fix_path = f'./fixed_cards/set{set_num}/{card_num}.png'
        if os.path.exists(card_fix_path):
            card_fix = Image.open(card_fix_path)
            # Setting the transparency of each used pixel to 255
            CardCreator.maxAlpha(card_fix)
            image.paste(card_fix, mask=card_fix)

        # Drawing the bottom 3 colors based on the element
        color_background = image_key['tri_color']['regular'][data['element']].copy()
        image.paste(color_background, mask=color_background)

        # Top Left Color
        color_top_left = image_key['top_left'][data['color']].copy()
        image.paste(color_top_left, mask=color_top_left)

        # Symbol and number shadow to mask
        white_mask = Image.new('RGBA', (750, 1050))

        # Drawing the Set Penguin
        if data.get('rare'):
            penguin_set = image_key['penguin_set']['rare'].copy()
        else:
            penguin_set = image_key['penguin_set'][set_num].copy()
        
        if data.get('rare') and data.get('description'):
            white_mask.paste(penguin_set, mask=penguin_set)
        else:
            image.paste(penguin_set, mask=penguin_set)

        # Adding card frame to mask
        card_outline = image_key['basic']['card_outline_regular'].copy()
        white_mask.paste(card_outline, mask=card_outline)

        # Adding element and power background to mask
        element_mask = image_key['symbols']['mask'][data['element']].copy()
        white_mask.paste(element_mask, mask=element_mask)
        power_mask = image_key['numbers']['mask'][data['value']].copy()
        white_mask.paste(power_mask, mask=power_mask)

        # Card title to mask if not snow, otherwise, black text to original
        reg_text_drawer = ImageDraw.Draw(image)
        mask_text_drawer = ImageDraw.Draw(white_mask)
        text_radius = CardCreator.TITLE_FONT.getlength(data['label'].upper()) // 2

        flavor_text = CardCreator.getFlavorText(data)

        # This removes any leading 0's
        card_id = str(int(card_num))

        if data['element'] == 's':
            reg_text_drawer.text((375-text_radius, 720), data['label'].upper(), font=CardCreator.TITLE_FONT, fill=(0, 0, 0))
            reg_text_drawer.text((50, 790), flavor_text, font=CardCreator.FLAVOR_FONT, fill=(0, 0, 0))
            reg_text_drawer.text((600, 960), f'{card_id}/{set_count[set_num]}', font=CardCreator.FLAVOR_FONT, fill=(0, 0, 0))
        else:
            mask_text_drawer.text((375-text_radius, 720), data['label'].upper(), font=CardCreator.TITLE_FONT, fill=(255, 255, 255))
            reg_text_drawer.text((50, 790), flavor_text, font=CardCreator.FLAVOR_FONT, fill=(255, 255, 255))
            reg_text_drawer.text((600, 960), f'{card_id}/{set_count[set_num]}', font=CardCreator.FLAVOR_FONT, fill=(255, 255, 255))

        description = data.get('description').upper()
        if description:
            if data['element'] == 's':
                reg_text_drawer.text((560, 925), 'POWER CARD', font=CardCreator.FLAVOR_FONT, fill=(0, 0, 0))
            else:
                mask_text_drawer.text((560, 925), 'POWER CARD', font=CardCreator.FLAVOR_FONT, fill=(255, 255, 255))

            CardCreator.mapPowerCard(image, white_mask, data)
            desc_split = description.split(', ')
            top_radius = CardCreator.FLAVOR_FONT.getlength(f'{desc_split[0]},') // 2
            bot_radius = CardCreator.FLAVOR_FONT.getlength(desc_split[1]) // 2
            reg_text_drawer.text((375-top_radius, 610), f'{desc_split[0]},', font=CardCreator.FLAVOR_FONT, fill=(255, 255, 255))
            reg_text_drawer.text((375-bot_radius, 645), desc_split[1],       font=CardCreator.FLAVOR_FONT, fill=(255, 255, 255))
        else:
            # Pasting the mask on
            image.paste(white_mask, mask=white_mask)

        # Adding Symbol and Power images
        element_mask = image_key['symbols']['symbol'][data['element']].copy()
        image.paste(element_mask, mask=element_mask)
        power_mask = image_key['numbers']['number'][data['value']].copy()
        image.paste(power_mask, mask=power_mask)

        # TODO See what the cards would look like borderless.
        # Just stretch the cards and offset them. idk

        # Saving the image to our generated cards
        if not os.path.exists('./generated_cards'):
            os.mkdir('./generated_cards')

        if not os.path.exists(f'./generated_cards/set{set_num}'):
            os.mkdir(f'./generated_cards/set{set_num}')

        image.save(f'./generated_cards/set{set_num}/{card_num}.png')

    @staticmethod
    def customizePenguin(data: dict, set_num: int, card_num: str):

        # Opening the card image
        image = CardCreator.getBaseImage()

        if not data.get('png_override') or not data.get('penguin_color'):
            print('CARD FAILED THE VIBE CHECK!')
            return

        card_image = Image.open(f'./downloaded_cards/{data['png_override']}.png')
        card_image = card_image.resize((900, 900))
        image.paste(card_image, (-20, 40))

        # TODO Pasting the penguin based on penguin color
        penguin_color = Image.open('./files/Basic/penguin_color_mask.png')
        penguin_color = convertImageColor(penguin_color, (178, 178, 178), CardCreator.COLOR_LOOKUP[data['penguin_color']])
        penguin_overlay = Image.open('./files/Basic/penguin_template.png')
        image.alpha_composite(penguin_color)
        image.alpha_composite(penguin_overlay)

        # Drawing the bottom 3 colors based on the element
        color_background = image_key['tri_color']['custom'][data['element']].copy()
        image.paste(color_background, mask=color_background)

        # Top Left Color
        color_top_left = image_key['top_left'][data['color']].copy()
        image.paste(color_top_left, mask=color_top_left)

        # Drawing the Set Penguin
        penguin_set = image_key['penguin_set'][set_num].copy()
        image.paste(penguin_set, mask=penguin_set)

        # Adding card frame to mask
        card_outline = image_key['basic']['card_outline_custom'].copy()
        image.paste(card_outline, mask=card_outline)

        # Adding element and power background to mask
        element_mask = image_key['symbols']['mask'][data['element']].copy()
        image.paste(element_mask, mask=element_mask)
        power_mask = image_key['numbers']['mask'][data['value']].copy()
        image.paste(power_mask, mask=power_mask)

        # Adding Symbol and Power images
        element_mask = image_key['symbols']['symbol'][data['element']].copy()
        image.paste(element_mask, mask=element_mask)
        power_mask = image_key['numbers']['number'][data['value']].copy()
        image.paste(power_mask, mask=power_mask)

        # Card title to mask if not snow, otherwise, black text to original
        reg_text_drawer = ImageDraw.Draw(image)
        text_radius = CardCreator.CUSTOM_TITLE_FONT.getlength(data['label'].upper()) // 2

        # This removes any leading 0's
        card_id = str(int(card_num))
        color_fill = (255, 255, 255) if data['element'] != 's' else (0, 0, 0)
        reg_text_drawer.text((375-text_radius, 920), data['label'].upper(), font=CardCreator.CUSTOM_TITLE_FONT, fill=color_fill)
        reg_text_drawer.text((600, 960), f'{card_id}/{set_count[set_num]}', font=CardCreator.FLAVOR_FONT, fill=color_fill)

        CardCreator.saveImage(image, set_num, card_num)

# Automating placing all the cards on sheets of paper.
class SheetGenerator():

    @staticmethod
    def generateSheets(card_images, width, height, sheet_name):
        # How much of a border do you want from the edge of the page
        card_width = card_images[0].width
        card_height = card_images[0].height
        cards_per_width  = width // card_width
        cards_per_height = height // card_height
        cards_per_page = cards_per_width * cards_per_height
        cards_width = (cards_per_width * card_width)
        cards_height = (cards_per_height * card_height)
        sheet_num = 0
        while card_images:
            cards_to_print = card_images[:cards_per_page]
            card_images = card_images[cards_per_page:]
            sheet = Image.new('RGBA', (cards_width, cards_height))
            card_index = 0
            for x_card in range(cards_per_width):
                for y_card in range(cards_per_height):
                    if card_index >= len(cards_to_print): break
                    x_offset = x_card*card_width
                    y_offset = y_card*card_height
                    sheet.paste(cards_to_print[card_index], (x_offset, y_offset))
                    card_index += 1

                if card_index >= len(cards_to_print): break

            if not os.path.exists(f'./paper_sheets/'):
                os.mkdir(f'./paper_sheets/')

            sheet.save(f'./paper_sheets/{sheet_name}_{sheet_num}.png')
            sheet_num += 1

    @staticmethod
    def mapCardsOnPaper():
        regular_cards = []
        power_cards = []
        for set_num, card_list in cards_json.items():
            for card_num, data in card_list.items():
                card_path = f'./generated_cards/set{set_num}/{card_num}.png'
                if not os.path.exists(card_path): continue
                image = Image.open(card_path)
                if data['description']: power_cards.append(image)
                else: regular_cards.append(image)

        # 300 pixels per inch
        # Cutting off the edges
        height = int(8.5 * 300)
        width  = int(11  * 300)
        SheetGenerator.generateSheets(regular_cards, width, height, 'reg')
        SheetGenerator.generateSheets(power_cards, width, height, 'pow')

with open('scrape/new_cards.json', 'r') as file:
    cards_json = json.load(file)

for set_num, card_list in cards_json.items():
    for card_num, data in card_list.items():

        # NOTE This is purely here to filter out any
        # unwanted cards for the sake of quick generation
        # Adjust this however you would like for testing generation
        continue

        # Custom penguin card
        if data['label'].lower() == 'customize your penguin':
            CardCreator.customizePenguin(data, set_num, card_num)
            continue

        # Creating normal card
        CardCreator.regularCardBuild(data, set_num, card_num)

# TODO speed up, slow poke
SheetGenerator.mapCardsOnPaper()