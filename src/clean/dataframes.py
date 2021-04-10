from .utils import load_json_folder, load_json, get_latest_file
from os import path, makedirs
import pandas as pd
import csv

def save_dataframes(raw_path_sold, raw_path_estate, clean_path):

    if not path.exists(clean_path):
        makedirs(clean_path)

    # load data
    latest_file = get_latest_file(raw_path_sold)
    list_dict = load_json(latest_file)
    df_sold = pd.DataFrame(list_dict)

    # to files
    df_sold.to_json(f'{clean_path}/sold.json')
    df_sold.to_csv(f'{clean_path}/sold.csv', quoting=csv.QUOTE_NONNUMERIC)

    # load data
    list_dict = load_json_folder(raw_path_estate)
    df_estate = pd.DataFrame(list_dict)
    df_estate_active = df_estate[df_estate['isActive'] == True]
    df_estate_inactive = df_estate[df_estate['isActive'] == False]

    # to json
    df_estate.to_json(f'{clean_path}/estate_all.json')
    df_estate_active.to_json(f'{clean_path}/estate_active.json')
    df_estate_inactive.to_json(f'{clean_path}/estate_inactive.json')

    # to csv
    df_estate.to_csv(f'{clean_path}/estate_all.csv', quoting=csv.QUOTE_NONNUMERIC)
    df_estate_active.to_csv(f'{clean_path}/estate_active.csv', quoting=csv.QUOTE_NONNUMERIC)
    df_estate_inactive.to_csv(f'{clean_path}/estate_inactive.csv', quoting=csv.QUOTE_NONNUMERIC)

