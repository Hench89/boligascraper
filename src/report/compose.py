from os import path, makedirs
import pandas as pd

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

    # load dataframe
    sold_list_path = f'{root_path}/clean/clean_sold_list.json'
    df = pd.read_json(sold_list_path)

    # fix columns
    df['url'] = df.apply(lambda x: set_url(x.estate_id), axis=1)
    df['list_price'] = df.apply(lambda x: fix_pricing(x.list_price), axis=1)
    df['sold_price'] = df.apply(lambda x: fix_pricing(x.sold_price), axis=1)
    df['sqm_price'] = df.apply(lambda x: fix_pricing(x.sqm_price), axis=1)
    df['price_diff'] = df.apply(lambda x: fix_pricing(x.price_diff), axis=1)


    # filtering
    cols = ['city', 'address', 'rooms', 'living_area', 'build_year', 'list_price', 'sold_price', 'sqm_price', 'price_diff', 'url', 'days_since_sale']
    df = df[cols].sort_values(by=['days_since_sale']).reset_index(drop=True).head(20)

    # save report
    report_path = f'{report_path}/sold_report.json'
    print(f'Saving report to {report_path}')
    df.to_json(report_path)


def make_for_sale_report(root_path, report_path):

    # load dataframe
    sold_list_path = f'{root_path}/clean/clean_for_sale_list.json'
    df = pd.read_json(sold_list_path)

    # fix columns
    df['url'] = df.apply(lambda x: set_url(x.estate_id), axis=1)
    df['list_price'] = df.apply(lambda x: fix_pricing(x.list_price), axis=1)
    df['sqm_price'] = df.apply(lambda x: fix_pricing(x.sqm_price), axis=1)

    # filtering
    cols = ['city', 'street', 'rooms', 'living_area', 'lot_area', 'energy_class', 'build_year', 'list_price', 'sqm_price', 'url', 'days_on_market']
    df = df[cols].sort_values(by=['days_on_market']).reset_index(drop=True)
    df = df[df['days_on_market'] < 7]

    # save report
    report_path = f'{report_path}/for_sale_report.json'
    print(f'Saving report to {report_path}')
    df.to_json(report_path)


def set_url(estate_id):
    return f'https://www.boliga.dk/bolig/{estate_id}' if estate_id != 0 else ''

def fix_pricing(price):
    price = '{:,}'.format(price)
    price = price.replace(',', '.')
    return str(price)
