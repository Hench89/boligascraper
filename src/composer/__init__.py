from boliga import get_listings_from_list, get_bolig_from_list
from composer.compose import wrap_compose, compose
import locale

try:
    import locale
    locale.setlocale(locale.LC_ALL, 'da_DK.utf8')
except Exception:
    locale.setlocale(locale.LC_ALL, 'da_DK.UTF-8')
