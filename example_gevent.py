from gevent import monkey
monkey.patch_all(thread=False, select=False)

from flask import Flask, render_template_string
from flask_stathat import StatHat


app = Flask(__name__)
app.config['STATHAT_EZ_KEY'] = 'STATHAT_EZ_KEY'
app.config['STATHAT_USE_GEVENT'] = True
app.config['STATHAT_GEVENT_POOL_SIZE'] = 10
stathat = StatHat()
stathat.init_app(app)  # or stathat = StatHat(app)


@app.route('/')
def index():
    return render_template_string("""
        <html><head><title>Flask-StatHat</title></head><body>
            <h1>Flask-StatHat</h1>
            <ol>
                <li><a href="{{ url_for('sample_gevent') }}">
                [stathat.count('sample_gevent', i) for i in range(10)]
                </a></li>
            </ol>
        </body></html>
        """)


@app.route('/sample_gevent')
def sample_gevent():
    [stathat.count('sample_gevent', i) for i in range(10)]
    return 'ok'


app.run()
