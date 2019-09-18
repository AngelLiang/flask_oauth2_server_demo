# coding=utf-8
"""
创建 access_token
"""

import os
import requests

client_id = os.getenv('CLIENT_ID', '')
client_secret = os.getenv('CLIENT_SECRET', '')

port = int(os.getenv('FLASK_RUN_PORT', 5000))
username = 'admin'
password = 'admin'

data = {
    'grant_type': 'password',
    'username': username,
    'password': password,
    'scope': 'profile'
}
url = f'http://127.0.0.1:{port}/oauth/token'

res = requests.post(url, data=data,
                    auth=(client_id, client_secret))
print(res)
print(res.text)
