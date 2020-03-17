# VIZ: https://github.com/oarepo/flask-taxonomies/blob/master/flask_taxonomies/ext.py
from flask_taxonomies.models import after_taxonomy_term_moved, after_taxonomy_term_updated, \
    after_taxonomy_term_deleted, after_taxonomy_term_created, before_taxonomy_jsonresolve

from flask_taxonomies_es import config
from flask_taxonomies_es.api import TaxonomyESAPI
from flask_taxonomies_es.signals import update_taxonomy_term, delete_taxonomy_term, move_term, \
    json_resolve


class FlaskTaxonomiesES(object):
    """App Extension for Flask Taxonomies."""

    def __init__(self, app=None, db=None):
        """Extension initialization."""
        if app:
            self.init_app(app, db)

    def init_app(self, app, db=None):
        """Flask application initialization."""
        self.init_config(app)

        # Connect signals
        after_taxonomy_term_created.connect(update_taxonomy_term)
        after_taxonomy_term_updated.connect(update_taxonomy_term)
        after_taxonomy_term_deleted.connect(delete_taxonomy_term)
        after_taxonomy_term_moved.connect(move_term)
        before_taxonomy_jsonresolve.connect(json_resolve)

        app.extensions['flask-taxonomies-es'] = TaxonomyESAPI(app)

    def init_config(self, app):
        """Initialize configuration."""

        app.config.setdefault("TAXONOMY_ELASTICSEARCH_INDEX",
                              config.TAXONOMY_ELASTICSEARCH_INDEX)  # pragma: no cover
        app.config.setdefault("TAXONOMY_ELASTICSEARCH_LOG_DIR",
                              config.TAXONOMY_ELASTICSEARCH_LOG_DIR)  # pragma: no cover
