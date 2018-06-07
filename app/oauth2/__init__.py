# coding-utf-8

from authlib.flask.oauth2 import AuthorizationServer, ResourceProtector
from authlib.flask.oauth2.sqla import (
    create_query_client_func, create_save_token_func, create_revocation_endpoint, create_bearer_token_validator,)
from authlib.specs.rfc6749 import grants
from werkzeug.security import gen_salt

# db
from app.database import db

# model
from app.models import User
from app.models import OAuth2Client, OAuth2AuthorizationCode, OAuth2Token


class AuthorizationCodeGrant(grants.AuthorizationCodeGrant):
    """认证码授权"""

    def create_authorization_code(self, client, user, request):
        """创建认证码"""
        code = gen_salt(48)
        item = OAuth2AuthorizationCode(
            code=code,
            client_id=client.client_id,
            redirect_uri=request.redirect_uri,
            scope=request.scope,
            user_id=user.id,
        )
        db.session.add(item)
        db.session.commit()
        return code

    def parse_authorization_code(self, code, client):
        """解析认证码"""
        item = OAuth2AuthorizationCode.query.filter_by(
            code=code, client_id=client.client_id).first()
        if item and not item.is_expired():
            return item

    def delete_authorization_code(self, authorization_code):
        """删除认证码"""
        db.session.delete(authorization_code)
        db.session.commit()

    def authenticate_user(self, authorization_code):
        """认证用户"""
        return User.query.get(authorization_code.user_id)


class PasswordGrant(grants.ResourceOwnerPasswordCredentialsGrant):
    """密码授权"""

    def authenticate_user(self, username, password):
        """认证用户"""
        # print(username)
        user = User.query.filter_by(username=username).first()
        if user.verify_password(password):
            return user


class RefreshTokenGrant(grants.RefreshTokenGrant):
    """Refresh Token授权"""

    def authenticate_refresh_token(self, refresh_token):
        """认证refresh token"""
        item = OAuth2Token.query.filter_by(refresh_token=refresh_token).first()
        if item and not item.is_refresh_token_expired():
            return item

    def authenticate_user(self, credential):
        """认证用户"""
        return User.query.get(credential.user_id)


authorization = AuthorizationServer()
require_oauth = ResourceProtector()


def init_oauth(app):
    """OAuth配置app"""
    query_client = create_query_client_func(db.session, OAuth2Client)
    save_token = create_save_token_func(db.session, OAuth2Token)
    authorization.init_app(
        app, query_client=query_client, save_token=save_token)

    # support all grants
    authorization.register_grant(grants.ImplicitGrant)
    authorization.register_grant(grants.ClientCredentialsGrant)
    authorization.register_grant(AuthorizationCodeGrant)    # 注册 code 授权
    authorization.register_grant(PasswordGrant)  # 注册密码授权
    authorization.register_grant(RefreshTokenGrant)  # 注册 refresh token 授权

    # support revocation
    revocation_cls = create_revocation_endpoint(db.session, OAuth2Token)
    authorization.register_endpoint(revocation_cls)

    # protect resource
    bearer_cls = create_bearer_token_validator(db.session, OAuth2Token)
    require_oauth.register_token_validator(bearer_cls())
