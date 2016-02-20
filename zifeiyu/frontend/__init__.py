#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    zifeiyu.frontend
    ~~~~~~~~~~~~~~~~~~~~

    The init of frontend module

    :copyright: (c) 2016 by zifeiyu.
    :license: MIT, see LICENSE for more details.
"""
from flask import Blueprint

frontend = Blueprint(
    'frontend',
    __name__,
    static_folder='static',
    template_folder='templates'
)
from zifeiyu.frontend import views