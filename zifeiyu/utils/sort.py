#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    zifeiyu.utils.sort
    ~~~~~~~~~~~~~~~~~~~~

    sort data for jinja

    :copyright: (c) 2016 by zifeiyu.
    :license: Apache License 2.0, see LICENSE for more details.
"""


class MessageReplySorter(object):
    '''sort MessageReply'''

    def __init__(self, replies):
        self.replies = replies

    def sort(self):
        return sorted(self.replies, key=lambda x:x.created_date)
