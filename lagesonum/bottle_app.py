# coding: utf-8


from dateutil import parser
import sqlite3
import os
import datetime
import threading
import locale
from babel.dates import format_datetime
from babel.core import Locale, UnknownLocaleError

from bottle import default_app, route, view, static_file, TEMPLATE_PATH, request, BaseTemplate, debug
debug(True)

from bottle_utils.i18n import I18NPlugin
from bottle_utils.i18n import lazy_gettext as _

from input_number import is_valid_number, parse_numbers, get_fingerprint
from dbhelper import initialize_database

from contextlib import contextmanager

# store database outside of repository so it is not overwritten by git pull
MOD_PATH = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.abspath(os.path.join(MOD_PATH, '../', '../', "lagesonr.db"))

LOCALE_LOCK = threading.Lock()

if not os.path.exists(DB_PATH):
    initialize_database(DB_PATH)

lagesonrdb = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)

# locales in alphabetical order
LANGS = [    ('ar_SY', u'العربية'),
             ('de_DE', u'Deutsch'),
             ('en_US', u'English'),
             ('eo_EO', u'Esperanto')
#             ('fa_IR', u'فارسی'),
#             ('prs_AF', u'دری'),
#             ('tr_TR', u'Türkçe'),
             ]

DEFAULT_LOCALE = 'en_US'

def get_valid_locale(l):
    try:
        Locale.parse(l)
        return l
    except UnknownLocaleError:
        return DEFAULT_LOCALE

# set as global variable available in all templates (to be able to call e.g. request.locale)
BaseTemplate.defaults['request'] = request
BaseTemplate.defaults['locale_datetime'] = lambda d: format_datetime(d, format="short", locale=get_valid_locale(request.locale))


@contextmanager
def setlocale(name):
    with LOCALE_LOCK:
        saved = locale.setlocale(locale.LC_ALL)
        try:
            yield locale.setlocale(locale.LC_ALL, name)
        finally:
            locale.setlocale(locale.LC_ALL, saved)

@route('/')
@view('views/query_page')
def index():
    """landing page is page for querying numbers"""

    context = {
        'result': 'NewNumber',
        'invalid_input': '',
        'timestamps': ''
    }

    return context


@route('/enter')
@view('views/start_page')
def enter():
    return {'entered': []}


@route('/enter', method='POST')
@view('views/start_page')
def do_enter():
    """Enter numbers into database"""
    numbers = set(parse_numbers(request.forms.get('numbers', '')))
    timestamp = datetime.datetime.now()

    usr_hash = get_fingerprint(request)

    result_num = []

    with lagesonrdb as connection:
        cursor = connection.cursor()
        insert_query = 'INSERT INTO numbers (number, fingerprint, place, time) VALUES (?, ?, ?, ?)'

        for num in numbers:
            if is_valid_number(num):
                values = (num.capitalize(), usr_hash, 'LAGESO', timestamp)
                try:
                    cursor.execute(insert_query, values)
                    result_num.append(num)
                except sqlite3.IntegrityError:
                    result_num.append(_(u'erruniquenumber') + ": {}".format(num))
            else:
                result_num.append(_('errinvalinput') + ": {}".format(num))

        if not len(numbers):
            result_num.append(_('novalidnumbers'))

    return {'entered': result_num, 'timestamp': str(timestamp)[:16]}


@route('/query')
@view('views/query_page')
def query():
    return {'result': None}


@route('/query', method='POST')
@view('views/query_page')
def do_query():
    """Search for numbers in database"""
    user_input = request.forms.get('number', '')
    numbers = parse_numbers(user_input)

    number = None
    rowcount = 0
    timestamps = []
    invalid_input = None

    if numbers:
        number = numbers[0]
        with lagesonrdb as connection:
            cursor = connection.cursor()

            select_query = 'SELECT time FROM numbers WHERE number LIKE ? ORDER BY time'
            values = (number,)

            result = cursor.execute(select_query, values).fetchall()
            timestamps = [row[0] for row in result] # cut off microseconds and seconds as requested in issue 31
    else:
        invalid_input = user_input

    context = {
        'result': number or invalid_input,
        'invalid_input': invalid_input,
        'timestamps': timestamps
    }

    return context


@route('/about')
@view('views/about')
def about():
    """Return page with information about this project"""
    pass


@route('/impressum')
@view('views/impressum')
def impressum():
    """Return page with contact information"""
    pass


@route('/static/<filename:path>', no_i18n=True)
def send_static(filename):
    return static_file(filename, root=os.path.join(MOD_PATH, 'static'))

@route('/favicon.ico', no_i18n=True)
def send_static():
    return static_file("favicon.png", root=os.path.join(MOD_PATH, 'static'))

# Numbers to be shown there:
# All numbers that have been entered 3 or more times and where the last time of entry is not older than X minutes.
# For the "last time of entry age" it would be great to collect stats how long numbers are displayed in average.
# Until the stats are actually being collected, we should use 15 minutes as an "inactive" time setting.
# There should also be a link "history" where those numbers are then listed with a note "last seen".
@route('/display')
@view('views/display')
def display():
    #todo: later, refactor in constants file if up and running
    MIN_COUNT = 3
    MIN_DAYS = 5
    oldest_to_be_shown = datetime.datetime.today()-datetime.timedelta(days=MIN_DAYS)

    with lagesonrdb as connection:
        cursor = connection.cursor()

        select_query = 'SELECT number FROM numbers WHERE time >= "' \
                + oldest_to_be_shown.strftime('%Y-%m-%d %H:%M:%S') + \
                '" GROUP BY number HAVING COUNT(number) >= ' + str(MIN_COUNT)

        result = cursor.execute(select_query).fetchall()

    # filter numbers entered recently enough
    numbers_young_enough = [number[0] for number in result]

    # format numbers for later output
    display_output = "\n".join(sorted(set(numbers_young_enough)))

    with setlocale(get_valid_locale(request.locale)):
        since = oldest_to_be_shown.strftime("%x %X")
    return {'numbers': display_output,
            'since': since,
            'min_count': MIN_COUNT
            }



@route('/pm-start')
@view('static/pm-start.html')
def enter():
    return {'entered': []}


# findet templates im gleichen Verzeichnis
TEMPLATE_PATH.append(MOD_PATH)
app = default_app()
application = I18NPlugin(app, langs=LANGS, default_locale=DEFAULT_LOCALE,
                         domain='messages',
                         locale_dir=os.path.join(MOD_PATH, 'locales'))
