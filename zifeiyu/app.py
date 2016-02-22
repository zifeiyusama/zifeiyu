#/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    zifeiyu.app
    ~~~~~~~~~~~~~~~~~~~~
    manages the app creation and configuration process

    :copyright: (c) 2016 by zifeiyu.
    :license: MIT, see LICENSE for more details.
"""
from flask import Flask, url_for, redirect
from zifeiyu.extensions import csrf, db, login_manager, cache
from .admin import admin
from .frontend import frontend
from .models import Admin, Archive, Column, Tag
from zifeiyu.utils.momentjs import momentjs
from zifeiyu.utils.markdown import MDconverter, MDSetter
from zifeiyu.constants import POST_STATUS
from jinja2 import environmentfilter
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def index():
    return redirect(url_for('frontend.index'))

def create_app(config=None):
    """Creates the app."""

    # Initialize the app
    app = Flask(__name__)
    # Configure app
    app.config.from_object('config')

    configure_extensions(app)
    configure_blueprints(app)
    app.jinja_env.globals['momentjs'] = momentjs
    app.jinja_env.globals['MDconverter'] = MDconverter
    app.jinja_env.globals['MDSetter'] = MDSetter
    configure_context_processors(app)
    with app.app_context():
        app.add_url_rule('/', view_func=index)
    configure_custom_filter(app)
    return app

def configure_blueprints(app):
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(frontend, url_prefix='/frontend')

def configure_extensions(app):
    """Configures the extensions."""

    # Flask-SQLAlchemy
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Flask-WTF CSRF
    csrf.init_app(app)

    # Flask-Login
    login_manager.login_view = 'admin.login'
    # login_manager.login_message = u'跳转至登录页面...'
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_admin(admin_id):
        """Loads the admin. Required by the `login` extension."""

        admin_instance = Admin()
        if admin_id == admin_instance.get_id():
            return admin_instance
        else:
            return None

    #Flask-Cache
    cache.init_app(app)


def configure_context_processors(app):

    @app.context_processor
    @cache.cached(timeout=50, key_prefix='archives')
    def archives():
        archives = Archive.query.all()
        return dict(archives=archives)

    @app.context_processor
    @cache.cached(timeout=50, key_prefix='columns')
    def columns():
        columns = Column.query.all()
        return dict(columns=columns)

    @app.context_processor
    @cache.cached(timeout=50, key_prefix='tags')
    def tags():
        tags = Tag.query.all()
        return dict(tags=tags)

def configure_custom_filter(app):

    @app.template_filter('post_status_format')
    def post_status_format(key):
        post_status = dict(POST_STATUS)
        return post_status[key]