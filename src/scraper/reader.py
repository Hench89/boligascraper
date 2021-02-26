import mechanicalsoup as ms
import pandas as pd
import numpy as np
import re
from scraper import cleaner as cln
from helper import helper as hlp


def get_boliga_listings():

    # setup
    df_zip = pd.read_csv('./static/zipcode.csv', sep=',')
    listings = []
    browser = ms.StatefulBrowser()

    # get post numbers
    for index, zipcode in enumerate(df_zip['zipcode']):

        city_listings = _get_city_listings(browser, str(zipcode))
        for item in city_listings:
            listings.append(item)

        print(".. finding listings in %s (%s of %s)" % (zipcode, index+1, len(df_zip)))


    # return as dataframe
    df = pd.DataFrame(listings)
    df = df.drop_duplicates(subset='boliga_id', keep="last")
    df = df.reset_index(drop=True)

    return df


# get all listings for a zipcode
def _get_city_listings(browser, zipcode):
    pages_to_process = _get_pages_to_process(browser, zipcode)
    url_list = []

    for p in range(1, pages_to_process + 1):

        # open page
        url = "https://www.boliga.dk/resultat?zipCodes=" + zipcode + "&page=" + str(p) + "&propertyType=1"
        browser.open(url)

        # retrieve listings
        html = browser.get_current_page()
        a = html.find_all('a', attrs={'href': re.compile("^/bolig/")})
        for item in a:
            full_id = item.get('href')
            boliga_id = re.search(r'\d+', full_id).group(0)
            url_list.append({'boliga_id': boliga_id, 'zipcode': zipcode})

    return url_list


# get pages needed to be scraped for a for zipcode
def _get_pages_to_process(browser, zipcode):

    # open page
    browser.open("https://www.boliga.dk/resultat?zipCodes=" + zipcode + "&propertyType=1")
    html = browser.get_current_page()

    # get page stats
    try:
        pg_stats = html.find_all('div', attrs={'class': re.compile('paging-stats')})
        pg_stats = pg_stats[-1].get_text()
        listings_count = re.search(r'(\d+)(?!.*\d)', pg_stats).group(0)
        listings_num = int(listings_count)
        pages = int(np.ceil(int(listings_count) / 50))
    except IndexError:
        return 0

    return pages


# get data from a specific listing
def get_boliga_data(boliga_listings):

    browser = ms.StatefulBrowser()
    processed_listings = []

    for index, item in enumerate(boliga_listings):

        # unpack
        boliga_id = item[0]
        zipcode = item[1]
        print(".. processing id %s in %s (%s of %s)" % (boliga_id, zipcode, index+1, len(boliga_listings)))

        # pull data
        url = "https://www.boliga.dk/bolig/" + str(boliga_id)
        soup_row, soup_icons = _get_boliga_soup(browser, url)

        # process to raw dataframe
        idd = {'boliga_id': boliga_id, 'zipcode': zipcode, 'url': url}
        row_details = _process_section_a(soup_row)
        icon_details = _process_section_b(soup_icons)
        d = {**idd, **row_details, **icon_details}
        df_raw = pd.DataFrame(d, index=[0])

        # cleaning and extending dataframe
        df_clean = cln.clean_boliga_data(df_raw)

        # geo related data
        df_clean['latlng'] = df_clean['address1'].apply(lambda x: hlp.get_lat_lng(x))
        df_clean['gmaps'] = df_clean['latlng'].apply(lambda x: 'https://maps.google.com/?q=' + str(x))
        df_clean['station_dist_km'] = df_clean.apply(lambda x:
                                                     hlp.get_dist_to_station(x.zipcode, x.latlng), axis=1)
        processed_listings.append(df_clean[cln.clean_cols])

    if len(processed_listings) > 0:
        return pd.concat(processed_listings)
    return pd.DataFrame(columns=cln.clean_cols)


def _get_boliga_soup(browser, url):

    # get page
    browser.open(url)
    soup = browser.get_current_page()
    inner_details = soup.find_all('div', attrs={'class': 'app-inner-details'})[0]

    # return sections of interest
    section_a = soup.find_all('div', attrs={'class': 'row no-gutters'})[0]
    section_b = inner_details.find_all('use')
    return section_a, section_b


def _process_section_a(soup):
    d = {}
    span = soup.find_all('span', attrs={'class': 'text-muted'})[0]
    d['address'] = span.get_text().strip()
    span = soup.find_all('span', attrs={'class': 'font-weight-bolder'})[0]
    d['list_price'] = span.get_text().strip()
    span = soup.find_all('p', attrs={'class': 'ng-star-inserted'})[-1]
    d['created_date'] = span.get_text().strip()
    return d


# processing of bs4 object, related to icons on page
def _process_section_b(soup):

    d = {}

    for i in soup:

        # get all spans to read data from
        icon_name = i.get('xlink:href')
        pp = i.find_parent().find_parent()

        grp1 = ['#icon-rooms', '#icon-floor']
        grp2 = ['#icon-square', '#icon-lot-size', '#icon-construction-year',
                '#icon-energy', '#icon-taxes', '#icon-basement-size']

        if icon_name in grp1:
            spans = pp.find_all('span')
            icon_value = spans[1].get_text().strip()
            d[icon_name] = icon_value

        if icon_name in grp2:
            spans = pp.find_all('span')
            icon_value = spans[1].get_text().strip()
            d[icon_name] = icon_value

    return d
