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
        ez_key = app.config.get('STATHAT_EZ_KEY')
        if not ez_key:
            raise KeyError("STATHAT_EZ_KEY not specified")

        # stathat.py
        self.stathat = stathat.StatHat(ez_key)

        # Setup gevent if set to be used
        self.use_gevent = app.config.get('STATHAT_USE_GEVENT', False)
        if self.use_gevent:
            pool_size = app.config.get('STATHAT_GEVENT_POOL_SIZE', 2)
            from gevent.pool import Pool
            self.pool = Pool(pool_size)

        # Prep stathat counts and values on start of request
        app.before_request(self.before_request)

        # Send stathat requests at the end of the request
        app.teardown_request(self.teardown_request)

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
        # Send stathat requests
        for values, action in ((g._stathat_counts, self.stathat.count),
                               (g._stathat_values, self.stathat.value)):
            for stat, value in values:
                if self.use_gevent:
                    self.pool.spawn(action, stat, value)
                else:
                    action(stat, value)

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
