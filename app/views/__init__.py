# coding=utf-8

from flask import Blueprint
from flask_admin import Admin

views = Blueprint("views", __name__, template_folder="templates")

from .index_views import *


def init_admin_views(admin: Admin):
    from .user_views import init_admin_view as init_user
    init_user(admin)

    from .oauth2_views import init_admin_view as init_auth
    init_auth(admin)
