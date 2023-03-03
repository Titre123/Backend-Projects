#!/usr/bin/env python3
'''
    Flask application
'''

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def Home():
    '''Home route'''
    return render_template('./0-index.html')


if __name__ == "__main__":
    app.run('localhost', 3000, True)
