#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    app.admin.forms
    ~~~~~~~~~~~~~~~~~~~~

    The module provides the forms for admin

    :copyright: (c) 2016 by zifeiyu.
    :license: MIT, see LICENSE for more details.
"""
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, TextField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email
from zifeiyu.constants import POST_STATUS
from wtforms.widgets import Select, TextArea, TextInput, HiddenInput
from zifeiyu.models import Column


class LoginForm(Form):
    '''The loginform for admin login'''
    email = StringField(('邮箱'), validators=[
        DataRequired(message=("邮箱必填")),
        Email(message=("无效的邮箱"))
    ])
    password = PasswordField(("密码"), validators=[
        DataRequired(message=("密码必填"))]
    )
    remember_me = BooleanField(("记住我"), default=False)

class PostForm(Form):
    """form for add Post"""
    title = TextField((u'标题'), validators=[
        DataRequired(message=(u"标题必填"))
    ])
    status = SelectField(u'状态', choices=POST_STATUS, option_widget=Select)
    column =  SelectField(u'栏目',option_widget=Select)
    tags = TextField((u'标签'))
    abstract = TextAreaField((u'摘要'),
        validators=[DataRequired(message=(u"摘要必填"))]
    )
    content = TextAreaField((u'内容'),
        validators=[DataRequired(message=(u"内容必填"))]
    )

    def generateColumnOption(self, options):
        # print options
        self.column.choices = options

class AddColumnForm(Form):
    """form for add Column"""
    label = TextField(('栏目名称'), validators=[
        DataRequired(message=("栏目名称必填"))
    ])

class AddTagForm(Form):
    """form for add Column"""
    label = TextField(('栏目名称'), validators=[
        DataRequired(message=("栏目名称必填"))
    ])