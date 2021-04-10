from utils import send_ssl_mail
from etl import get_dataframe
import os
import sys
import traceback

# prepare table
try:
    # read archive
    archive_path = "./archive/"
    df = get_dataframe(archive_path)
    print(df)
except:
    print('Unable to read and prepare table from archive!')
    traceback.print_exc()
    sys.exit()
