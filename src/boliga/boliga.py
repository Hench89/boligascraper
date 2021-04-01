import mechanicalsoup as ms
import pandas as pd
import numpy as np
from utils import date_clean, strip_digits
from boliga.dataclass import Housing, HousingList
import re

def get_listings(browser, zipcode, property_types = [1,2]):

    property_type_filter = "&propertyType=" + ','.join(str(x) for x in property_types)

    # identify pages to process
    url = "https://www.boliga.dk/resultat?zipCodes=" + str(zipcode) + property_type_filter
    browser.open(url)
    soup = browser.get_current_page()

    try:
        pg_stats = soup.find_all('div', attrs={'class': re.compile('paging-stats')})
        pg_stats = pg_stats[-1].get_text()
        listings_count = re.search(r'(\d+)(?!.*\d)', pg_stats).group(0)
        pages = int(np.ceil(int(listings_count) / 50))
    except IndexError:
        pages = 0

    # fetch listings
    listings = []
    for p in range(1, pages + 1):

        # open page
        url = "https://www.boliga.dk/resultat?zipCodes=" + str(zipcode) + "&page=" + str(p) + property_type_filter
        browser.open(url)

        # retrieve listings
        soup = browser.get_current_page()
        a = soup.find_all('a', attrs={'href': re.compile("^/bolig/")})
        for item in a:
            full_id = item.get('href')
            boliga_id = re.search(r'\d+', full_id).group(0)
            listings.append(boliga_id)

    return listings


def read_bolig(boliga_id, browser = ms.StatefulBrowser()) -> Housing:
    
    housing = Housing()
    
    # open page and start reading soup
    url = "https://www.boliga.dk/bolig/" + str(boliga_id)
    browser.open(url)
    soup = browser.get_current_page()

    # results stored in dict
    housing.boliga_id = boliga_id
    housing.url = url

    # fetch title + for sale status
    title = soup.find_all('title')[0]
    title = title.get_text().strip()
    address = title.split(':')
    housing.address = address[1].strip()
    housing.for_sale = 0 if address[1] == 'Tidligere salg på' else 1

    # retrieve and process section a
    def section_a(soup):
        d = {}
        section_a = soup.find_all('div', attrs={'class': 'row no-gutters'})[0]

        icon = section_a.find_all('span', attrs={'class': 'icon'})[0]
        d['property_type'] = icon.get_text().strip()

        span = section_a.find_all('span', attrs={'class': 'font-weight-bolder'})[0]
        stripped = span.get_text().strip()
        d['list_price'] = strip_digits(stripped)
        
        span = section_a.find_all('p', attrs={'class': 'ng-star-inserted'})[-1]
        stripped = span.get_text().strip()
        d['created_date'] = date_clean(stripped)

        return d

    # retrieve and process section b
    def section_b(soup):

        inner_details = soup.find_all('div', attrs={'class': 'app-inner-details'})[0]
        section_b = inner_details.find_all('use')
        d = {}
        fields = ['rooms','floor','square','lot-size', 'construction-year', 'energy', 'taxes', 'basement-size']
        
        for i in section_b:
            field = i.get('xlink:href').replace('#icon-', '')
            if field in fields:
                pp = i.find_parent().find_parent()
                spans = pp.find_all('span')
                stripped = spans[1].get_text().strip()
                d[field] = strip_digits(stripped)

        return d

    d = section_a(soup)
    housing.property_type = d['property_type']
    housing.list_price = d['list_price']
    housing.created_date = d['created_date']

    d = section_b(soup)
    housing.rooms = d['rooms']
    housing.floors = d['floor']
    housing.living_area = d['square']
    housing.lot_area = d['lot-size']
    housing.construction_year = d['construction-year']
    housing.energy_rating = d['energy']
    housing.taxes_pr_month = d['taxes']
    housing.bsmnt_area = d['basement-size']

    housing.final_price = None

    return housing


def get_bolig_from_list(id_list, browser = ms.StatefulBrowser()) -> HousingList:

    housing_list = HousingList()

    for index, boliga_id in enumerate(id_list):
        print(".. processing id %s (%s of %s)" % (boliga_id, index+1, len(id_list)))
        housing = read_bolig(boliga_id, browser)
        housing_list.append(housing)
    
    return housing_list


def get_listings_from_list(zipcodes = [], browser =  ms.StatefulBrowser()):

    print('.. processing %s zipcodes' % len(zipcodes))
    all_listings = []
    for index, zipcode in enumerate(zipcodes):
        print(".. finding listings in %s (%s of %s)" % (zipcode, index+1, len(zipcodes)))
        all_listings = all_listings + get_listings(browser, zipcode)

    return list(dict.fromkeys(all_listings))
