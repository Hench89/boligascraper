from clean import save_dataframes
import traceback
import sys


print('===== Getting Started =====')

archive_path = './archive'
raw_sold_path = f'{archive_path}/raw/sold'
raw_estate_path = f'{archive_path}/raw/estate'
clean_path = f'{archive_path}/clean'

print('===== Saving raw data as dataframes =====')
try:
    save_dataframes(raw_sold_path, raw_estate_path, clean_path)
except:
    print('Unable to save as dataframes!')
    traceback.print_exc()
    sys.exit()

print('Done!')
