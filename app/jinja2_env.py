# coding=utf-8

from sqlalchemy import func
from flask import Flask, request, url_for, current_app
from flask_user import current_user

# db
from app.database import db, Column, reference_col, relationship

# model
from app.models import User, Role


def get_count(model) -> int:
    return db.session.query(func.count(model.id)).first()[0]


def get_user_count() -> int:
    return get_count(User)

##########################################################################


def init_jinja2_env(app: Flask):
    app.add_template_global(get_user_count, "get_user_count")
