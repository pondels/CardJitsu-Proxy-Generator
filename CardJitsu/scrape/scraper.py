from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import csv
import json


# opening up connection, grabbing the page

with open('cards.json', 'r') as cards:
    card_json = {data['card_id']: data for data in json.loads(cards.read().__str__())}

paths = [
    'cards-1-4.html',
    'cards-5-8.html',
    'power_cards.html'
]

for path in paths:
    with open(path, 'r') as file:
        html = file.read()

        # html parsing
        page_soup = soup(html, "html.parser")

        for i in range(805):
            # Grabs each td description
            containers = page_soup.find("tr", id=f'card_{i}')
            if containers:
                # Grabbing the card flavor text at the bottom
                flavor_text = containers.__str__().split('<td>')[-1].split('</td>')[0]

                # Filtering out the nonsense elements within the text
                flavor_text = ''.join([c if i % 2 == 0 else c.split('>')[1] for i, c in enumerate(flavor_text.split('<'))])
                if not card_json[str(i)].get('flavor_text'):
                    card_json[str(i)]['flavor_text'] = flavor_text.strip()

with open('new_cards.json', 'w') as file:
    json.dump(card_json, file)

# {"flavor_text": "Sweeping the sands of liberty. Only the truest of sand castles may be thwarted by the mightiest of penguins.", "card_id":"801","set_id":"8","power_id":"0","element":"f","name":"Mobile Fire 1","label":"Mobile Fire 1","prompt":"Mobile Fire 1","color":"r","value":"6","asset":"","description":"","is_active":"1"},
#     {"flavor_text": "A fortress mighty enough for a king. A traveling agent ready for deployment.", "card_id":"802","set_id":"8","power_id":"0","element":"s","name":"Mobile Snow 1","label":"Mobile Snow 1","prompt":"Mobile Snow 1","color":"g","value":"7","asset":"","description":"","is_active":"1"},
#     {"flavor_text": "Nobody kills the messenger.", "card_id":"803","set_id":"8","power_id":"0","element":"w","name":"Mobile Water 1","label":"Mobile Water 1","prompt":"Mobile Water 1","color":"b","value":"8","asset":"","description":"","is_active":"1"},
#     {"flavor_text": "There is no war in Ba Sing Se.", "card_id":"804","set_id":"8","power_id":"2","element":"f","name":"Mobile Fire Power Card 1","label":"Mobile Fire Power Card 1","prompt":"Mobile Fire Power Card 1","color":"p","value":"11","asset":"","description":"When this is scored, your card gets +2 for the next round","is_active":"1"}

# allElements = []

# for i in containers:
#     # if "Card-Jitsu" in i["href"] or 'card_image' in i['href']:
#     allElements.append(i["href"])

# with open('allCards.csv', 'r+') as file:
#     writer = csv.writer(file)
#     for i in allElements:
#         writer.writerow([i])