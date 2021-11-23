from os import path, makedirs
import pandas as pd
import pandasql as ps
from .utils import get_property_types, set_url


def compose(root_path):

    print(f'===== BASELINE =====')

    # prepare staging paths
    input_folder_path = f'{root_path}/clean/'
    baseline_path = f'{root_path}/baseline'
    if not path.exists(baseline_path):
        makedirs(baseline_path)

    # make sold baseline
    input_list_path = f'{input_folder_path}/sold_list.json'
    input_estate_path = f'{input_folder_path}/sold_estate.json'
    output_file_path = f'{baseline_path}/sold.json'
    make_sold_baseline(input_list_path, input_estate_path, output_file_path)

    # make for sale baseline
    input_list_path = f'{input_folder_path}/for_sale_list.json'
    input_estate_path = f'{input_folder_path}/for_sale_estate.json'
    output_file_path = f'{baseline_path}/forsale.json'
    make_for_sale_baseline(input_list_path, input_estate_path, output_file_path)


def make_sold_baseline(input_list_path, input_estate_path, output_file_path):

    # load dataframes
    df_list = pd.read_json(input_list_path, orient='table')
    df_estate = pd.read_json(input_estate_path, orient='table')
    df_types = get_property_types()

    # merge data to get meaningful sold list
    q = """
        SELECT
            IFNULL(E.estate_id, 0) AS estate_id,
            E.estate_url,
            E.area_category_id,
            E.municipality_code,
            COALESCE(E.city, L.city) AS city,
            E.zip_code,
            L.address,
            E.lat,
            E.lon,
            T.property_id,
            T.alias AS type,
            COALESCE(E.build_year, L.build_year) AS built,
            COALESCE(E.living_area, L.living_area) AS living_area,
            E.lot_area,
            E.bsmnt_area,
            COALESCE(E.rooms, L.rooms) AS rooms,
            E.floor,
            IFNULL(UPPER(E.energy_class), '-') AS energy,
            E.net,
            E.exp,
            E.created_date,
            E.list_price,
            L.sold_price,
            L.sold_date,
            L.sale_type,
            COALESCE(L.price_change, E.price_change) AS price_change,
            COALESCE(L.sqm_price, E.sqm_price) AS sqm_price,
            E.days_for_sale
        FROM df_list L
        LEFT JOIN df_estate E ON E.estate_id = L.estate_id
        INNER JOIN df_types T ON T.property_id = COALESCE(E.property_type, L.property_type)
        """
    df = ps.sqldf(q)

    # add cols
    df['price_diff'] = df['sold_price'] - df['list_price']
    df['boliga_url'] = df.apply(lambda x: set_url(x.estate_id), axis=1)

    # save report
    print(f'Saving report to {output_file_path}')
    df.to_json(output_file_path, orient='table')


def make_for_sale_baseline(input_list_path, input_estate_path, output_file_path):

    # load dataframe
    df_list = pd.read_json(input_list_path, orient='table')
    df_estate = pd.read_json(input_estate_path, orient='table')
    df_types = get_property_types()

    # merge data to get meaningful sold list
    q = """
        SELECT
            L.estate_id,
            L.created_date,
            T.property_id,
            T.alias AS type,
            L.city,
            L.municipality_code,
            L.address,
            E.clean_street,
            L.zip_code,
            L.area_category_id,
            L.build_year AS built,
            L.energy_class AS energy,
            L.rooms,
            L.floor,
            L.living_area,
            L.lot_area,
            L.bsmnt_area,
            L.list_price,
            L.price_change,
            L.sqm_price,
            L.lat,
            L.lon,
            L.net,
            L.exp,
            E.estate_url AS realtor_url
        FROM df_list L
        LEFT JOIN df_estate E ON E.estate_id = L.estate_id
        INNER JOIN df_types T ON T.property_id = L.property_type
        """
    df = ps.sqldf(q)

    # add cols
    df['boliga_url'] = df.apply(lambda x: set_url(x.estate_id), axis=1)

    # save report
    print(f'Saving report to {output_file_path}')
    df.to_json(output_file_path, orient='table')
