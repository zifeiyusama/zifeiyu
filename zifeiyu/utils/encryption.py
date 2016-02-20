#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    zifeiyu.utils.encription
    ~~~~~~~~~~~~~~~~~~~~

    SHA1 encription utility

    :copyright: (c) 2016 by zifeiyu.
    :license: Apache License 2.0, see LICENSE for more details.
"""
import hashlib

def generate_SHA1(para):
    return hashlib.sha1(para).hexdigest()