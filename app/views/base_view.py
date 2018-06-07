# coding=utf-8

from sqlalchemy import func
from flask import redirect, url_for, request, abort, g, current_app, render_template
from flask_user import current_user, login_required

from flask_admin import BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.model import BaseModelView

# model
from app.models import User


class MyBaseView(BaseView):

    def is_accessible(self):
        # 验证登录并验证权限
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('user.login', next=request.url))
        # raise abort(401)


class MyAdminIndexView(AdminIndexView):

    def is_accessible(self):
        # 验证登录并验证权限
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('user.login', next=request.url))
        # raise abort(401)

    @expose("/")
    # @login_required
    def dashboard(self):
        """dashboard"""
        return self.render("admin/dashboard.jinja2")

    def init_errors_page(self, app):
        @app.errorhandler(401)
        def error_401(e):
            return self.render('admin/errors/401.jinja2')

        @app.errorhandler(403)
        def error_403(e):
            return self.render('admin/errors/403.jinja2')

        @app.errorhandler(404)
        def error_404(e):
            return self.render('admin/errors/404.jinja2')

        @app.errorhandler(500)
        def error_500(e):
            return self.render('admin/errors/404.jinja2')


class MyBaseModelView(ModelView):

    can_create = True
    can_delete = True
    can_view_details = True
    can_export = False

    column_display_pk = False

    # 页数
    can_set_page_size = False
    page_size = 20

    # modal
    # create_modal = True
    # edit_modal = True
    # details_modal = True

    def is_accessible(self):
        # 验证登录并验证权限
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('user.login', next=request.url))
        # raise abort(401)

    def get_query(self):
        return super().get_query()

    def get_count_query(self):
        return super().get_count_query()
