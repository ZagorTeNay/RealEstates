import re
import urllib.request
from time import sleep
import random
import pandas as pd
from bs4 import BeautifulSoup

NEKRETNINE_URL = 'https://www.nekretnine.rs'
NEKRETNINE_FIRST_PART_OF_URL = 'https://www.nekretnine.rs/stambeni-objekti/'
NEKRETNINE_SECOND_PART_OF_URL = '/izdavanje-prodaja/prodaja/lista/po-stranici/10/'


def get_data(type_of_estate):
    page = 1
    url = 'https://www.nekretnine.rs/stambeni-objekti/' + type_of_estate + '/lista/po-stranici/20/stranica/' + str(page)
    while True:
        source = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(source, 'html.parser')

        if type_of_estate == 'stanovi':
            estate_type = 'apartment'
        else:
            estate_type = 'house'

        for link in soup.find_all('div', class_='col-8 col-md-9 offer-body py-2 px-3'):
            href = link.find('a').get('href')
            crawl_advert(NEKRETNINE_URL + href, estate_type)
        page += 1

        next_page = soup.find('link', rel='next')
        if not next_page:
            break
        sleep(random.choice([0.5, 3])
)


def crawl_advert(href, type_of_estate):
    url = href
    source = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(source, 'html.parser')

    crawled_information = {'href': href, 'type': type_of_estate}

    location = soup.find('h3', class_='stickyBox__Location').get_text().strip()
    crawled_information['location'] = location

    price = soup.find('h4', class_='stickyBox__price').get_text().strip()
    crawled_information['price'] = price

    # Every second one is not good, so we skip it. TODO: Check if the text could be retrieved better
    cnt = 1
    for tag in soup.find('div', class_='property__main-details').find_all('span'):
        if cnt % 2 == 0:
            cnt += 1
            continue

        splitted_text = tag.getText().split(':')
        # remove non numeric characters
        property_name = re.sub('[^A-Za-z0-9 ]+', '', splitted_text[0])
        # remove all spaces but one
        property_name = ' '.join(property_name.split())

        property_value = re.sub('[^A-Za-z0-9 ]+', '', splitted_text[1])
        property_value = ' '.join(property_value.split())

        crawled_information[property_name] = property_value

        cnt += 1

    for tag in soup.find('div', class_='property__amenities').find_all('li'):
        splitted_text = tag.getText().split(':')
        # remove non numeric characters
        property_name = re.sub('[^A-Za-z0-9 ]+', '', splitted_text[0])
        # remove all spaces but one
        property_name = ' '.join(property_name.split())

        property_value = re.sub('[^A-Za-z0-9 ]+', '', splitted_text[1])
        property_value = ' '.join(property_value.split())

        crawled_information[property_name] = property_value

    insert_crawled_data_into_json(crawled_information)

    return


def insert_crawled_data_into_json(crawled_information):
    needed_information = trim_all_informations_into_needed_ones(crawled_information)
    df = pd.DataFrame([needed_information])
    df.to_csv('out.csv', mode='a', encoding='utf-8')

def trim_all_informations_into_needed_ones(crawled_information):
    needed_info = {}

    needed_info['transaction'] = crawled_information['Transakcija'] if 'Transakcija' in crawled_information else None
    needed_info['city_part'] = crawled_information['Pozicija'] if 'Pozicija' in crawled_information else None
    needed_info['location'] = crawled_information['location'] if 'location' in crawled_information else None
    needed_info['price'] = crawled_information['price'] if 'price' in crawled_information else None
    needed_info['square_footage'] = crawled_information['Kvadratura'] if 'Kvadratura' in crawled_information else None

    needed_info['heating'] = crawled_information['Grejanje'] if 'Grejanje' in crawled_information else None
    needed_info['floor'] = crawled_information['Spratnost'] if 'Spratnost' in crawled_information else None
    needed_info['registration'] = crawled_information['Uknjiženo'] if 'Uknjiženo' in crawled_information else None

    needed_info['num_of_rooms'] = crawled_information['Ukupan broj soba'] if 'Ukupan broj soba' in crawled_information else None
    needed_info['num_of_bathrooms'] = crawled_information['Broj kupatila'] if 'Broj kupatila' in crawled_information else None
    needed_info['year_of_construction'] = crawled_information['Godina izgradnje'] if 'Godina izgradnje' in crawled_information else None

    needed_info['area'] = crawled_information['Godina izgradnje'] if 'Godina izgradnje' in crawled_information else None
    needed_info['parking'] = crawled_information['Parking'] if 'Parking' in crawled_information else None
    needed_info['area'] = crawled_information['Godina izgradnje'] if 'Godina izgradnje' in crawled_information else None
    needed_info['property_condition'] = crawled_information['Stanje nekretnine'] if 'Stanje nekretnine' in crawled_information else None
    needed_info['href'] = crawled_information['href'] if 'href' in crawled_information else None
    needed_info['type'] = crawled_information['type'] if 'type' in crawled_information else None
    return needed_info


list_of_estate_types = ['stanovi', 'kuce']
for estate_type in list_of_estate_types:
    get_data(estate_type)
