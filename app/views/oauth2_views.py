# coding=utf-8

from sqlalchemy import func
from werkzeug.security import gen_salt
from flask import request, render_template, redirect, url_for, flash, current_app, session, jsonify
from flask_user import login_required, roles_required, current_user
from flask_admin import Admin, expose

# db
from app.database import db

# model
from app.models import User
from app.models import OAuth2Client, OAuth2Token, OAuth2AuthorizationCode

# flask admin base mode view
from .base_view import MyBaseModelView, MyBaseView
from . import views

# oauth
from authlib.flask.oauth2 import current_token
from authlib.specs.rfc6749 import OAuth2Error
from app.oauth2 import authorization, require_oauth


from app.json_response import singleton_json_response as s_json

##########################################################################
# token


@views.route('/oauth/token/get', methods=['GET', 'POST'])
def get_token():
    """发布access token"""
    response_json = s_json.make_fail()

    # 必须给 authorization.create_token_response() 提供以下字段
    # Authorization: Basic xxx
    # ImmutableMultiDict([('grant_type', 'password'), ('password', 'admin'), ('username', 'admin')])
    # current_app.logger.debug(request.headers)

    current_app.logger.debug(request.form)
    username = request.form.get("username")
    password = request.form.get("password")

    user = User.query.filter_by(username=username).first()
    if user:
        ret = user.verify_password(password)
        if ret:
            token = OAuth2Token.query.filter_by(user_id=user.id).first()
            if token and not token.is_access_token_expired():
                data = {
                    "access_token": token.access_token,
                    "issued_at": token.issued_at,
                    "expires_in": token.expires_in,
                    "token_type": token.token_type,
                }

    return jsonify(response_json)


@views.route('/oauth/token', methods=['GET', 'POST'])
def issue_token():
    """发布access token"""

    # 必须给 authorization.create_token_response() 提供以下字段
    # Authorization: Basic xxx
    # ImmutableMultiDict([('grant_type', 'password'), ('password', 'admin'), ('username', 'admin')])
    # current_app.logger.debug(request.headers)
    data = authorization.create_token_response()
    current_app.logger.debug(data)
    return data


@views.route('/oauth/revoke', methods=['POST'])
def revoke_token():
    """废除token"""
    return authorization.create_endpoint_response('revocation')


@views.route('/oauth/authorize', methods=['GET', 'POST'])
def authorize():
    """
    Create the HTTP response for authorization.
    If resource owner granted the authorization,
    pass the resource owner as the user parameter, otherwise None:
    """
    # user = current_user
    user = User.query.filter_by(username="admin").first()
    current_app.logger.debug(user)
    if request.method == 'GET':
        try:
            grant = authorization.validate_consent_request(end_user=user)
        except OAuth2Error as error:
            current_app.logger.debug(error)
            return error.error
        return render_template('oauth2/authorize.html', user=user, grant=grant)

    if not user and 'username' in request.form:
        username = request.form.get('username')
        user = User.query.filter_by(username=username).first()

    if request.form['confirm']:
        grant_user = user
    else:
        grant_user = None

    return authorization.create_authorization_response(grant_user=grant_user)

##########################################################################
# 资源


@views.route('/api/me')
# @require_oauth('profile')
@require_oauth()
def api_me():
    """
    @require_oauth()

    header:
    Authorization: Bearer xxx
    """
    user = current_token.user
    return jsonify(id=user.id, username=user.username)

##########################################################################
# admin view


class Oauth2View(MyBaseView):

    @expose("/")
    def index(self):
        return self.render("oauth2/index.jinja2")

    @expose("/app_list")
    def app_list(self):
        user = current_user
        if user:
            clients = OAuth2Client.query.filter_by(user_id=user.id).all()
        else:
            clients = []
        return self.render("oauth2/app_list.jinja2", user=user, clients=clients)

    @expose("/app_create", methods=["GET", "POST"])
    def app_create(self):
        user = current_user
        if request.method == "POST":
            # POST
            client = OAuth2Client(**request.form.to_dict(flat=True))
            client.user_id = user.id
            client.client_id = gen_salt(24)
            if client.token_endpoint_auth_method == 'none':
                client.client_secret = ''
            else:
                client.client_secret = gen_salt(48)
            db.session.add(client)
            db.session.commit()

            return redirect(url_for("oauth2view.app_list"))

        return self.render("oauth2/app_create.jinja2")

    # @expose('/authorize', methods=['GET', 'POST'])
    # def authorize(self):
    #     user = current_user
    #     current_app.logger.debug(user)
    #     if request.method == 'GET':
    #         try:
    #             grant = authorization.validate_consent_request(end_user=user)
    #         except OAuth2Error as error:
    #             current_app.logger.debug(error)
    #             return error.error
    # return self.render('oauth2/authorize.html', user=user, grant=grant)

    #     if not user and 'username' in request.form:
    #         username = request.form.get('username')
    #         user = User.query.filter_by(username=username).first()

    #     if request.form['confirm']:
    #         grant_user = user
    #     else:
    #         grant_user = None

    # return
    # authorization.create_authorization_response(grant_user=grant_user)

    # @expose('/token', methods=['POST'])
    # def issue_token(self):
    #     """获取access token"""
    #     # ImmutableMultiDict([('grant_type', 'password'), ('password', 'admin'), ('username', 'admin')])
    #     print(request.form)
    #     return authorization.create_token_response()

    # @expose("/revoke", methods=["POST"])
    # def revoke_token(self):
    #     """废除token"""
    #     return authorization.create_endpoint_response('revocation')


class Oauth2ClientModelView(MyBaseModelView):

    # column_list = (OAuth2Client.client_name, "user",
    #                OAuth2Client.client_id, OAuth2Client.issued_at,
    #                OAuth2Client.expires_at, OAuth2Client.token_endpoint_auth_method,
    #                OAuth2Client.grant_type, OAuth2Client.scope)

    column_labels = {
        "user": u"用户",
        "client_id": u"client_id",
        "issued_at": u"创建时间",
        "expires_at": u"过期时间",
        "client_name": u"client_name",
    }


class OAuth2TokenModelView(MyBaseModelView):
    pass


class OAuth2AuthorizationCodeModelView(MyBaseModelView):
    pass

##########################################################################
# init


def init_admin_view(admin: Admin):
    admin.add_view(Oauth2View(name=u"OAuth2View", category="OAuth"))
    admin.add_view(Oauth2ClientModelView(
        OAuth2Client, db.session, name=u"OAuth2Client", category="OAuth"))
    admin.add_view(OAuth2TokenModelView(
        OAuth2Token, db.session, name=u"OAuth2Token", category="OAuth"))
    admin.add_view(OAuth2AuthorizationCodeModelView(
        OAuth2AuthorizationCode, db.session, name=u"OAuth2AuthorizationCode", category="OAuth"))
