import csv
import re
import urllib.request
from bs4 import BeautifulSoup
from time import sleep

NEKRETNINE_URL = 'https://www.nekretnine.rs'
NEKRETNINE_FIRST_PART_OF_URL = 'https://www.nekretnine.rs/stambeni-objekti/'
NEKRETNINE_SECOND_PART_OF_URL = '/izdavanje-prodaja/prodaja/lista/po-stranici/10/'


def get_data(max_pages, type_of_estate):
    page = 1
    real_estate_type = 'house' if type_of_estate == 'kuce' else 'apartment'
    url = 'https://www.nekretnine.rs/stambeni-objekti/' + type_of_estate + '/lista/po-stranici/20/stranica/' + str(page)
    while page <= max_pages:
        source = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(source, 'html.parser')
        for link in soup.find_all('div', class_='col-8 col-md-9 offer-body py-2 px-3'):
            href = link.find('a').get('href')
            crawl_advert(NEKRETNINE_URL + href)
            break
        page += 1

        next_page = soup.find('link', rel='next')
        sleep(1)


def crawl_advert(href):
    url = href
    source = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(source, 'html.parser')
    crawled_information = {}
    print('Here')
    print(href)

    location = soup.find('h3', class_='stickyBox__Location').get_text().strip()

    res = {}
    # Every second one is not good, so we skip it. TO DO: Check if the text could be retrieved better
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

        res[property_name] = property_value

        cnt += 1

    for tag in soup.find('div', class_='property__amenities').find_all('li'):
        splitted_text = tag.getText().split(':')
        # remove non numeric characters
        property_name = re.sub('[^A-Za-z0-9 ]+', '', splitted_text[0])
        # remove all spaces but one
        property_name = ' '.join(property_name.split())

        property_value = re.sub('[^A-Za-z0-9 ]+', '', splitted_text[1])
        property_value = ' '.join(property_value.split())

        res[property_name] = property_value


    sptxt = soup.find('div', class_='property__main-details').getText().strip()
    re.sub(r'\n\s*\n', '\n\n', sptxt)

    crawled_information['location'] = location
    print(location)
    insert_crawled_data_into_json(crawled_information)

    return


def insert_crawled_data_into_json(crawled_information):
    print(crawled_information)
    with open("sample.csv", "w", encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(crawled_information)


list_of_estate_types = ['stanovi', 'kuce']
for estate_type in list_of_estate_types:
    get_data(1, estate_type)
