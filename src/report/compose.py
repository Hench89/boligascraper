from os import path, makedirs
import pandas as pd
import pandasql as ps
from .utils import (
    fix_pricing,
    add_days_ago,
    set_url,
    get_property_types
)


def compose(root_path):

    print(f'===== REPORT =====')

    # prepare clean folder
    report_path = f'{root_path}/report'
    if not path.exists(report_path):
        makedirs(report_path)

    # make reports
    make_sold_report(root_path, report_path)
    make_for_sale_report(root_path, report_path)


def make_sold_report(root_path, report_path):

    # load dataframes
    sold_list_path = f'{root_path}/clean/clean_sold_list.json'
    sold_estate_path = f'{root_path}/clean/clean_sold_estate.json'

    df_list = pd.read_json(sold_list_path, orient='table')
    df_estate = pd.read_json(sold_estate_path, orient='table')
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
            E.street,
            E.clean_street,
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

    # pricing cols
    df['price_diff'] = df['sold_price'] - df['list_price']
    df['price_diff'] = df.apply(lambda x: fix_pricing(x.price_diff), axis=1)
    df['list_price'] = df.apply(lambda x: fix_pricing(x.list_price), axis=1)
    df['sold_price'] = df.apply(lambda x: fix_pricing(x.sold_price), axis=1)
    df['sqm_price'] = df.apply(lambda x: fix_pricing(x.sqm_price), axis=1)
    
    # helper cols
    df['boliga_url'] = df.apply(lambda x: set_url(x.estate_id), axis=1)
    df = add_days_ago(df, 'sold_date', 'days')

    # filtering
    cols = [
        'city',
        'address',
        'type',
        'rooms',
        'living_area',
        'built',
        'list_price',
        'sold_price',
        'sqm_price',
        'energy',
        'price_diff',
        'boliga_url',
        'days'
    ]
    df = df[cols].sort_values(by=['days']).reset_index(drop=True).head(30)

    # save report
    report_path = f'{report_path}/sold_report.json'
    print(f'Saving report to {report_path}')
    df.to_json(report_path, orient='table')


def make_for_sale_report(root_path, report_path):

    # load dataframe
    sold_list_path = f'{root_path}/clean/clean_for_sale_list.json'
    sold_estate_path = f'{root_path}/clean/clean_for_sale_estate.json'

    df_list = pd.read_json(sold_list_path, orient='table')
    df_estate = pd.read_json(sold_estate_path, orient='table')
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
            L.street,
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

    # fix columns
    df['boliga_url'] = df.apply(lambda x: set_url(x.estate_id), axis=1)
    df['list_price'] = df.apply(lambda x: fix_pricing(x.list_price), axis=1)
    df['sqm_price'] = df.apply(lambda x: fix_pricing(x.sqm_price), axis=1)
    df = add_days_ago(df, 'created_date', 'days')

    # filtering
    cols = [
        'city',
        'street',
        'type',
        'rooms',
        'living_area',
        'lot_area',
        'energy',
        'built',
        'list_price',
        'sqm_price',
        'boliga_url',
        'realtor_url',
        'days'
    ]
    df = df[cols].sort_values(by=['days']).reset_index(drop=True)
    df = df[df['days'] < 14]

    # save report
    report_path = f'{report_path}/for_sale_report.json'
    print(f'Saving report to {report_path}')
    df.to_json(report_path, orient='table')
