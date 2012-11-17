from random import random

from flask import Flask, render_template_string
from flask_stathat import StatHat


app = Flask(__name__)
app.config['STATHAT_EZ_KEY'] = 'STATHAT_EZ_KEY'
stathat = StatHat()
stathat.init_app(app)  # or stathat = StatHat(app)


@app.route('/')
def index():
    return render_template_string("""
        <html><head><title>Flask-StatHat</title></head><body>
            <h1>Flask-StatHat</h1>
            <ol>
                <li><a href="{{ url_for('sample_count') }}">stathat.count('sample_count', 5)</a></li>
                <li><a href="{{ url_for('sample_value') }}">stathat.value('sample_value', random())</a></li>
                <li><a href="{{ url_for('sample_exception') }}">stathat.count('sample_exception', 5)</a></li>
                <li><a href="{{ url_for('sample_count_pageview') }}">@stathat.count_pageview</a></li>
            </ol>
        </body></html>
        """)


@app.route('/sample_count')
def sample_count():
    stathat.count('sample_count', 5)
    return 'ok'


@app.route('/sample_value')
def sample_value():
    stathat.value('sample_value', random())
    return 'ok'


@app.route('/sample_exception')
def sample_exception():
    stathat.count('sample_exception', 5)
    0 / 0
    return 'ok'


@app.route('/sample_count_pageview')
@stathat.count_pageview
def sample_count_pageview():
    return 'ok'


app.run()
