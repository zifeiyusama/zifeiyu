#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    app.frontend.forms
    ~~~~~~~~~~~~~~~~~~~~

    The module provides the forms for frontend

    :copyright: (c) 2016 by zifeiyu.
    :license: MIT, see LICENSE for more details.
"""
from flask_wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired


class MessageForm(Form):
    '''Forms for Message'''
    content = TextAreaField((u'内容'),
        validators=[DataRequired(message=(u"内容必填"))]
    )
    weibo_id = StringField((u'用户'))

class MessageReplyForm(Form):
    '''Forms for MessageReply'''
    content = TextAreaField((u'内容'),
        validators=[DataRequired(message=(u"内容必填"))]
    )
    weibo_id = StringField((u'用户'))
    message_id = StringField((u'留言'))
    reply_id = StringField((u'回复'))
