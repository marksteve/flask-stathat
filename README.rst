.. image:: http://i.imgur.com/YuqGF.png

=============
Flask-StatHat
=============

.. image:: http://img.shields.io/pypi/v/Flask-StatHat.png

`StatHat <https://www.stathat.com>`_ extension for `Flask <http://flask.pocoo.org>`_

-------
Install
-------
::
    
    python
    pip install Flask-StatHat
    
-----
Setup
-----
::

    from flask_stathat import StatHat
    stathat = StatHat()
    stathat.init_app(app)  # or stathat = StatHat(app)


-----
Usage
-----
::

    @app.route('/')
    def index():
        stathat.count('some_stat', 1)
        stathat.value('some_value', 9001)
        # The stathat requests won't be sent until the flask request
        # has been processed and no exceptions were raised
        ...
    
    @app.route('/signup')
    @stathat.count_pageview
    def signup():
        # Sends a count with the request path as stat name
        ...



-------------
Configuration
-------------
::

    app.config.update(STATHAT_EZ_KEY='STAHAT_EZ_KEY',
                      STATHAT_USE_GEVENT=True,
                      STATHAT_GEVENT_POOL_SIZE=10)

-------
License
-------
http://marksteve.mit-license.org
