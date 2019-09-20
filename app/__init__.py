# coding=utf-8

from app.views.base_view import MyAdminIndexView
from app.views import init_admin_views
from flask_admin import Admin
from werkzeug.contrib.cache import SimpleCache, RedisCache
from flask_babelex import Babel
from .database import db
import os
import sys
from flask import Flask, jsonify, url_for, request, current_app, session

# config
from config.config import config

curr_dir = os.path.dirname(os.path.realpath(__file__))

###############################################################################
# 数据库

# from flask_sqlalchemy import SQLAlchemy
# db = SQLAlchemy()

###############################################################################
# 国际化

babel = Babel()


@babel.localeselector
def get_locale():
    if request.args.get('lang'):
        session['lang'] = request.args.get('lang')
    return session.get('lang', 'zh_CN')


###############################################################################
# cache

# try:
#     cache = RedisCache()
#     cache.get("connection")  # 连接测试
# except Exception:
#     cache = SimpleCache()
#     print("cache is SimpleCache")
# else:
#     print("cache is RedisCache")
cache = SimpleCache()


###############################################################################
# flask-user

try:
    from .utils.custom_user_manager import CustomUserManager
    user_manager = CustomUserManager()
    # print("user_manager init from custom_user_manager")
except Exception:
    from flask_user import UserManager
    user_manager = UserManager(None, None, None)
    # print("user_manager init from flask_user")

###############################################################################
# flask admin


amdin_index_view = MyAdminIndexView(
    name="仪表盘",
    menu_icon_type="glyph",
    menu_icon_value="glyphicon-home",
)
admin = Admin(
    index_view=amdin_index_view,
    template_mode="bootstrap3",
    # name="flask web admin demo",
)
admin.base_template = "admin/base.jinja2"  # 改为app/templates/admin/base.jinja2
init_admin_views(admin)

###############################################################################


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # 数据库
    db.init_app(app)
    db.app = app

    # 国际化
    babel.init_app(app)

    # flask-admin
    admin.init_app(app)
    admin.name = app.config.get("APP_NAME")

    # flask-user
    from app.models import User
    user_manager.init_app(app, db, User)

    # views
    from app.views import views
    app.register_blueprint(views)

    # apis
    from app.apis import api_bp
    app.register_blueprint(api_bp)

    from app.jinja2_env import init_jinja2_env
    init_jinja2_env(app)

    # oauth2
    from app.oauth2 import init_oauth
    init_oauth(app)

    # error pages
    # from app.errors import init_errors_page
    # init_errors_page(app)
    amdin_index_view.init_errors_page(app)

    return app
