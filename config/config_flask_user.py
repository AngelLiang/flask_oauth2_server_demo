# coding=utf-8

__all__ = ("FlaskUserConfig", )


class FlaskUserConfig(object):
    # Flask-Mail settings
    # Flask-Mail SMTP server settings
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    USER_EMAIL_SENDER_EMAIL = 'email@example.com'
    MAIL_PASSWORD = 'password'
    USER_EMAIL_SENDER_NAME = '"MyApp" <noreply@example.com>'

    USER_APP_NAME = "AppName"  # Used by email templates

    ######################################################################
    # username

    USER_ENABLE_USERNAME = True  # Register and Login with username

    # Allow users to change their username.
    # Depends on USER_ENABLE_USERNAME=True.
    USER_ENABLE_CHANGE_USERNAME = False

    ######################################################################
    # register

    # Allow unregistered users to register.
    USER_ENABLE_REGISTER = True  # Allow new users to register

    ######################################################################
    # Email

    # Allow users to login and register with an email address
    USER_ENABLE_EMAIL = False

    # Allow users to associate multiple email addresses with one user account.
    # Depends on USER_ENABLE_EMAIL=True
    USER_ENABLE_MULTIPLE_EMAILS = False

    # Enable email confirmation emails to be sent.
    # Depends on USER_ENABLE_EMAIL=True.
    USER_ENABLE_CONFIRM_EMAIL = False

    # Ensure that users can login only with a confirmed email address.
    # Depends on USER_ENABLE_EMAIL=True.
    USER_ALLOW_LOGIN_WITHOUT_CONFIRMED_EMAIL = True

    # Send notification email after a registration.
    # Depends on USER_ENABLE_EMAIL=True.
    USER_SEND_REGISTERED_EMAIL = False

    ######################################################################
    # password

    # Allow users to reset their passwords.
    # Depends on USER_ENABLE_EMAIL=True.
    USER_ENABLE_FORGOT_PASSWORD = False

    # Require users to retype their password.
    # Affects registration, change password and reset password forms.
    USER_REQUIRE_RETYPE_PASSWORD = True

    # Allow users to change their password.
    USER_ENABLE_CHANGE_PASSWORD = True

    # Send notification email after a password change.
    # Depends on USER_ENABLE_EMAIL=True.
    USER_SEND_PASSWORD_CHANGED_EMAIL = False

    ######################################################################
    # login

    # Automatic sign-in if the user session has not expired.
    USER_AUTO_LOGIN = True

    # Automatic sign-in after a user confirms their email address.
    USER_AUTO_LOGIN_AFTER_CONFIRM = True

    # Automatic sign-in after a user registers.
    USER_AUTO_LOGIN_AFTER_REGISTER = True

    # Automatic sign-in after a user resets their password.
    USER_AUTO_LOGIN_AFTER_RESET_PASSWORD = True

    # Automatic sign-in at the login form (if the user session has not
    # expired).
    USER_AUTO_LOGIN_AT_LOGIN = True

    # Allow unregistered users to be invited.
    USER_ENABLE_INVITE_USER = False

    # Remember user sessions across browser restarts.
    USER_ENABLE_REMEMBER_ME = True

    USER_ENABLE_AUTH0 = False

    ######################################################################
    # URL

    # USER_CHANGE_PASSWORD_URL = '/user/change-password'

    # USER_CHANGE_USERNAME_URL = '/user/change-username'

    # USER_CONFIRM_EMAIL_URL = '/user/confirm-email/<token>'

    # USER_EDIT_USER_PROFILE_URL = '/user/edit_user_profile'

    # USER_EMAIL_ACTION_URL = '/user/email/<id>/<action>'

    # USER_FORGOT_PASSWORD_URL = '/user/forgot-password'

    # USER_INVITE_USER_URL = '/user/invite'

    # USER_LOGIN_URL = '/user/sign-in'
    USER_LOGIN_URL = '/user/login'

    # USER_LOGOUT_URL = '/user/sign-out'
    USER_LOGOUT_URL = '/user/logout'

    # USER_MANAGE_EMAILS_URL = '/user/manage-emails'

    # USER_REGISTER_URL = '/user/register'

    # USER_RESEND_EMAIL_CONFIRMATION_URL = '/user/resend-email-confirmation'

    # USER_RESET_PASSWORD_URL = '/user/reset-password/<token>'

    ######################################################################
    # template

    # Form template files                   # Defaults

    # USER_CHANGE_PASSWORD_TEMPLATE = 'flask_user/change_password.html'
    USER_CHANGE_PASSWORD_TEMPLATE = 'user/change_password.jinja2'

    # USER_CHANGE_USERNAME_TEMPLATE = 'flask_user/change_username.html'

    # USER_EDIT_USER_PROFILE_TEMPLATE = 'flask_user/edit_user_profile.html'

    # USER_FORGOT_PASSWORD_TEMPLATE = 'flask_user/forgot_password.html'

    # USER_INVITE_USER_TEMPLATE = 'flask_user/invite_user.html'

    # USER_LOGIN_TEMPLATE = 'flask_user/login.html'
    USER_LOGIN_TEMPLATE = 'auth/login.jinja2'

    # USER_LOGIN_AUTH0_TEMPLATE = 'flask_user/login_auth0.html'

    # USER_MANAGE_EMAILS_TEMPLATE = 'flask_user/manage_emails.html'

    # USER_REGISTER_TEMPLATE = 'flask_user/register.html'
    USER_REGISTER_TEMPLATE = 'auth/register.jinja2'

    # USER_RESEND_CONFIRM_EMAIL_TEMPLATE = 'flask_user/resend_confirm_email.html'

    # USER_RESET_PASSWORD_TEMPLATE = 'flask_user/reset_password.html'

    # Place the Login form and the Register form on one page:
    # Only works for Flask-User v0.4.9 and up
    # USER_LOGIN_TEMPLATE                     = 'flask_user/login_or_register.html'
    # USER_REGISTER_TEMPLATE                  = 'flask_user/login_or_register.html'

    ######################################################################
    # Email template file settings

    # USER_CONFIRM_EMAIL_TEMPLATE = 'flask_user/emails/confirm_email'

    # USER_INVITE_USER_EMAIL_TEMPLATE = 'flask_user/emails/invite_user'

    # USER_PASSWORD_CHANGED_EMAIL_TEMPLATE = 'flask_user/emails/password_changed'

    # USER_REGISTERED_EMAIL_TEMPLATE = 'flask_user/emails/registered'

    # USER_RESET_PASSWORD_EMAIL_TEMPLATE = 'flask_user/emails/reset_password'

    # USER_USERNAME_CHANGED_EMAIL_TEMPLATE = 'flask_user/emails/username_changed'

    ######################################################################
    # FLask endpoint settings

    # USER_AFTER_CHANGE_PASSWORD_ENDPOINT = ''

    # USER_AFTER_CHANGE_USERNAME_ENDPOINT = ''

    # USER_AFTER_CONFIRM_ENDPOINT = ''

    # USER_AFTER_EDIT_USER_PROFILE_ENDPOINT = ''

    # USER_AFTER_FORGOT_PASSWORD_ENDPOINT = ''

    # USER_AFTER_LOGIN_ENDPOINT = ''

    # USER_AFTER_LOGOUT_ENDPOINT = ''

    # USER_AFTER_REGISTER_ENDPOINT = ''

    # USER_AFTER_RESEND_EMAIL_CONFIRMATION_ENDPOINT = ''

    # USER_AFTER_RESET_PASSWORD_ENDPOINT = ''

    # USER_AFTER_INVITE_ENDPOINT = ''

    # USER_UNAUTHENTICATED_ENDPOINT = 'user.login'

    # USER_UNAUTHORIZED_ENDPOINT = ''
