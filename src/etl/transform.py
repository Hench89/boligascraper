from os import path, makedirs, listdir
from utils import (
    strip_digits, 
    compare_number_sets, 
    get_decompressed_soup_from_file,
    get_geo_details,
    date_clean,
    dict_to_json
)

def transform_new(archive_path, stations):

    # setup clean dir if not exists
    raw_path = archive_path + '/raw/'
    clean_path = archive_path + '/clean/'
    if not path.exists(clean_path):
        makedirs(clean_path)

    # check changes between layers
    ids_in_raw = [strip_digits(name) for name in listdir(raw_path) if path.isfile(path.join(raw_path, name))]
    ids_in_clean = [strip_digits(name) for name in listdir(clean_path) if path.isfile(path.join(clean_path, name))]
    to_transform, unchanged, to_remove = compare_number_sets(ids_in_raw, ids_in_clean)

    # decompress and save again
    for i, id in enumerate(to_transform):
        raw_file = id_path(raw_path, id, 'gzip')
        clean_file = id_path(clean_path, id, 'json')

        print('opening %s to save in %s (%s of %s)' % (raw_file, clean_file, i+1, len(to_transform)))

        # make results to dict
        soup = get_decompressed_soup_from_file(raw_file)
        dict_boliga = read_boliga(soup)
        dict_boliga['boliga_id'] = int(id)
        dict_boliga['url'] = 'https://www.boliga.dk/bolig/' + str(id)
        dict_geo = get_geo_details(dict_boliga['address'], stations)
        dict_boliga.update(dict_geo)
        
        # save file
        dict_to_json(dict_boliga, clean_file)

    
def id_path(path, id, file_format):
    return path + str(id) + '.' + file_format

def read_boliga(soup):
    
    dict = {}

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
        d['created_date'] = str(date_clean(stripped))

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
