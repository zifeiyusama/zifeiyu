#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    app.admin
    ~~~~~~~~~~~~~~~~~~~~

    The init of admin module

    :copyright: (c) 2016 by zifeiyu.
    :license: MIT, see LICENSE for more details.
"""
from flask import Blueprint

admin = Blueprint(
    'admin',
    __name__,
    static_folder='static',
    template_folder='templates'
)
from zifeiyu.admin import views