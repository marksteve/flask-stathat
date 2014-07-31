from flask import g, json

try:
    import grequests as requests
    use_grequests = True
except ImportError:
    import requests
    use_grequests = False


class StatHat(object):

    url = 'https://api.stathat.com/ez'

    def __init__(self, app=None):
        if app:
            self.app = app
            self.init_app(app)
        else:
            self.app = None

    def init_app(self, app):
        self.ez_key = app.config.get('STATHAT_EZ_KEY')
        if not self.ez_key:
            raise KeyError("STATHAT_EZ_KEY not specified")

        # Initial requests session
        self.session = requests.Session()
        self.session.headers.update({'Content-Type': 'application/json'})

        # Prep stathat counts and values on start of request
        app.before_request(self.before_request)

        # Send stathat requests at the end of the request
        app.teardown_request(self.teardown_request)

    def before_request(self):
        g._stathat_data = []

    def teardown_request(self, exception):
        # Send stathat requests only if there were no unhandled exceptions
        if exception:
            return
        data = getattr(g, '_stathat_data', None)
        if not data:
            return
        # Send stathat requests
        req = dict(
            ezkey=self.ez_key,
            data=data,
        )
        if use_grequests:
            requests.send(requests.post(
                self.url,
                data=json.dumps(req),
                session=self.session,
            ))
        else:
            self.session.post(self.url, data=json.dumps(req))

    def count(self, stat, count):
        g._stathat_data.append(dict(stat=stat, count=count))

    def value(self, stat, value):
        g._stathat_data.append(dict(stat=stat, value=value))

