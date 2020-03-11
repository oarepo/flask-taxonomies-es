from flask import current_app
from werkzeug.local import LocalProxy

current_flask_taxonomies_es = LocalProxy(
    lambda: current_app.extensions['flask-taxonomies-es'])
