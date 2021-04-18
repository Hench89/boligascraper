from .html import get_html_df
from .emails import send_ssl_mail
from .utils import add_days_ago, fix_pricing, float_to_int_text
import numpy as np
import pandas as pd
import pandasql as ps
import os


def compose(root_path):

    print(f'===== MAILING REPORT =====')

    # files
    baseline_path = f'{root_path}/baseline'
    sold_input_file_path = f'{baseline_path}/sold.json'
    for_sale_input_file_path = f'{baseline_path}/forsale.json'

    # sold stats
    df_sold_stats = prepare_sold_stats(sold_input_file_path)

    # prepare htmltable - sold
    sold_html = prepare_sold(sold_input_file_path, 'Sold')
    for_sale_html = prepare_for_sale(for_sale_input_file_path, df_sold_stats, 'For Sale')

    # merge to body and sent
    email_body = '<br><br>'.join([for_sale_html, sold_html])
    send_email(email_body)



def prepare_sold_stats(input_file_path):

    # read data
    df = pd.read_json(input_file_path, orient='table')

    # filter
    df = add_days_ago(df, 'sold_date', 'days')
    df = df.query("sale_type == 'Alm. Salg' & days < 365")

    # generate stats
    stats = []
    for c in np.unique(df['city']):
        for pi in np.unique(df['property_id']):
            for er in np.unique(df['energy']):

                # filter data
                df_stats = df.query(f"city == '{c}' & property_id == {pi}")
                if not er == '-':
                    df_stats = df_stats.query(f"energy == '{er}'")

                n = df_stats.shape[0]
                if n == 0:
                    continue

                d = {
                    'city' : c,
                    'property_id': pi,
                    'energy_rating': er,
                    'n' : n,
                    'sqm_mean' : int(df_stats['sqm_price'].mean()),
                    'sqm_mode' : int(df_stats['sqm_price'].mode()[0]),
                    'sqm_std' : 0 if n == 1 else int(df_stats['sqm_price'].std())
                }
                stats.append(d)

    return pd.DataFrame(stats)


def prepare_for_sale(input_file_path, df_sold_stats, header):

    # read data
    df = pd.read_json(input_file_path, orient='table')
    df = add_days_ago(df, 'created_date', 'days')

    # filter data
    df = df[df['days'] < 30]
    df = df[df['property_id'].isin([1,2])]

    q = """
        SELECT
            D.city,
            D.street,
            D.type,
            D.rooms,
            D.living_area,
            D.lot_area,
            D.energy,
            D.built,
            D.list_price,
            D.sqm_price,
            S.sqm_mean AS market_mean,
            S.n AS market_n,
            D.sqm_price - S.sqm_mean AS market_diff,
            '' AS market,
            D.boliga_url,
            D.realtor_url,
            D.days
        FROM df D
        LEFT JOIN df_sold_stats S
            ON  S.city = D.city
            AND S.property_id = D.property_id
            AND S.energy_rating = D.energy

        ORDER BY D.city, D.days
        """
    df = ps.sqldf(q)

    # finetuning of presentation
    df['city'] = df.apply(lambda x: 'Lyngby' if x.city == 'Kongens Lyngby' else x.city, axis=1)
    df['list_price'] = df.apply(lambda x: fix_pricing(x.list_price), axis=1)
    df['sqm_price'] = df.apply(lambda x: fix_pricing(x.sqm_price), axis=1)
    df['market_mean'] = df.apply(lambda x: fix_pricing(x.market_mean), axis=1)
    df['market_diff'] = df.apply(lambda x: fix_pricing(x.market_diff), axis=1)
    df['market'] = df.apply(lambda x: f'{x.market_mean},n={float_to_int_text(x.market_n)} ({x.market_diff})', axis=1)
    df = df.drop(columns=['market_mean', 'market_n', 'market_diff'])

    return get_html_df(df, header)


def prepare_sold(input_file_path, header):

    # fetch sold data
    df = pd.read_json(input_file_path, orient='table')

    # make fancy
    df = add_days_ago(df, 'sold_date', 'days')
    df['price_diff'] = df.apply(lambda x: fix_pricing(x.price_diff), axis=1)
    df['list_price'] = df.apply(lambda x: fix_pricing(x.list_price), axis=1)
    df['sold_price'] = df.apply(lambda x: fix_pricing(x.sold_price), axis=1)
    df['sqm_price'] = df.apply(lambda x: fix_pricing(x.sqm_price), axis=1)

    df = df[df['sale_type'] == 'Alm. Salg']
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
    df = df[cols]
    df = df.sort_values(by=['days']).reset_index(drop=True)
    df = df.head(30)

    return get_html_df(df, header)


def send_email(email_body):

    # retrieve environment variables
    try:
        env_send_from = os.getenv('MAILFROM')
        env_send_to = os.getenv('MAILTO')
        env_send_to = env_send_to.split(';') if ';' in env_send_to else env_send_to
        env_password = os.getenv('MAILPASSWORD')
    except:
        print('Unable to retrieve environment variables!')
        pass

    # send email
    send_ssl_mail(
        send_from = env_send_from,
        password = env_password,
        subject = "Housing Agent",
        body = email_body,
        server = "smtp.gmail.com",
        port = 465,
        send_to = env_send_to
    )
