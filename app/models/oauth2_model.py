# coding=utf-8

import time

# database
from app.database import (db, SurrogatePK, CRUDMixin,
                          Model, reference_col, relationship, backref, aliased)

# model
from .user_model import User

# authlib
from authlib.flask.oauth2.sqla import (
    OAuth2ClientMixin, OAuth2AuthorizationCodeMixin, OAuth2TokenMixin, OAuth2AuthorizationCodeMixin)


class OAuth2Client(Model, OAuth2ClientMixin):
    """OAuth2客户端"""
    __tablename__ = 'oauth2_client'

    id = db.Column(db.Integer, primary_key=True)

    # 与 user model 为多对一
    user_id = db.Column(
        db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    user = db.relationship('User')


class OAuth2Token(Model, OAuth2TokenMixin):
    """OAuth2 token"""
    __tablename__ = 'oauth2_token'

    id = db.Column(db.Integer, primary_key=True)

    # 与 user model 为多对一
    user_id = db.Column(
        db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    user = db.relationship('User')

    def is_access_token_expired(self):
        expires_at = self.issued_at + self.expires_in
        return expires_at < time.time()

    def is_refresh_token_expired(self):
        """
        refresh token是否过期
        """
        expires_at = self.issued_at + self.expires_in * 2  # expires_in两倍时间
        return expires_at < time.time()


class OAuth2AuthorizationCode(Model, OAuth2AuthorizationCodeMixin):
    """OAuth2认证码"""
    __tablename__ = 'oauth2_code'

    id = db.Column(db.Integer, primary_key=True)

    # 与 user model 为多对一
    user_id = db.Column(
        db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    user = db.relationship('User')
