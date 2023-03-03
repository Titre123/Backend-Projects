#!/usr/bin/env python3
'''
    Flask application
'''

from flask import Flask, render_template, request, g
from flask_babel import Babel
import pytz
import typing
from datetime import datetime


class Config:
    """Represents a Flask Babel configuration.
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


@babel.timezoneselector
def get_timezone():
    '''
        get the time zone and covert to the current time
    '''
    args = request.args.to_dict()
    date_dict = {
        "1": "Jan", "2": "Feb", "3": "Mar", "4": "Apr", "5": "May", "6": "Jun",
        "7": "Jul", "8": "Aug", "9": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"
    }
    if 'timezone' in args:
        try:
            date = datetime.now(pytz.timezone(args['timezone']))
            if date.hour > 12:
                return "{} {}, {}, {}:{}:{} PM".format(date_dict.get(str(date.month)), date.day, date.year,
            date.hour - 12, date.minute, date.second)
            return "{} {}, {}, {}:{}:{} AM".format(date_dict.get(str(date.month)), date.day, date.year,
            date.hour, date.minute, date.second)
        except pytz.exceptions.UnknownTimeZoneError:
            return 'Invalid timezone'
    if g.user:
        try:
            date = datetime.now(pytz.timezone(g.user.get('timezone')))
            if date.hour > 12:
                return "{} {}, {}, {}:{}:{} PM".format(date_dict.get(str(date.month)), date.day, date.year,
            date.hour - 12, date.minute, date.second)
            return "{} {}, {}, {}:{}:{} AM".format(date_dict.get(str(date.month)), date.day, date.year,
            date.hour, date.minute, date.second)
        except pytz.exceptions.UnknownTimeZoneError:
            return 'Invalid timezone'
    date = datetime.now(pytz.timezone(app.config['BABEL_DEFAULT_TIMEZONE']))
    if date.hour > 12:
        return "{} {}, {}, {}:{}:{} PM".format(date_dict.get(str(date.month)), date.day, date.year,
            date.hour - 12, date.minute, date.second)
        return "{} {}, {}, {}:{}:{} AM".format(date_dict.get(str(date.month)), date.day, date.year,
            date.hour, date.minute, date.second)



def get_user() -> typing.Dict:
    '''
        get user
    '''
    args = request.args.to_dict()
    if args.get('login_as') and users.get(int(args.get('login_as'))):
        return users.get(int(args.get('login_as')))
    else:
        return None


@app.before_request
def before_request():
    '''load before other functions'''
    user = get_user()
    if user is not None:
        g.user = user


@babel.localeselector
def get_locale():
    '''method to set language'''
    args = request.args.to_dict()
    head = request.headers.get('locale')
    if 'locale' in args and args.get('locale') in app.config['LANGUAGES']:
        return args['locale']
    if g.user and g.user.get('locale') in app.config['LANGUAGES']:
        return g.user.get('locale')
    if head and head in app.config['LANGUAGES']:
        return head
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def Home() -> str:
    '''Home route'''
    timezone = get_timezone()
    return render_template('./index.html', timezone=timezone)


if __name__ == "__main__":
    app.run('localhost', 3000, True)
