import re
from numpy import ceil
from os import path, makedirs, listdir
from utils import get_soup_from_url, get_compressed_html_from_url


def extract_new(archive_path, zipcodes = [], property_types = [1,2]):

    if len(zipcodes)==0 or len(property_types)==0:
        return print('zipcodes and property types not configured correctly!')

    # setup raw dir if not exists
    raw_path = archive_path + '/raw/'
    if not path.exists(raw_path):
        makedirs(raw_path)

    # get page stats
    property_type_filter = "&propertyType=" + ','.join(str(x) for x in property_types)
    zipcode_filter = "&zipCodes=" + ','.join(str(x) for x in zipcodes)
    url = "https://www.boliga.dk/resultat?zipCodes=" + zipcode_filter + property_type_filter
    print('getting soup from %s' % url)
    soup = get_soup_from_url(url)
    pages_to_process = get_page_stats(soup)
    print('need to process %s pages' % pages_to_process)

    # iterate pages to get ids
    all_ids = []
    for page_number in range(1, pages_to_process+1):
        page_url = url + '&page=' + str(page_number)
        print('getting soup from %s' % page_url)
        soup = get_soup_from_url(page_url)
        page_ids = get_bolig_ids(soup)
        all_ids.extend(page_ids)

    all_ids = list(set(all_ids)) # distinct
    
    # check if page already fetched in raw
    ids_to_get = [id for id in all_ids if not path.exists(id_path(raw_path, id))]

    # print summary
    raw_files = len([name for name in listdir(raw_path) if path.isfile(path.join(raw_path, name))])
    print('total ids in archive: %s' % raw_files)
    print('for sale ids: %s' % len(all_ids))
    print('to fetch: %s' % len(ids_to_get))

    # download and store in raw folder
    for i, id in enumerate(ids_to_get):
        filepath = id_path(raw_path, id)
        print('fetching, minifying and compressing to file: %s (%s of %s)' % (filepath, i+1, len(ids_to_get)))
        url = 'https://www.boliga.dk/bolig/' + str(id)
        bytes = get_compressed_html_from_url(url)
        with open(filepath, 'wb') as f:
                f.write(bytes)


def get_page_stats(soup):
    try:
        pg_stats = soup.find_all('div', attrs={'class': re.compile('paging-stats')})
        pg_stats = pg_stats[-1].get_text()
        listings_count = re.search(r'(\d+)(?!.*\d)', pg_stats).group(0)
        return int(ceil(int(listings_count) / 50))
    except IndexError:
        return 0


def get_bolig_ids(soup):

    def read_id(tag):
        full_id = tag.get('href')
        return re.search(r'\d+', full_id).group(0)

    a_tags = soup.find_all('a', attrs={'href': re.compile("^/bolig/")})
    return [read_id(tag) for tag in a_tags]


def id_path(path, id):
    return path + str(id) + '.gzip'
