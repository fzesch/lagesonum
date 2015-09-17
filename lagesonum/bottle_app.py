# coding: utf-8

import sqlite3
import os
import time
import hashlib
import re

from bottle import default_app, route, view, static_file, TEMPLATE_PATH, request

from bottle_utils.i18n import I18NPlugin

from dbhelper import initialize_database
from input_number import is_valid_number

MOD_PATH = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.abspath(os.path.join(MOD_PATH, '..', '..', "lagesonr.db"))

if not os.path.exists(DB_PATH):
    initialize_database(DB_PATH)

lagesonrdb = sqlite3.connect(DB_PATH)

# todo: populate list dynamically based on available/selected translations
LANGS = [
    ('de_DE', 'Deutsch'),
    ('en_US', 'English'),
]
# ('ar_AR', 'Arab'),
DEFAULT_LOCALE = 'en_US'


@route('/')
@view('start_page')
def index():
    """1.Seite: Helfer steht am LaGeSo und gibt Nummern ein [_____] """
    return {'entered': []}


def get_fingerprint(request):
    usr_agent = str(request.environ.get('HTTP_USER_AGENT', ''))
    usr_lang = str(request.environ.get('HTTP_ACCEPT_LANGUAGE', ''))
    usr_ip = str(request.remote_addr)

    usr_fingerprint = u'{}{}{}'.format(usr_agent, usr_lang, usr_ip)

    return hashlib.md5(usr_fingerprint.encode("utf-8")).hexdigest()


def parse_numbers(input_string, first_only=False):
    r = re.compile(r'[a-z]\s*[0-9]+', re.IGNORECASE)
    input_string = input_string.upper()

    numbers = []
    if first_only:
        numbers += r.search(input_string).groups()
    else:
        numbers += r.findall(input_string)

    return [''.join(num.split()) for num in numbers]


@route('/', method='POST')
@view('start_page')
def do_enter():
    numbers = set(parse_numbers(request.forms.get('numbers', '')))
    timestamp = time.asctime()

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
                    result_num.append("ALREADY KNOWN: {}".format(num))
            else:
                result_num.append("INVALID INPUT: {}".format(num))

    return {'entered': result_num, 'timestamp': timestamp}


@route('/query')
@view('query_page')
def query():
    return {'result': '-', 'timestamp_first': '-', 'timestamp_last': '-',
            'n': '-'}


@route('/query', method='POST')
@view('query_page')
def do_query():
    numbers = parse_numbers(request.forms.get('number', ''))

    number = ''
    rowcount = 0
    timestamp_first = 'NOT FOUND'

    if numbers:
        number = numbers[0]
        with lagesonrdb as connection:
            cursor = connection.cursor()

            select_query = 'SELECT * FROM numbers WHERE number LIKE ? ORDER BY time'
            values = (number,)

            result = cursor.execute(select_query, values).fetchall()
            if len(result) > 0:
                rowcount = len(result)
                timestamp_first = result[0][0]
                timestamp_last = result[-1][0]
            else:
                timestamp_first = 'NOT FOUND'
                timestamp_last = '-'

    context = {
        'result': number,
        'timestamp_first': timestamp_first,
        'timestamp_last': timestamp_last,
        'n': rowcount
    }

    return context


@route('/about')
@view('about')
def about():
    pass


@route('/impressum')
@view('impressum')
def impressum():
    pass


@route('/static/<filename:path>', no_i18n=True)
def send_static(filename):
    return static_file(filename, root=os.path.join(MOD_PATH, 'static'))


# findet templates im gleichen Verzeichnis
TEMPLATE_PATH.append(MOD_PATH)
app = default_app()
application = I18NPlugin(app, langs=LANGS, default_locale=DEFAULT_LOCALE,
                         domain='messages',
                         locale_dir=os.path.join(MOD_PATH, 'locales'))
