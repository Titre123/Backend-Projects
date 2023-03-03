#!/usr/bin/env python3
'''
    Flask application
'''

from flask import Flask, render_template, request
from flask_babel import Babel
import pytz


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


@app.route('/')
def Home():
    '''Home route'''
    return render_template('./2-index.html')


@babel.localeselector
def get_locale():
    '''method to set language'''
    return request.accept_languages.best_match(['en', 'fr'])


if __name__ == "__main__":
    app.run('localhost', 3000, True)
