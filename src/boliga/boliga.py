import mechanicalsoup as ms
import numpy as np
from utils import date_clean, strip_digits, get_geo_details
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


def read_boliga(boliga_id, browser = ms.StatefulBrowser()):
    
    dict = {}
    
    # open page and start reading soup
    url = "https://www.boliga.dk/bolig/" + str(boliga_id)
    browser.open(url)
    soup = browser.get_current_page()

    # results stored in dict
    dict['boliga_id'] = boliga_id
    dict['url'] = url

    # fetch title + for sale status
    def title(soup):
        d = {}
        title = soup.find_all('title')[0]
        title = title.get_text().strip()
        address = title.split(':')
        d['address'] = address[1].strip()
        d['for_sale'] = 0 if address[0] == 'Tidligere salg på' else 1
        return d

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

    def max_sold_price(soup):
        try:
            history = soup.find_all('app-real-estate-property-info-history')[0]
            price = history.find_all('td', attrs={'class': 'text-right price-col'})
            txt = []
            for p in price:
                spans = p.find_all('span')
                for s in spans:
                    txt.append(s.get_text().strip())
            stripped = [strip_digits(s) for s in txt]
            stripped_int = [s for s in stripped if isinstance(s, int)]
            return str(max(stripped_int))
        except Exception:
            return ''
    
    # merge to one dict
    dict.update(title(soup))
    dict.update(section_a(soup))
    dict.update(section_b(soup))
    dict['final_price'] = max_sold_price(soup) if dict['for_sale'] == 0 else ''
    
    # rename dict to fit class names
    rename_dict = {
        'floor': 'floors', 
        'square': 'living_area', 
        'lot-size' : 'lot_area',
        'energy' : 'energy_rating',
        'taxes' : 'taxes_per_month',
        'basement-size' : 'bsmt_area'
    }
    for k, v in rename_dict.items():
        dict[v] = dict.pop(k)

    return dict


def get_bolig_from_list(id_list, stations, browser = ms.StatefulBrowser()):

    housing_list = []
    for index, boliga_id in enumerate(id_list):
        print(".. processing id %s (%s of %s)" % (boliga_id, index+1, len(id_list)))

        # fetch data from boliga
        housing = read_boliga(boliga_id, browser=browser)

        # add geo details
        geo = get_geo_details(housing['address'], stations)
        housing.update(geo)
        housing_list.append(housing)
    
    return housing_list


def get_listings_from_list(zipcodes = [], browser =  ms.StatefulBrowser()):

    print('Processing %s zipcodes' % len(zipcodes))
    all_listings = []
    for index, zipcode in enumerate(zipcodes):
        print(".. finding listings in %s (%s of %s)" % (zipcode, index+1, len(zipcodes)))
        all_listings = all_listings + get_listings(browser, zipcode)

    return list(dict.fromkeys(all_listings))
