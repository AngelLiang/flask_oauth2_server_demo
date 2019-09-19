# coding-utf-8

from werkzeug.security import gen_salt
from authlib.flask.oauth2 import AuthorizationServer, ResourceProtector
from authlib.flask.oauth2.sqla import (
    create_query_client_func, create_save_token_func,
    create_revocation_endpoint, create_bearer_token_validator
)
from authlib.specs.rfc6750 import BearerTokenValidator
from authlib.specs.rfc6749 import grants


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

# 认证服务器
authorization = AuthorizationServer()


class MyBearerTokenValidator(BearerTokenValidator):
    """客制化 Bearer Token 验证器"""

    def authenticate_token(self, token_string):
        """A method to query token from database with the given token string.
        Developers MUST re-implement this method. For instance::

            def authenticate_token(self, token_string):
                return get_token_from_database(token_string)

        :param token_string: A string to represent the access_token.
        :return: token
        """
        return OAuth2Token.query.filter_by(access_token=token_string).first()

    def request_invalid(self, request):
        """Check if the HTTP request is valid or not.  Developers MUST
        re-implement this method.  For instance, your server requires a
        "X-Device-Version" in the header::

            def request_invalid(self, request):
                return 'X-Device-Version' in request.headers

        Usually, you don't have to detect if the request is valid or not,
        you can just return a ``False``.

        :param request: instance of TokenRequest
        :return: Boolean
        """
        return False

    def token_revoked(self, token):
        """Check if this token is revoked. Developers MUST re-implement this
        method. If there is a column called ``revoked`` on the token table::

            def token_revoked(self, token):
                return token.revoked

        :param token: token instance
        :return: Boolean
        """
        return token.revoked

# 资源保护器
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

    # only bearer token is supported currently
    require_oauth.register_token_validator(MyBearerTokenValidator())

    # you can also create BearerTokenValidator with shortcut
    # bearer_cls = create_bearer_token_validator(db.session, OAuth2Token)
    # require_oauth.register_token_validator(bearer_cls())
