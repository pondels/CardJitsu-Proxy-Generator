from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import csv
import json

def createCardDict():

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
                    flavor_text = ''.join([c.split('<')[0] for c in flavor_text.split(">")])
                    if not card_json[str(i)].get('flavor_text'):
                        card_json[str(i)]['flavor_text'] = flavor_text.strip()

    with open('new_cards.json', 'w') as file:
        json.dump(card_json, file)

def createSWFDict():
    swf_dict = {}
    with open('./swf.html', 'r') as file:
        html = file.read()

        # html parsing
        page_soup = soup(html, "html.parser")

        # Grabs each swf path
        containers = page_soup.find_all("a", {'class': 'internal'})
        for container in containers:
            container = str(container)
            card_num = container.split('>')[1].split('<')[0]
            card_link = container.split('href="')[1].split('"')[0]
            swf_dict[card_num] = f'https://archives.clubpenguinwiki.info{card_link}'

    print(swf_dict)
    with open('swf_links.json', 'w+') as file:
        json.dump(swf_dict, file)

createCardDict()
# createSWFDict()