# coding=utf-8
"""
创建 access_token
"""

import os
from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session

# 不需要 https
if 'OAUTHLIB_INSECURE_TRANSPORT' not in os.environ:
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

client_id = os.getenv('CLIENT_ID', '')
client_secret = os.getenv('CLIENT_SECRET', '')

port = int(os.getenv('FLASK_RUN_PORT', 5000))
username = 'admin'
password = 'admin'

url = f'http://127.0.0.1:{port}/oauth/token'

oauth = OAuth2Session(client=LegacyApplicationClient(client_id=client_id))
token = oauth.fetch_token(token_url=url,
                          username=username, password=password,
                          client_id=client_id, client_secret=client_secret)
print(token)
