from datetime import datetime, date

def date_clean(date_string):
    date_string = date_string.replace('Oprettet ', '').replace('.', '')
    date_value = datetime.strptime(date_string, '%d %b %Y')
    return date_value

def days_on_market(created_date_string):
    try:
        today_date = date.today()
        created_date_string = str(created_date_string)[:10]
        created_date = datetime.strptime(created_date_string, '%Y-%m-%d').date()
        return (today_date - created_date).days
    except ValueError:
        return ''
