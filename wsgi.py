# coding=utf-8
"""

.flaskenv:

FLASK_APP=wsgi.py
FLASK_ENV=development

"""

import os
from app import create_app

curr_dir = os.path.dirname(os.path.realpath(__file__))

app = create_app(os.getenv('FLASK_ENV') or 'default')

if __name__ == '__main__':
    app.run()

###############################################################################

import getpass

from flask import current_app
from app import db
from app.models import User, Role


def _createuser(roles):
    username = input("Please Enter the superuser username:")
    if not username:
        print("username is empty!")
        return

    if User.query.filter_by(username=username).first():
        print("There is the same superuser username!")
        return

    password = getpass.getpass("Password:")
    password2 = getpass.getpass("Confirm password:")
    if password != password2:
        print("password is not confirmed!")
        return

    user = User.create(
        username=username, password=password, roles=roles, active=True)
    return user


@app.cli.command()
def createsuperuser():
    """创建超级管理员"""

    admin = Role.get_or_create(name="admin")
    developer = Role.get_or_create(name="developer")
    default = Role.get_or_create(name="default")

    ret = _createuser([admin, developer])
    if ret:
        print("Superuser is created successfully!")


@app.cli.command()
def initdb():
    """数据库初始化"""

    ret = input("drop the database? [y/n] ")
    if ret in ("y", "Y", "yes"):
        db.drop_all()
        print("drop database finish!")
    db.create_all()
    print("The database is created successfully!")
    # createsuperuser()
