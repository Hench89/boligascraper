import locale

try:
    import locale
    locale.setlocale(locale.LC_ALL, 'da_DK.utf8')
except Exception:
    locale.setlocale(locale.LC_ALL, 'da_DK.UTF-8')
