import mechanicalsoup as ms
import pandas as pd
import numpy as np
from dfutils.geo import get_dk_lat_lng, get_nearest_station
from dfutils.dates import date_clean
import re

def get_browser():
    return ms.StatefulBrowser()

def get_listings(browser, zipcode):

    # identify pages to process
    browser.open("https://www.boliga.dk/resultat?zipCodes=" + str(zipcode) + "&propertyType=1,2")
    soup = browser.get_current_page()

    try:
        pg_stats = soup.find_all('div', attrs={'class': re.compile('paging-stats')})
        pg_stats = pg_stats[-1].get_text()
        listings_count = re.search(r'(\d+)(?!.*\d)', pg_stats).group(0)
        listings_num = int(listings_count)
        pages = int(np.ceil(int(listings_count) / 50))
    except IndexError:
        pages = 0

    # fetch listings
    listings = []
    for p in range(1, pages + 1):

        # open page
        url = "https://www.boliga.dk/resultat?zipCodes=" + str(zipcode) + "&page=" + str(p) + "&propertyType=1,2"
        browser.open(url)

        # retrieve listings
        soup = browser.get_current_page()
        a = soup.find_all('a', attrs={'href': re.compile("^/bolig/")})
        for item in a:
            full_id = item.get('href')
            boliga_id = re.search(r'\d+', full_id).group(0)
            listings.append(boliga_id)

    return listings

def read_bolig(browser, boliga_id):
    
    # open page and get soup
    url = "https://www.boliga.dk/bolig/" + str(boliga_id)
    browser.open(url)
    soup = browser.get_current_page()

    # results stored in dict
    d = {'boliga_id' : boliga_id, 'url' : url}

    # fetch title
    title = soup.find_all('title')[0]
    title = title.get_text().strip()
    d['address'] = title.replace('Til salg:', '')

    # retrieve and process section a
    section_a = soup.find_all('div', attrs={'class': 'row no-gutters'})[0]
    icon = section_a.find_all('span', attrs={'class': 'icon'})[0]
    d['property_type'] = icon.get_text().strip()
    span = section_a.find_all('span', attrs={'class': 'font-weight-bolder'})[0]
    d['list_price'] = span.get_text().strip()
    span = section_a.find_all('p', attrs={'class': 'ng-star-inserted'})[-1]
    d['created_date'] = span.get_text().strip()

    # retrieve and process section b
    inner_details = soup.find_all('div', attrs={'class': 'app-inner-details'})[0]
    section_b = inner_details.find_all('use')

    for i in section_b:

        # get all spans to read data from
        icon_name = i.get('xlink:href')
        pp = i.find_parent().find_parent()

        grp = ['#icon-rooms', '#icon-floor', '#icon-square', '#icon-lot-size', '#icon-construction-year',
                '#icon-energy', '#icon-taxes', '#icon-basement-size']

        if icon_name in grp:
            spans = pp.find_all('span')
            icon_value = spans[1].get_text().strip()
            d[icon_name] = icon_value

    df = pd.DataFrame(d, index=[0])
    
    # rename some columns
    rename_dict = {
        '#icon-square': 'living_area',
        '#icon-lot-size': 'lot_area',
        '#icon-rooms': 'rooms',
        '#icon-floor': 'floors',
        '#icon-construction-year': 'construction_date',
        '#icon-energy': 'energy_rating',
        '#icon-taxes': 'taxes_pr_month',
        '#icon-basement-size': 'bsmnt_area'
    }
    df = df.rename(columns=rename_dict)

    # trim and clean
    trim = re.compile(r'[^\d]+')
    df['address'] = df['address'].apply(lambda x: x.strip())
    df['list_price'] = df['list_price'].apply(lambda x: trim.sub('', x))
    df['living_area'] = df['living_area'].apply(lambda x: trim.sub('', x))
    df['lot_area'] = df['lot_area'].apply(lambda x: trim.sub('', x))
    df['floors'] = df['floors'].apply(lambda x: trim.sub('', x))
    df['taxes_pr_month'] = df['taxes_pr_month'].apply(lambda x: trim.sub('', x))
    df['bsmnt_area'] = df['bsmnt_area'].apply(lambda x: trim.sub('', x))
    df['created_date'] = df['created_date'].apply(lambda x: date_clean(x))

    # return ordered dataframe
    ordered_columns = [
            'boliga_id', 'property_type', 'address', 'list_price', 'living_area', 'lot_area', 'rooms', 
            'floors', 'construction_date', 'energy_rating', 'taxes_pr_month', 
            'bsmnt_area', 'created_date', 'url'
    ]
    return df[ordered_columns]
