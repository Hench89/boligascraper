from pretty_html_table import build_table
from urllib.parse import urlparse


def get_html_df(df, df_title):

    # make url columns to one
    url_columns = [c for c in df.columns if 'url' in c]
    df['links'] = df.apply(lambda x: ', '.join([add_url_tags(x[c]) for c in url_columns]), axis=1)
    df = df.drop(columns=url_columns)

    # make address short
    def trunc(txt):
        return txt[:15] + '..' if len(txt) > 15 else txt
    df['address'] = df.apply(lambda x: trunc(x.address), axis=1)

    # build table
    theme = 'red_dark'
    html_table = build_table(df, theme)
    html_table = html_table.replace("URLSTART", "<a href=\"")
    html_table = html_table.replace("URLMID", "\">")
    html_table = html_table.replace("URLEND", "</a>")

    # add title
    title_txt = f'<b>{df_title}</b><br>'
    return title_txt + html_table


def add_url_tags(url):
    if url == '-':
        return url
    domain = get_domain(url)
    return "URLSTART" + url + "URLMID" + domain + "URLEND"


def get_domain(url):
    domain = urlparse(url).netloc
    domain = domain.replace('.dk', '')
    domain = domain.replace('.com', '')
    domain = domain.replace('.', '')
    domain = domain.replace('www', '')
    domain = domain.replace('google', 'maps')
    return domain
