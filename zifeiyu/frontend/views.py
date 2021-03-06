#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    zifeiyu.frontend.views
    ~~~~~~~~~~~~~~~~~~~~

    The module provides the views for entry

    :copyright: (c) 2016 by zifeiyu.
    :license: MIT, see LICENSE for more details.
"""
from zifeiyu.models import Post, Column, Archive, Tag, Message, MessageRelpy, Weibo
from . import frontend
from flask import redirect, render_template, request, current_app, url_for, session
from flask.ext.sqlalchemy import Pagination
from zifeiyu.constants import POSTS_PER_PAGE
from zifeiyu.utils.oauth import Oauth
from zifeiyu.frontend.forms import MessageForm, MessageReplyForm
import json

weibo = Oauth()


@frontend.route('/login')
def login():
    # callback = 'http://zifeiyu.herokuapp.com/frontend/index'
    callback = url_for('frontend.oauth_authorized',
        next=request.args.get('next') or request.referrer or None, _external=True)
    return weibo.authorize(callback=callback)

@frontend.route('/logout')
def logout(next_url=None):
    session.pop('weibo_token', None)
    session.pop('weibo_id', None)
    session.pop('screen_name', None)
    session.pop('expires_in', None)
    session.pop('uid', None)
    session.pop('profile_image_url', None)
    if next_url is None:
        next_url = url_for('frontend.index')
    return redirect(next_url)

@frontend.route('/oauth_authorized')
def oauth_authorized():
    resp = weibo.authorized_handler(request)
    next_url = request.args.get('next') or url_for('index')
    if resp is None:
        return redirect(next_url)
    resp_json = resp
    session['weibo_token'] = resp_json['access_token']
    session['expires_in'] = resp_json['expires_in']
    session['uid'] = resp_json['uid']
    user_resp = weibo.get('https://api.weibo.com/2/users/show.json', {'uid':session['uid']})
    if user_resp.status == 200:
        user = user_resp.data
        session['weibo_id'] = user['id']
        session['screen_name'] = user['screen_name']
        session['profile_image_url'] = user['profile_image_url']
        weibo_user = Weibo(session['weibo_id'], session['weibo_token'], \
                           session['expires_in'], session['screen_name'], session['profile_image_url'])
        weibo_user.save()
    return redirect(next_url)

@frontend.route('/')
@frontend.route('/index')
@frontend.route('/index/<int:page>')
def index(page=1):
    posts = Post.query.filter_by(status='PUBLISHED').paginate(page, POSTS_PER_PAGE, False)
    return render_template('frontend/index.html', posts=posts)

@frontend.route('/column/<column_id>/<int:page>')
@frontend.route('/column/<column_id>')
def column(column_id,page=1):
    posts = Post.query.filter_by(column_id=column_id, status='PUBLISHED').paginate(page, POSTS_PER_PAGE, False)
    return render_template('frontend/index.html', posts=posts, column_id=column_id)

@frontend.route('/archive/<archive_id>/<int:page>')
@frontend.route('/archive/<archive_id>')
def archive(archive_id,page=1):
    posts = Post.query.filter_by(archive_id=archive_id, status='PUBLISHED').paginate(page, POSTS_PER_PAGE, False)
    return render_template('frontend/index.html', posts=posts, archive_id=archive_id)

@frontend.route('/tag/<tag_id>/<int:page>')
@frontend.route('/tag/<tag_id>')
def tag(tag_id,page=1):
    posts = Post.query.filter(Post.tags.any(Tag.id == tag_id), Post.status=='PUBLISHED').paginate(page, POSTS_PER_PAGE, False)
    return render_template('frontend/index.html', posts=posts, tag_id=tag_id)

@frontend.route('/post/<post_id>')
def post(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    return render_template('frontend/post.html', post=post)

@frontend.route('/message', methods=['GET','POST'])
def message():
    message_form = MessageForm()
    reply_form = MessageReplyForm()
    messages = Message.query.order_by(Message.created_date).all()
    return render_template('frontend/message.html', message_form=message_form, reply_form=reply_form, messages=messages)

@frontend.route('/add_message', methods=['POST'])
def add_message():
    form = MessageForm()
    if form.validate_on_submit():
        message = Message(form.content.data)
        # message.weibo_id = '123456'
        message.weibo_id = session['weibo_id']
        message.save()
    return redirect(url_for('frontend.message'))

@frontend.route('/add_reply', methods=['POST'])
def add_reply():
    form = MessageReplyForm()
    if form.validate_on_submit():
        reply = MessageRelpy(form.content.data)
        # reply.weibo_id = '123456'
        message_id = form.message_id.data
        if len(message_id) > 10:
            reply.message_id = message_id
        reply_id = form.reply_id.data
        if len(reply_id) > 10:
            reply.reply_id = reply_id
        reply.weibo_id = session['weibo_id']
        reply.save()
    return redirect(url_for('frontend.message'))


@frontend.route('/about', methods=['GET','POST'])
def about():
    return render_template('frontend/about.html')

@frontend.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(current_app.root_path, 'static/img'),'favicon.ico', mimetype='image/vnd.microsoft.icon')

@weibo.tokengetter
def get_weibo_token():
    return session.get('weibo_token')