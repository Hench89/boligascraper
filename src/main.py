import pandas as pd
import boliga_reader as br
import helper as hlp
import config as cnf
import os

# read from archive
try:
    df_old = pd.read_csv('../data/boliga.csv', sep=';')
    print('(1) read from archive:', len(df_old), 'listings')
except FileNotFoundError:
    df_old = pd.DataFrame(columns=cnf.clean_cols)
    print('(1) starting a new archive')

# read from boliga
print('(2) reading from boliga')
df_new = br.get_boliga_listings()

# ids to remove and insert
print('(3) identifying what to remove and insert')
list_old = df_old['boliga_id'].astype(str).to_numpy()
list_new = df_new['boliga_id'].astype(str).to_numpy()
list_add = [x for x in list_new if x not in list_old]
list_rem = [x for x in list_old if x not in list_new]
print('..to insert:', len(list_add))
print('..to delete:', len(list_rem))

df_old = df_old[~df_old['boliga_id'].astype(str).isin(list_rem)].reset_index(drop=True)
df_add = df_new[df_new['boliga_id'].astype(str).isin(list_add)].reset_index(drop=True)

# process items
if len(df_add) > 0:
    print('(4) retrieving new items ..')
    items_to_process = df_add[['boliga_id', 'zipcode']].to_numpy()
    df_new = br.get_boliga_data(items_to_process)

# merge data
try:
    df = pd.concat([df_old, df_new]).reset_index(drop=True)
except ValueError:
    df = df_old

# date related data
print('(5) saving to archive ..')
df['market_days'] = df.apply(lambda x: hlp.days_on_market(x.created_date), axis=1)
df = df.sort_values(by=['market_days', 'list_price']).reset_index(drop=True)
df = df[cnf.print_cols]

# save csv
csv_path = '../data/boliga.csv'
os.remove(csv_path)
df.to_csv(csv_path, index=False, sep=';')

# save excel
excel_path = '../data/boliga.xlsx'
os.remove(excel_path)
hlp.write_to_excel(df, excel_path)