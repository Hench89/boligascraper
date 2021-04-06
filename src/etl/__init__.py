from etl.extract import extract_new
from etl.transform import transform_new
from etl.load import load

import locale

try:
    import locale
    locale.setlocale(locale.LC_ALL, 'da_DK.utf8')
except Exception:
    locale.setlocale(locale.LC_ALL, 'da_DK.UTF-8')
