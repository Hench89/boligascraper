from .utils import load_json_folder, load_json, get_latest_file
from os import path, makedirs
import pandas as pd
import csv

def compose_sold(root_path):

    # setup paths
    raw_sold_list = f'{root_path}/raw/sold/list'
    raw_sold_estate = f'{root_path}/raw/sold/estate'
    clean_sold_list = f'{root_path}/clean'
    clean_sold_estate =  f'{root_path}/clean'

    clean_fodler = f'{root_path}/clean/'
    if not path.exists(clean_fodler):
        makedirs(clean_fodler)

    # load list
    latest_file = get_latest_file(raw_sold_list)
    print(f'Latest file is: {latest_file}')
    list_dict = load_json(latest_file)
    df_sold = pd.DataFrame(list_dict)

    # to files
    df_sold.to_json(f'{clean_sold_list}/list.json')
    df_sold.to_csv(f'{clean_sold_list}/list.csv', quoting=csv.QUOTE_NONNUMERIC)

    # load data
    list_dict = load_json_folder(raw_sold_estate)
    df_estate = pd.DataFrame(list_dict)

    # to json
    df_estate.to_json(f'{clean_sold_estate}/estate.json')
    df_estate.to_csv(f'{clean_sold_estate}/estate.csv', quoting=csv.QUOTE_NONNUMERIC)
