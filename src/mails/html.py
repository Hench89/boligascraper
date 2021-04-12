from pretty_html_table import build_table

def get_html_df(df, df_title):

    # link columns

    def add_url_tags(url):
        if url == '':
            return url
        return "URLSTART" + url + "URLEND"

    link_columns = [c for c in df.columns if 'url' in c]
    for c in link_columns:
        df[c] = df.apply(lambda x: add_url_tags(x[c]), axis=1)

    # build table
    theme = 'red_dark'
    html_table = build_table(df, theme)
    html_table = html_table.replace("URLSTART", "<a href=\"")
    html_table = html_table.replace("URLEND", "\">LINK</a>")

    # add title
    title_txt = f'<b>{df_title}</b><br>'
    return title_txt + html_table
