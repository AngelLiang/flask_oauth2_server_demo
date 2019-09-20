# coding=utf-8
# coding=utf-8

from sqlalchemy import func
from werkzeug.security import gen_salt
from flask import Blueprint
from flask import request, render_template, redirect, url_for, flash, current_app, session, jsonify
from flask_user import login_required, roles_required, current_user

# db
from app.database import db

# model
from app.models import User
from app.models import OAuth2Client, OAuth2Token, OAuth2AuthorizationCode

# oauth
from authlib.flask.oauth2 import current_token
from authlib.specs.rfc6749 import OAuth2Error
from app.oauth2 import authorization, require_oauth

from app.json_response import singleton_json_response as s_json


api_bp = Blueprint('api', __name__)


@api_bp.route('/oauth/token/get', methods=['GET', 'POST'])
def get_token():
    """获取access token"""
    response_json = s_json.make_fail()

    # 必须给 authorization.create_token_response() 提供以下字段
    # Authorization: Basic xxx
    # ImmutableMultiDict([('grant_type', 'password'), ('password', 'admin'), ('username', 'admin')])
    # current_app.logger.debug(request.headers)

    current_app.logger.debug(request.form)
    username = request.form.get("username")
    password = request.form.get("password")

    user = User.query.filter_by(username=username).first()
    if user and user.verify_password(password):
        token = OAuth2Token.query.filter_by(user_id=user.id).first()
        if token and not token.is_access_token_expired():
            pass
        else:
            return jsonify(s_json.make_success())
            # token = OAuth2Token(user=user)
            # db.session.add(token)
            # db.session.commit()
            # current_app.logger.info('create OAuth2Token')
        data = {
            "access_token": token.access_token,
            "issued_at": token.issued_at,
            "expires_in": token.expires_in,
            "token_type": token.token_type,
        }
        return jsonify(s_json.make_success(data))
    else:
        current_app.logger.info('user not found or password error')

    return jsonify(response_json)


@api_bp.route('/oauth/token', methods=['GET', 'POST'])
def issue_token():
    """发布access token"""

    # 必须给 authorization.create_token_response() 提供以下字段
    # Authorization: Basic ${client_id}:${client_secret}
    # ImmutableMultiDict([('grant_type', 'password'), ('password', 'admin'), ('username', 'admin')])

    # current_app.logger.debug(request.headers)
    response = authorization.create_token_response()
    current_app.logger.debug(response)
    return response


@api_bp.route('/oauth/revoke', methods=['POST'])
def revoke_token():
    """废除token"""
    return authorization.create_endpoint_response('revocation')


@api_bp.route('/oauth/authorize', methods=['GET', 'POST'])
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


@api_bp.route('/api/me')
@require_oauth('profile')
# @require_oauth()
def api_me():
    """
    @require_oauth()

    header:
    Authorization: Bearer xxx
    """
    user = current_token.user
    return jsonify(id=user.id, username=user.username)
