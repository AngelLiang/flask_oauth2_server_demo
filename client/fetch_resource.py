# coding=utf-8

import os
import requests

port = int(os.getenv('FLASK_RUN_PORT', 5000))
token = os.getenv('TOKEN', '')

url = f'http://127.0.0.1:{port}/api/me'
headers = {'Authorization': f'Bearer {token}'}

res = requests.get(url, headers=headers)
print(res)
print(res.text)
