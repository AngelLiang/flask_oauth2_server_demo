# coding=utf-8
"""
how to use

```
# filename:__init__.py

def create_app():
    # ...

    form errors import init_errors_page
    init_errors_page(app)

    return app
```
"""

from flask import render_template
from app import admin

def init_errors_page(app):
    @app.errorhandler(401)
    def error_401(e):
        return render_template('errors/401.jinja2')

    @app.errorhandler(403)
    def error_403(e):
        return render_template('errors/403.jinja2')

    @app.errorhandler(404)
    def error_404(e):
        return render_template('errors/404.jinja2')

    @app.errorhandler(500)
    def error_500(e):
        return render_template('errors/404.jinja2')
