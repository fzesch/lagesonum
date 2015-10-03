# coding: utf-8

import os
import datetime
from babel.dates import format_datetime
from babel.core import Locale, UnknownLocaleError

from bottle import default_app, route, view, static_file, TEMPLATE_PATH, request, BaseTemplate, debug, hook
from peewee import IntegrityError, DoesNotExist, fn


from bottle_utils.i18n import I18NPlugin
from bottle_utils.i18n import lazy_gettext as _

from input_number import is_valid_number, parse_numbers, get_fingerprint
from models import BaseModel, Number, Place

debug(True)
# store database outside of repository so it is not overwritten by git pull
MOD_PATH = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.abspath(os.path.join(MOD_PATH, '../', '../', "lagesonr.db"))

model = BaseModel(database=DB_PATH)

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


@hook('before_request')
def _connect_db():
    model.connect()


@hook('after_request')
def _close_db():
    model.disconnect()


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

    # TODO make place variable, depending on current request
    q = Place.select().where(Place.place == 'LAGESO')
    lageso = q.get() if q.count() == 1 else None

    if not numbers:
        result_num.append(_('novalidnumbers'))
    else:
        for num in numbers:
            if is_valid_number(num):
                try:
                    n = Number.create(number=num.upper(), time=timestamp, place=lageso, fingerprint=usr_hash)
                    result_num.append(n.number)
                except IntegrityError:
                    try:
                        n = Number.get(Number.number == num.upper())
                        # FIXME Why ain't there any value placeholder in translation string?
                        result_num.append(_(u'erruniquenumber') + ': {}'.format(n.number))
                    except DoesNotExist:
                        result_num.append(u'Something weired happend with {}'.format(num))

    # FIXME result_num is horrible, as it contains success and failures, indistinguishable
    return {'entered': result_num, 'timestamp': timestamp.strftime('%x %X')}


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
    timestamps = []
    invalid_input = None

    if numbers:
        # FIXME WTF? Allow and parse a list and than pick one & silently drop the others?
        number = numbers[0]
        qry = Number.select(Number.time).where(Number.number ** number).order_by(Number.time)
        timestamps = [n.time for n in qry]
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
    # TODO move time delta and count to soem other location, e.g. configuration
    max_days = 21
    min_count = 3

    oldest_to_be_shown = datetime.datetime.combine(datetime.date.today() - datetime.timedelta(days=max_days),
                                                   datetime.datetime.min.time())
    # TODO optimize query, so we don't need to iterate manually, e.g. by selecing only count > min_count!
    # TODO make Place variable and part of WHERE
    numbers = Number.select(Number.number, Number.time, fn.Count(Number.number).alias('count')).\
        where(Number.time >= oldest_to_be_shown).group_by(Number.number).order_by(Number.time.desc(), Number.number)

    # filter numbers entered often enough
    # format numbers for later output
    display_output = sorted([{'num': n.number, 'count': int(n.count)}
                             for n in numbers if int(n.count) >= min_count][:18], key=lambda n: n['num'])

    since = format_datetime(oldest_to_be_shown, 'short', locale=request.locale)
    return {'numbers': display_output,
            'since': since,
            'min_count': min_count
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
