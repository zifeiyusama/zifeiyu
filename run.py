#!/usr/bin/env ptyhon
# -*- coding:utf-8 -*-
"""
    run
    ~~~~~~~~~~~~~~~~~~~~
    run app

    :copyright: (c) 2016 by zifeiyu.
    :license: MIT, see LICENSE for more details.
"""
from zifeiyu import create_app

app = create_app()

if __name__ == '__main__':
    app.run()