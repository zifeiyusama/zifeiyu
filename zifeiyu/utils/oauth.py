#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    zifeiyu.utils.oauth
    ~~~~~~~~~~~~~~~~~~~~

    Link to social websetie via oauth

    :copyright: (c) 2016 by zifeiyu.
    :license: MIT, see LICENSE for more details.
"""
import urllib, requests, json
from werkzeug import url_decode, url_encode, url_quote, \
     parse_options_header, Headers
from flask import session, redirect

WEIBO = {
    'name': 'weibo',
    'client_id': '1421334646',
    'client_secret': 'e10b836ccf233af0f95f1f851ba00782',
    'authorize_url': 'https://api.weibo.com/oauth2/authorize',
    'authorize_params': {
        'response_type': 'code'
    },
    'access_token_url': 'https://api.weibo.com/oauth2/access_token',
    'access_token_params': {
        'grant_type': 'authorization_code'
    }
}

def encode_request_data(data, format):
    if format is None:
        return data, None
    elif format == 'json':
        return json.dumps(data or {}), 'application/json'
    elif format == 'urlencoded':
        return url_encode(data or {}), 'application/x-www-form-urlencoded'
    raise TypeError('Unknown format %r' % format)

def add_query(url, args):
    if not args:
        return url
    return url + ('?' in url and '&' or '?') + url_encode(args)


class OAuthResponse(object):
    """Contains the response sent back from an OAuth protected remote
    application.
    """

    def __init__(self, resp, content):
        #: a :class:`~werkzeug.Headers` object with the response headers
        #: the application sent.
        self.headers = Headers(resp)
        #: the raw, unencoded content from the server
        self.raw_data = content
        #: the parsed content from the server
        self.data = json.loads(content)

    @property
    def status(self):
        """The status code of the response."""
        return self.headers.get('status', type=int)


class OAuthException(RuntimeError):
    """Raised if authorization fails for some reason."""
    message = None
    type = None

    def __init__(self, message, type=None, data=None):
        #: A helpful error message for debugging
        self.message = message
        #: A unique type for this exception if available.
        self.type = type
        #: If available, the parsed data from the remote API that can be
        #: used to pointpoint the error.
        self.data = data

    def __str__(self):
        return self.message.encode('utf-8')

    def __unicode__(self):
        return self.message


class Oauth(object):
    '''Oauth client
    :param name: then name of the remote application
    :param client_id: the application specific consumer key
    :param client_secret: the application specific consumer secret
    :param authorize_url: the URL for requesting new tokens
    :param access_token_url: the URL for token exchange
    :param authorize_params: an optional dictionary of parameters
                                 to forward to the request token URL
                                 or authorize URL depending on oauth
                                 version.
    :param access_token_params: an option diction of parameters to forward to
                                the access token URL
    '''
    def __init__(self):
        self.name = str(WEIBO['name'])
        self.client_id = str(WEIBO['client_id'])
        self.client_secret = str(WEIBO['client_secret'])
        self.authorize_url = WEIBO['authorize_url']
        self.access_token_url = WEIBO['access_token_url']
        self.authorize_params = WEIBO['authorize_params']
        self.access_token_params = WEIBO['access_token_params']
        self.access_token = None
        self.expires = 0.0

    def status_okay(self, resp):
        """Given request data, checks if the status is okay."""
        try:
            return int(resp['status']) in (200, 201)
        except ValueError:
            return False

    def get(self, url, data):
        """Sends a ``GET`` request.  Accepts the same parameters as
        :meth:`request`.
        """
        return self.request(url, data)

    def post(self, url, data, method):
        """Sends a ``POST`` request.  Accepts the same parameters as
        :meth:`request`.
        """
        return self.request(url, data, method='POST')

    def request(self, url, data="", headers=None, format='urlencoded', \
                method='GET', content_type=None):
        """Sends a request to the remote server with OAuth tokens attached.
        :param url: where to send the request to
        :param data: the data to be sent to the server.  If the request method
                     is ``GET`` the data is appended to the URL as query
                     parameters, otherwise encoded to `format` if the format
                     is given.  If a `content_type` is provided instead, the
                     data must be a string encoded for the given content
                     type and used as request body.
        :param headers: an optional dictionary of headers.
        :param format: the format for the `data`.  Can be `urlencoded` for
                       URL encoded data or `json` for JSON.
        :param method: the HTTP request method to use.
        :param content_type: an optional content type.  If a content type is
                             provided, the data is passed as it and the
                             `format` parameter is ignored.
        :return: an :class:`OAuthResponse` object.
        """
        headers = dict(headers or {})
        if method == 'GET':
            assert format == 'urlencoded'
            if data:
                url = add_query(url, data)
                data = ""
            return OAuthResponse(requests.get(url))
        else:
            if content_type is None:
                print 'data is %' % data
                data, content_type = encode_request_data(data, format)
            if content_type is not None:
                headers['Content-Type'] = content_type
            return OAuthResponse(requests.post(url, body=data, headers=headers))

    def authorize(self, callback=None):
        """Returns a redirect response to the remote authorization URL with
        the signed callback given. It's an URL on the system that has to be
        decorated as :meth:`authorized_handler`.
        """
        assert callback is not None, 'Callback is required OAuth2'
        # Since we need the
        # callback for the access_token_url we need to keep it in the
        # session.
        params = dict(self.authorize_params)
        params['redirect_uri'] = callback
        params['client_id'] = self.client_id
        session[self.name + '_oauthredir'] = callback
        url = add_query(self.authorize_url, params)
        return redirect(url)

    def tokengetter(self, f):
        """Registers a function as tokengetter.  The tokengetter has to return
        a tuple of ``(token, secret)`` with the user's token and token secret.
        If the data is unavailable, the function must return `None`.
        If the `token` parameter is passed to the request function it's
        forwarded to the tokengetter function::
            @oauth.tokengetter
            def get_token(token='user'):
                if token == 'user':
                    return find_the_user_token()
                elif token == 'app':
                    return find_the_app_token()
                raise RuntimeError('invalid token')
        """
        self.tokengetter_func = f
        return f

    def handle_oauth2_response(self, code):
        """Handles an oauth2 authorization response.  The return value of
        this method is forwarded as first argument to the handling view
        function.
        """
        remote_args = {
            'code':             code,
            'client_id':        self.client_id,
            'client_secret':    self.client_secret,
            'redirect_uri':     session.get(self.name + '_oauthredir')
        }
        remote_args.update(self.access_token_params)
        resp = self.post(self.access_token_url, remote_args)
        if not self.status_okay(resp.headers):
            raise OAuthException('Invalid response from ' + self.name,
                                 type='invalid_response', data=remote_args)
        return resp.data

    def authorized_handler(self, request):
        """Injects additional authorization functionality into the function.
        The function will be passed the response object as first argument
        if the request was allowed, or `None` if access was denied.  When the
        authorized handler is called, the temporary issued tokens are already
        destroyed.
        """
        if 'code' in request.args:
            data = self.handle_oauth2_response(request.args.get('code'))
            self.free_request_token()
            return data
        else:
            return None

    def free_request_token(self):
        session.pop(self.name + '_oauthtok', None)
        session.pop(self.name + '_oauthredir', None)