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

# Database
db = SQLAlchemy()

# Login
login_manager = LoginManager()

# CSRF
csrf = CsrfProtect()

# Flask-Cache

cache = Cache(config={'CACHE_TYPE': 'simple'})