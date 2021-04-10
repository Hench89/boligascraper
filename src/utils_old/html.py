from pretty_html_table import build_table

def get_html_df(df, link_columns = [], theme = 'red_dark'):

    df['index'] = df.index + 1
    for column in link_columns:
        df[column] = "URLSTART" + df[column] + "URLEND"

    html_table = build_table(df, theme)
    html_table = html_table.replace("URLSTART", "<a href=\"")
    html_table = html_table.replace("URLEND", "\">LINK</a>")

    return html_table
