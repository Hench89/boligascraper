from os import path, listdir
from utils import days_on_market, read_json
import pandas as pd

def load(archive_path):

    # read everything into dataframe
    clean_path = archive_path + '/clean/'
    files = [clean_path + file for file in listdir(clean_path) if path.isfile(path.join(clean_path, file))]
    json_dumps = [read_json(file) for file in files]
    df = pd.DataFrame(json_dumps)

    # enrich dataframe
    df['market_days'] = df.apply(lambda x: days_on_market(x['created_date']),axis=1)
    df = df.sort_values(by=['market_days'])

    return df
