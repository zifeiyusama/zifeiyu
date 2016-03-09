#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    zifeiyu.frontend.views
    ~~~~~~~~~~~~~~~~~~~~

    The module provides the views for entry

    :copyright: (c) 2016 by zifeiyu.
    :license: MIT, see LICENSE for more details.
"""
from zifeiyu.models import Post, Column, Archive, Tag
from . import frontend
from flask import redirect, render_template, request, current_app, url_for
from flask.ext.sqlalchemy import Pagination
from zifeiyu.constants import POSTS_PER_PAGE
from zifeiyu.extensions import weibo


@frontend.route('/')
@frontend.route('/index')
@frontend.route('/index/<int:page>')
def index(page=1):
    posts = Post.query.paginate(page, POSTS_PER_PAGE, False)
    return render_template('frontend/index.html', posts=posts, page_url='frontend.index')

@frontend.route('/column/<column_id>/<int:page>')
@frontend.route('/column/<column_id>')
def column(column_id,page=1):
    posts = Post.query.filter_by(column_id=column_id).paginate(page, POSTS_PER_PAGE, False)
    return render_template('frontend/index.html', posts=posts, column_id=column_id)

@frontend.route('/column/<archive_id>/<int:page>')
@frontend.route('/archive/<archive_id>')
def archive(archive_id,page=1):
    posts = Post.query.filter_by(archive_id=archive_id).paginate(page, POSTS_PER_PAGE, False)
    return render_template('frontend/index.html', posts=posts, archive_id=archive_id)


@frontend.route('/post/<post_id>')
def post(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    return render_template('frontend/post.html', post=post)

@frontend.route('/message', methods=['GET','POST'])
def message():
    return render_template('frontend/message.html')

@frontend.route('/about', methods=['GET','POST'])
def about():
    return render_template('frontend/about.html')

@frontend.route('/login')
def login():
    return weibo.authorize(callback='http://zifeiyu.herokuapp.com/frontend/oauth-authorized',
                           next=request.args.get('next') or request.referrer or None)

@frontend.route('/oauth-authorized')
@weibo.authorized_handler
def oauth_authorized(resp):
    next_url = request.args.get('next')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)

    access_token = resp['access_token']
    expires_in = resp['expires_in']
    print 'access token is %s' % access_token
    print 'expires_in is %s' % expires_in
    session['access_token'] = access_token, ''
    return redirect(url_for('index'))
    return redirect(next_url)

@weibo.tokengetter
def get_access_token():
    return session.get('access_token')

@frontend.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(current_app.root_path, 'static/img'),'favicon.ico', mimetype='image/vnd.microsoft.icon')