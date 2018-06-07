# cofing=utf-8

from flask import redirect, url_for, current_app
from flask_user import current_user

from . import views


@views.route('/')
@views.route('/index')
@views.route('/home')
def index():
    # 如果用户已经登录则重定向到 profile ，否则重定向到登录页面
    current_app.logger.debug(current_user)
    if current_user and current_user.is_authenticated:
        # return redirect(url_for("user.profile"))
        return redirect(url_for("admin.index"))
    return redirect(url_for("user.login"))
