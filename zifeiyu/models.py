#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    zifeiyu.models
    ~~~~~~~~~~~~~~~~~~~~

    The module provides the models for admin

    :copyright: (c) 2016 by zifeiyu.
    :license: MIT, see LICENSE for more details.
"""
from zifeiyu.constants import ADMIN_ID, EMAIL, PASSWORD_HASH, NICKNAME
from flask_login import UserMixin
from datetime import datetime
from zifeiyu.extensions import db
from zifeiyu.constants import POST_STATUS
import uuid
from zifeiyu.utils.encryption import generate_SHA1
from sqlalchemy.ext.hybrid import hybrid_property


class Admin(UserMixin):

    def __init__(self):
        self.__id = ADMIN_ID
        self.__nickname = NICKNAME
        self.__email = EMAIL
        self.__password_hash = PASSWORD_HASH

    @classmethod
    def authenticate(cls, email, password):
        admin = Admin()
        authenticate = False
        if email == EMAIL and generate_SHA1(password) == PASSWORD_HASH:
            authenticate = True
        return admin, authenticate

    def get_id(self):
        return self.__id

    def __unicode__(self):
        return self.__nickname

tags = db.Table('tags',
                db.Column('tag_id', db.String(50), db.ForeignKey('tag.id')),
                db.Column('post_id', db.String(50), db.ForeignKey('post.id'))
                )


class Tag(db.Model):

    __tablename__='tag'
    id = db.Column(db.String(50), primary_key=True)

    def __init__(self, tag):
        self.id = tag

    @hybrid_property
    def post_num(self):
        return len(self.posts)


class Post(db.Model):

    __tablename__ = 'post'
    id = db.Column(db.String(50), primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    abstract = db.Column(db.Text)
    status = db.Column(db.String(10), default=dict(POST_STATUS)['DRAFT'])
    archive_id = db.Column(db.String(50), db.ForeignKey('archive.id'))
    column_id = db.Column(db.String(50), db.ForeignKey('column.id'))
    tags = db.relationship('Tag', secondary=tags, backref=db.backref('posts'))
    created_date = db.Column(db.DateTime)
    updated_date = db.Column(db.DateTime)
    publish_date = db.Column(db.DateTime)
    deleted_date = db.Column(db.DateTime)

    def __init__(self):
        pass

    @hybrid_property
    def local_created_date(self):
        return self.created_date.strftime("%Y-%m-%dT%H:%M:%S Z")

    @hybrid_property
    def local_updated_date(self):
        return self.updated_date.strftime("%Y-%m-%dT%H:%M:%S Z")

    @hybrid_property
    def local_publish_date(self):
        return self.publish_date.strftime("%Y-%m-%dT%H:%M:%S Z")

    def save(self, tag_list):
        self.updated_date = datetime.utcnow()
        # set post status
        statuses = dict(POST_STATUS)
        if self.status == statuses['PUBLISHED']:
            self.publish_date = datetime.utcnow()
        elif self.status == statuses['DELETED']:
            self.deleted_date = datetime.utcnow()

        # insert post
        if self.id is None:
            u = uuid.uuid1()
            self.id = str(uuid.uuid5(u, 'post'))
            self.created_date = datetime.utcnow()
            archive = Archive(datetime.now())
            db.session.merge(archive)
            # archive_id = datetime.now().strftime("%Y-%m")
            # archive = Archive.query.filter(Archive.id == archive_id).first()
            # if archive is None:
            #     # TODO: test
            #     archive = Archive(datetime.now())
            #     db.session.add(archive)
            #     db.session.commit()
            self.archive_id = archive.id
        self.updated_date = datetime.utcnow()
        if len(tag_list) > 0:
            post_tags_id = [t.id for t in self.tags]
            for tag in tag_list:
                if tag.id not in post_tags_id:
                    self.tags.append(tag)
        db.session.add(self)
        db.session.commit()


class Archive(db.Model):

    __tabname__ = 'archive'
    id = db.Column(db.String(50), primary_key=True)
    label = db.Column(db.String(15))
    posts = db.relationship('Post', backref="archive")
    created_date = db.Column(db.DateTime)
    updated_date = db.Column(db.DateTime)
    deleted_date = db.Column(db.DateTime)

    def __init__(self, archive_time):
        self.id = archive_time.strftime("%Y-%m")
        self.label = str(archive_time.year) + u"年" + \
            str(archive_time.month) + u"月"

    @hybrid_property
    def post_num(self):
        return len(self.posts)

    def save(self, label, operation):
        if self.id is None and operation == 'insert':
            self.created_date = datetime.utcnow()
        elif self.id is not None and operation == 'update':
            self.updated_date = datetime.utcnow()
        else:
            return False
        self.label = label
        db.session.add(self)
        db.session.commit()
        return True


class Column(db.Model):

    __tablename__ = 'column'
    id = db.Column(db.String(50), primary_key=True)
    posts = db.relationship('Post', backref="column")
    label = db.Column(db.String(15))
    created_date = db.Column(db.DateTime)
    updated_date = db.Column(db.DateTime)
    deleted_date = db.Column(db.DateTime)

    def __init__(self):
        pass

    @hybrid_property
    def post_num(self):
        return len(self.posts)

    @hybrid_property
    def local_created_date(self):
        return self.created_date.strftime("%Y-%m-%dT%H:%M:%S Z")

    @hybrid_property
    def local_updated_date(self):
        return self.updated_date.strftime("%Y-%m-%dT%H:%M:%S Z")

    @classmethod
    def getColumnList(self):
        choices = [(u'', u'未选择')]
        for k, v in db.session.query(Column.id, Column.label).all():
            choices.append((k, v))
        return choices

    def save(self, operation):
        if self.id is None and operation == 'insert':
            u = uuid.uuid1()
            self.id = str(uuid.uuid5(u, 'column'))
            self.created_date = datetime.utcnow()
        elif self.id is None and operation != 'update':
            return False
        self.updated_date = datetime.utcnow()
        db.session.add(self)
        db.session.commit()
        return True

class Weibo(db.Model):

    __tablename__ = 'weibo'
    id = db.Column(db.String(100), primary_key=True)
    access_token = db.Column(db.String(100))
    screen_name = db.Column(db.String(100))
    expires = db.Column(db.Float)
    authenticate_date = db.Column(db.DateTime)
    profile_image_url = db.Column(db.String(150))
    created_date = db.Column(db.DateTime)
    updated_date = db.Column(db.DateTime)
    messages = db.relationship('Message', backref="weibo")
    message_replies = db.relationship('MessageRelpy', backref="weibo")

    def __init__(self, id, access_token, expires, screen_name, profile_image_url):
        self.id = id
        self.access_token = access_token
        self.expires = expires
        self.screen_name = screen_name
        self.profile_image_url = profile_image_url

    def save(self):
        db.session.add(self)
        db.session.commit()

class Message(db.Model):

    __tablename__ = 'message'
    id = db.Column(db.String(100), primary_key=True)
    created_date = db.Column(db.DateTime)
    content = db.Column(db.String(130))
    replies = db.relationship('MessageRelpy', backref="message")
    weibo_id = db.Column(db.String(100), db.ForeignKey('weibo.id'))
    is_deleted = db.Column(db.Boolean)

    def __init__(self, content, weibo_id=None, message_id=None):
        self.content = content
        self.weibo_id = weibo_id
        self.message_id = message_id

    def save(self):
        u = uuid.uuid1()
        self.id = str(uuid.uuid5(u, 'message'))
        self.created_date = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    @hybrid_property
    def reply_num(self):
        return len(self.replies)

class MessageRelpy(db.Model):

    __tablename__ = 'message_reply'
    id = db.Column(db.String(100), primary_key=True)
    created_date = db.Column(db.DateTime)
    content = db.Column(db.String(130))
    message_id = db.Column(db.String(100), db.ForeignKey('message.id'))
    reply_id = db.Column(db.String(100), db.ForeignKey('message_reply.id'))
    weibo_id = db.Column(db.String(100), db.ForeignKey('weibo.id'))
    is_from_admin = db.Column(db.Boolean)
    is_deleted = db.Column(db.Boolean)

    def __init__(self, content, weibo_id=None, message_id=None):
        self.content = content

    def save(self):
        u = uuid.uuid1()
        self.id = str(uuid.uuid5(u, 'message_reply'))
        self.created_date = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

