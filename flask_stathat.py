from functools import wraps

from flask import g, request
import stathat


class StatHat(object):

    def __init__(self, app=None):
        if app:
            self.app = app
            self.init_app(app)
        else:
            self.app = None

    def init_app(self, app):
        STATHAT_EZ_KEY = app.config.get('STATHAT_EZ_KEY')
        if not STATHAT_EZ_KEY:
            raise KeyError("STATHAT_EZ_KEY not specified")
        # stathat.py
        self.stathat = stathat.StatHat(STATHAT_EZ_KEY)
        # Prep stathat counts and values on start of request
        app.before_request(self.before_request)
        # Send stathat requests at the end of the request
        app.teardown_request(self.teardown_request)
        # Don't send stats when in debug mode
        self.debug = app.config.get('DEBUG', False)

    def before_request(self):
        g._stathat_counts = []
        g._stathat_values = []

    def teardown_request(self, exception):
        # Send stathat requests only if there were no unhandled exceptions
        if exception:
            return
        # Don't send in debug mode
        if self.debug:
            return
        for stat, count in g._stathat_counts:
            self.stathat.count(stat, count)
        for stat, value in g._stathat_values:
            self.stathat.value(stat, value)

    def count(self, stat, count):
        g._stathat_counts.append((stat, count))

    def value(self, stat, value):
        g._stathat_values.append((stat, value))

    def count_pageview(self, func):
        @wraps(func)
        def decorated(*args, **kwargs):
            # Set path as stat name
            stat = request.script_root + request.path
            # Count pageview
            self.count(stat, 1)
            return func(*args, **kwargs)
        return decorated
