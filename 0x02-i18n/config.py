'''
    confoguration module in Babel to make our flask
    application support other languages
'''

import pytz


class Config(object):
    # ...
    LANGUAGES = ['en', 'fr']

    DEFAULT_LOCALE = 'en'

    TIMEZONE = pytz.utc