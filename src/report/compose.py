from .html import get_html_df
from .emails import send_ssl_mail
from .utils import add_days_ago, fix_pricing
import pandas as pd
import os

def compose(root_path):

    print(f'===== MAILING REPORT =====')
    
    # prepare htmltable - for sale
    baseline_path = f'{root_path}/baseline'
    input_file_path = f'{baseline_path}/forsale.json'
    for_sale_html_table = prepare_for_sale(input_file_path, 'For Sale')
    
    # prepare htmltable - sold
    input_file_path = f'{baseline_path}/sold.json'
    sold_html_table = prepare_sold(input_file_path, 'Sold')

    # merge to body and sent
    email_body = '<br><br>'.join([for_sale_html_table, sold_html_table])
    send_email(email_body)


def prepare_for_sale(input_file_path, header):

    # read data
    df = pd.read_json(input_file_path, orient='table')

    # fix columns
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

    df = df[cols].sort_values(by=['days']).reset_index(drop=True)
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
