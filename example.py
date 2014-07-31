from flask import Flask
from flask_stathat import StatHat

app = Flask(__name__)
app.config['STATHAT_EZ_KEY'] = 'marksteve@insynchq.com'
stathat = StatHat(app)


@app.route('/count')
def count():
    stathat.count('test_count', 1)
    return "stathat.count('test_count', 1)"


@app.route('/value')
def value():
    stathat.value('test_value', 1)
    return "stathat.value('test_value', 1)"


@app.route('/multiple_stats')
def multiple_stats():
    stathat.count('test_count', 1)
    stathat.count('test_count', 1)
    stathat.count('test_count', 1)
    stathat.value('test_value', 3)
    return """stathat.count('test_count', 1)
stathat.count('test_count', 1)
stathat.count('test_count', 1)
stathat.value('test_value', 3)
"""


if __name__ == '__main__':
    app.run(debug=True)

