#/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    app.extensions
    ~~~~~~~~~~~~~~~~~~~~

    The extensions used in zifeiyu

    :copyright: (c) 2016 by zifeiyu.
    :license: MIT, see LICENSE for more details.
"""
from flask.ext.sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CsrfProtect
from flask.ext.cache import Cache
from flask_oauth import OAuth

# Database
db = SQLAlchemy()

# Login
login_manager = LoginManager()

# CSRF
csrf = CsrfProtect()

# Flask-Cache
cache = Cache(config={'CACHE_TYPE': 'simple'})

# Flask-oauth
oauth = OAuth()
weibo = oauth.remote_app('weibo',
                        base_url='https://api.weibo.com/oauth2/',
                        authorize_url='https://api.weibo.com/oauth2/authorize',
                        request_token_params={'redirect_uri': '127.0.0.1:5000'},
                        request_token_url=None,
                        access_token_url='https://api.weibo.com/oauth2/access_token',
                        access_token_params={'grant_type': 'authorization_code'},
                        consumer_key='1421334646',
                        consumer_secret='e10b836ccf233af0f95f1f851ba00782')