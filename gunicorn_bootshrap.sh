#!/bin/sh
# 使用虚拟环境的 gunicorn 启动 flask
# 首先需要安装gunicorn
# (venv) pip install gunicorn

# basepath=$(cd `dirname $0`; pwd)
# cd ${basepath}  # 进入脚本的执行目录
venv/bin/gunicorn wsgi:app -c deploy/gunicorn_config.py
# OR
#venv/bin/gunicorn wsgi:app --keyfile tools/cer/server/server-key.pem --certfile tools/cer/server/server-cert.pem
