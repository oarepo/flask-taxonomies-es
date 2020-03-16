import pytest
from flask import Flask

from flask_taxonomies_es import FlaskTaxonomiesES


def test_version():
    """Test version import."""
    from flask_taxonomies_es.version import __version__
    assert __version__


# TODO: vyřešit problém s current_search_client, aplikace potřebuje znát adresu elastiku
@pytest.mark.skip(
    reason="The test needs to resolve the dependency on invenio-search and its "
           "current_search_client.")
def test_init():
    """Test extension initialization."""
    print("start")
    app = Flask('testapp')
    ext = FlaskTaxonomiesES(app)
    assert 'flask-taxonomies-es' in app.extensions

    app = Flask('testapp')
    ext = FlaskTaxonomiesES()
    assert 'flask-taxonomies-es' not in app.extensions
    ext.init_app(app)
    assert 'flask-taxonomies-es' in app.extensions
