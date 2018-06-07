# coding=utf-8

import os
from .config_flask_user import FlaskUserConfig

curr_dir = os.path.abspath(os.path.dirname(__file__))
last_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

app_dir = last_dir


class Config(FlaskUserConfig):
    APP_NAME = "OAuth2 Server 示例"
    USER_APP_NAME = APP_NAME
    # SECRET_KEY
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or 'hard to guess string and longer than 32 byte!'

    # 数据库session在请求后自动提交
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    # 本地化
    BABEL_DEFAULT_LOCALE = "zh_CN"

    FLASK_ADMIN_THEME_FOLDER = "sb-admin-2"

    # USE_X_SENDFILE = True   # default False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(app_dir, 'data-dev.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # jinja2模板自动加载
    TEMPLATES_AUTO_RELOAD = True
    # jinja2模板渲染跟踪
    EXPLAIN_TEMPLATE_LOADING = False


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(app_dir, 'data-test.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(app_dir, 'data.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'prodection': ProductionConfig,
    'default': DevelopmentConfig
}
