#!/usr/bin/env python3
'''
    Flask application
'''

from flask import Flask, render_template, request, g
from flask_babel import Babel
import pytz
import typing


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
    if 'locale' in args and args.get('locale') in app.config['LANGUAGES']:
        return args['locale']
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def Home() -> str:
    '''Home route'''
    return render_template('./5-index.html')


if __name__ == "__main__":
    app.run('localhost', 3000, True)
