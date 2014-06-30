import urlparse

import requests
from requests_oauthlib import OAuth1

from secret import CLIENT_KEY, CLIENT_SECRET
from urls import *

def get_request_token():
    """ Get a token allowing us to request user authorization """
    oauth = OAuth1(CLIENT_KEY, client_secret=CLIENT_SECRET) # create oauth instance from the request_oathlib library. We pass in the the client key and secret from our secret.py file
    response = requests.post(REQUEST_TOKEN_URL,       # making POST request to the request token endpoint passing in the oauth object for credentials
                             auth=oauth)
    credentials = urlparse.parse_qs(response.content) # return item gets stored in response.content, us parse_ps function from urlparse module to create dict of token and secret

    request_token = credentials.get("oauth_token")[0]           # pull auth. token from dict and store
    request_secret = credentials.get("oauth_token_secret")[0]   # pull token secret from dict and store
    return request_token, request_secret

def get_user_authorization(request_token):
    """
    Redirect the user to authorize the client, and get them to give us the
    verification code.
    """
    authorize_url = AUTHORIZE_URL
    authorize_url = authorize_url.format(request_token=request_token) # auth url + request token => spec url to get PIN
    print 'Please go here and authorize: ' + authorize_url
    return raw_input('Please input the verifier: ')

def authorize():
	""" A complete OAuth authentication flow """
	request_token, request_secret = get_request_token()
	verifier = get_user_authorization(request_token)
	# print request_token, request_secret