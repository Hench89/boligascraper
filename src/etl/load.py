from os import path, listdir
from utils import days_on_market, read_local_json, get_html_df
import pandas as pd

def get_dataframe(archive_path):

    # read everything into dataframe
    clean_path = archive_path + '/clean/'
    files = [clean_path + file for file in listdir(clean_path) if path.isfile(path.join(clean_path, file))]
    json_dumps = [read_local_json(file) for file in files]
    df = pd.DataFrame(json_dumps)

    # enrich dataframe
    df['market_days'] = df.apply(lambda x: days_on_market(x['created_date']),axis=1)
    df['url'] = 'https://www.boliga.dk/bolig/' + str(df['boliga_id'])
    df['gmaps'] = df.apply(lambda x: None if x.latlon == '' else 'https://maps.google.com/?q=' + x.latlon, axis=1)
    df = df.sort_values(by=['market_days']).reset_index(drop=True)
    
    return df

def get_html_dataframe(archive_path):

    df = get_dataframe(archive_path)

    # prepare archive for email
    output_columns = ['address', 'property_type', 'list_price', 'living_area', 'rooms', 'url', 'gmaps', 'station_dist_km', 'market_days']
    link_columns = ['url', 'gmaps']
    
    # get table for villa
    df['list_price'] = df.apply(lambda x: '{:,}'.format(x.list_price).replace(',', '.'), axis=1)
    df = df[output_columns]
    df = df[df['market_days'] <= 7].reset_index(drop=True)
    return get_html_df(df, link_columns=link_columns)
