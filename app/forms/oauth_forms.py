# coding=utf-8

# flask_wtf
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class OAuth2ClientForm():
    client_name = StringField('client_name', validators=[
                              DataRequired()], default="Hi")
    client_uri = StringField('client_uri', validators=[
                             DataRequired()], default="https://authlib.org/")
    allowed_scope = StringField('allowed_scope', validators=[
                                DataRequired()], default="profile")
    redirect_uris = StringField('redirect_uris', validators=[
                                DataRequired()])
    allowed_grant_types = StringField('allowed_grant_types', validators=[
        DataRequired()])
    allowed_response_types = StringField('allowed_response_types', validators=[
        DataRequired()])
    token_endpoint_auth_method = StringField('allowed_response_types', validators=[
        DataRequired()])
