import csv
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