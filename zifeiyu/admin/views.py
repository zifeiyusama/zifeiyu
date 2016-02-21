#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    app.admin.views
    ~~~~~~~~~~~~~~~~~~~~

    The module provides the views for admin

    :copyright: (c) 2016 by zifeiyu.
    :license: MIT, see LICENSE for more details.
"""
from flask_login import current_user, login_required, logout_user, login_user, fresh_login_required
from . import admin
from .forms import LoginForm, PostForm, AddColumnForm
from zifeiyu.models import Admin
from flask import redirect, url_for, render_template, request, flash
from zifeiyu.models import Post, Column, Archive, Tag
from zifeiyu.extensions import db
from zifeiyu.extensions import csrf
from zifeiyu.utils.markdown import MDconverter


@admin.route('/login', methods=['GET', 'POST'])
def login():
    '''let the admin login'''
    if current_user is not None and current_user.is_authenticated:
        return redirect(url_for("admin.index"))
    form = LoginForm()
    # validate data
    if form.validate_on_submit():
        # authenticate admin
        admin, authenticated = Admin.authenticate(form.email.data,
                                                  form.password.data)
        if authenticated:
            login_user(admin, remember=form.remember_me.data)
            # valid redirect url
            next = request.args.get('next')
            return redirect(next or url_for('admin.index'))
        flash((u"帐号密码错误"), u"danger")
    return render_template('admin/login.html', form=form)

@admin.route('/index', methods=["POST", "GET"])
@admin.route('/', methods=["POST", "GET"])
@login_required
@fresh_login_required
def index():
    return render_template('admin/index.html')

@admin.route('/post')
@login_required
@fresh_login_required
def post():
    posts = Post.query.all()
    return render_template('admin/post.html', posts = posts)

@admin.route('/add_post', methods=["POST", "GET"])
@login_required
@fresh_login_required
def add_post():
    form = PostForm()
    form.generateColumnOption(Column.getColumnList())
    print form.tags.data
    if form.validate_on_submit():
        post = Post()
        post.title = form.title.data
        post.content = form.content.data
        post.abstract = form.abstract.data
        post.status = form.status.data
        post.column_id = form.column.data
        tag_list = []
        tag_value = form.tags.data.decode('utf-8')
        if tag_value != '':
            tag_list = [ Tag(tag) for tag in tag_value.split(',')]
        post.save(tag_list)
        return redirect(url_for('admin.post'))
    return render_template('admin/add_post.html', form=form, edit_post_id=None)



@admin.route('/post/<post_id>', methods=["POST", "GET"])
@login_required
@fresh_login_required
def edit_post(post_id):
    form = PostForm()
    form.generateColumnOption(Column.getColumnList())
    post = Post.query.filter_by(id=post_id).first_or_404()
    if request.method == 'GET':
        form.title.data = post.title
        form.status.data =  post.status
        form.content.data = post.content
        form.abstract.data = post.abstract
        form.column.data = post.column_id
        if len(post.tags) >0:
            form.tags.data = ','.join([tag.id.encode('utf-8') for tag in post.tags])
        print form.tags.data
    elif form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.status = form.status.data
        post.abstract = form.abstract.data
        post.column_id = form.column.data
        tag_list = []
        tag_value = form.tags.data.decode('utf-8')
        if tag_value != '':
            tag_list = [ Tag(tag) for tag in form.tags.data.decode('utf-8').split(',')]
        post.save(tag_list)
        return redirect(url_for('admin.post'))
    return render_template('admin/add_post.html', form=form, edit_post_id=post_id)

@admin.route('delete_post', methods=['POST'])
@login_required
@fresh_login_required
def delete_post():
    try:
        jsonstring = request.get_json(force=True)
        columns = Post.query.filter(Post.id.in_(jsonstring['ids'])).delete(synchronize_session=False)
        db.session.commit()
    except:
        return 'false'
    return 'true'

@admin.route('/add_column', methods=["POST"])
@login_required
@fresh_login_required
def add_column():
    form = AddColumnForm()
    if form.validate_on_submit():
        column = Column()
        column.label = form.label.data
        if column.save('insert'):
            flash((u"插入成功"), "success")
        else:
            flash((u"插入失败"), "danger")
    return redirect(url_for("admin.column"))

@admin.route('/delete_column', methods=["POST"])
@login_required
@fresh_login_required
def delete_column():
    try:
        jsonstring = request.get_json(force=True)
        columns = Column.query.filter(Column.id.in_(jsonstring['ids'])).delete(synchronize_session=False)
        db.session.commit()
    except:
        return 'false'
    return 'true'

@admin.route('/column', methods=["GET"])
@login_required
@fresh_login_required
def column():
    form = AddColumnForm()
    columns = Column.query.all()
    return render_template('admin/column.html', form=form, columns = columns)

@admin.route('/archive')
@login_required
@fresh_login_required
def archive():
    archives = Archive.query.all()
    return render_template('admin/archive.html', archives=archives)

@admin.route('/tag')
@login_required
@fresh_login_required
def tag():
    tags = Tag.query.all()
    return render_template('admin/tag.html', tags=tags)

@admin.route('/message')
@login_required
@fresh_login_required
def message():
    return render_template('admin/message.html')

