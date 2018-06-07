# coding=utf-8

from sqlalchemy import func
from flask import request, render_template, redirect, url_for, flash, current_app, session
from flask_user import login_required, roles_required, current_user
from flask_admin import Admin, expose
from flask_admin.form import rules
from flask_admin.actions import action
from flask_admin.model.template import EndpointLinkRowAction, LinkRowAction

# db
from app.database import db, Column, reference_col, relationship

# model
from app.models import User, Role

# blueprint
from . import views

# flask admin base mode view
from .base_view import MyBaseModelView

##########################################################################
# amdin model view


class UsersModelView(MyBaseModelView):
    """Users Model View"""
    can_create = True
    can_delete = False
    can_view_details = True

    column_display_pk = False

    # column_list = (
    #     User.username,
    #     User.nickname,
    #     User.email,
    # )

    column_labels = {
        "username": u"用户名",
        "email": u"邮箱",
        "nickname": u"昵称",
        "group": u"用户组",
        "roles": u"角色",
        "phone": u"手机号码",
        "sex": u"性别",
        "active": u"激活",
        "groups": u"用户组",
        "org": u"所属组织",
        "create_datetime": u"创建时间",
        "current_login_datetime": u"本次登录时间",
        "last_login_datetime": u"上次登录时间",
        "current_login_ip": u"本次登录IP",
        "last_login_ip": u"上次登录IP",
    }

    column_searchable_list = ('username', )

    # 不显示password
    column_exclude_list = ("password_hash", "password", "avatar_hash")

    # 在表单中排除相关的字段
    form_excluded_columns = (
        # "username",
        # "email",
        # "phone",
        "password_hash",
        "avatar_hash",
    )

    # 表单参数
    form_widget_args = {
        'username': {
            'disabled': True  # 禁用
        },
        "password_hash": {
            'disabled': True
        },
        "org": {
            'disabled': True
        },
    }


class RolesModelView(MyBaseModelView):
    """
    Roles Model View
    """
    can_create = False
    can_delete = False
    can_edit = False
    can_view_details = False

    column_labels = {"name": u"角色名称", "description": u"描述"}

    # action_disallowed_list = ["delete"]


def init_admin_view(admin: Admin):
    admin.add_view(
        UsersModelView(
            User,
            db.session,
            name=u"用户",
            endpoint="users",
            menu_icon_type="glyph",
            menu_icon_value="glyphicon-user",
            category="用户管理"))
    admin.add_view(
        RolesModelView(
            Role, db.session, name=u"角色", endpoint="roles", category="用户管理"))
