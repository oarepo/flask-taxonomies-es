from __future__ import absolute_import, print_function

import os
import shutil
import tempfile

import pytest
from flask import Flask
from flask_taxonomies import FlaskTaxonomies
from flask_taxonomies.views import blueprint as taxonomies_blueprint
from invenio_app.factory import create_api
from invenio_db import InvenioDB
from invenio_db import db as _db
from invenio_search import InvenioSearch, current_search_client
from sqlalchemy_utils import create_database, database_exists

from flask_taxonomies_es.ext import FlaskTaxonomiesES


@pytest.fixture(scope='module')
def create_app():
    """Create test app."""
    return create_api


@pytest.yield_fixture()
def app():
    instance_path = tempfile.mkdtemp()
    _app = Flask('testapp', instance_path=instance_path)

    _app.config.update(

        SQLALCHEMY_TRACK_MODIFICATIONS=True,
        TAXONOMY_ELASTICSEARCH_INDEX="test_taxonomies_es",
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            'SQLALCHEMY_DATABASE_URI',
            'sqlite:////tmp/test.db'),
        SERVER_NAME='localhost',
    )
    InvenioDB(_app)
    InvenioSearch(_app)
    FlaskTaxonomies(_app)
    FlaskTaxonomiesES(_app)
    with _app.app_context():
        _app.register_blueprint(taxonomies_blueprint)
        yield _app

    shutil.rmtree(instance_path)
    with _app.app_context():
        current_search_client.indices.delete(index=_app.config["TAXONOMY_ELASTICSEARCH_INDEX"])


# @pytest.yield_fixture()
# def db(app):
#     """Database fixture."""
#     if not database_exists(str(db_.engine.url)):
#         create_database(str(db_.engine.url))
#     yield db_


@pytest.fixture
def db(app):
    """Create database for the tests."""
    with app.app_context():
        if not database_exists(str(_db.engine.url)) and \
                app.config['SQLALCHEMY_DATABASE_URI'] != 'sqlite://':
            create_database(_db.engine.url)
        _db.create_all()

    yield _db

    # Explicitly close DB connection
    _db.session.close()
    _db.drop_all()

# @pytest.fixture
# def test_db(app):
#     """Create database for the tests."""
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
#     with app.app_context():
#         if not database_exists(str(db_.engine.url)):
#             create_database(db_.engine.url)
#         db_.drop_all()
#         db_.create_all()
#
#     yield db_
#
#     # Explicitly close DB connection
#     db_.session.close()
#     db_.drop_all()


@pytest.fixture
def root_taxonomy(db):
    """Create root taxonomy element."""
    from flask_taxonomies.models import Taxonomy
    root = Taxonomy.create_taxonomy(code="root")
    db.session.add(root)
    db.session.commit()
    return root


@pytest.fixture
def sample_term(db, root_taxonomy):
    """Taxonomy Term fixture."""
    extra_data = {
        "url": "http://www.vscht.cz/",
        "title": [
            {
                "lang": "cze",
                "value": "Vysoká škola chemicko-technologická v Praze"
            }
        ],
        "address": "Technická 5, 166 28 Praha 6",
        "lib_url": ""
    }
    term = root_taxonomy.create_term(slug="1", extra_data=extra_data)
    db.session.add(term)
    db.session.commit()
    return term

@pytest.fixture
def sample_term_dict():
    return {
        'url': 'http://www.vscht.cz/',
        'title': [
            {
                'lang': 'cze',
                'value': 'Vysoká škola chemicko-technologická v Praze'
            }
        ],
        'address': 'Technická 5, 166 28 Praha 6',
        'lib_url': '',
        'id': 2,
        'slug': '1',
        'taxonomy': 'root',
        'path': '/1',
        'links': {
            'self': 'http://localhost/taxonomies/root/1/',
            'tree': 'http://localhost/taxonomies/root/1/?drilldown=True',
            'parent': 'http://localhost/taxonomies/root/',
            'parent_tree': 'http://localhost/taxonomies/root/?drilldown=True'
        },
        'level': 1
    }


@pytest.fixture
def sample_term_2(db, root_taxonomy):
    """Taxonomy Term fixture."""
    extra_data = {
        "url": "http://cuni.cz/",
        "title": [
            {
                "lang": "cze",
                "value": "Univerzita Karlova"
            }
        ],
        "address": "Ovocný trh 5, 116 36 Praha 1",
        "lib_url": "https://dspace.cuni.cz/"
    }
    term = root_taxonomy.create_term(slug="2", extra_data=extra_data)
    db.session.add(term)
    db.session.commit()
    return term


@pytest.fixture
def child_term(db, root_taxonomy, sample_term):
    extra_data = {
        "title": [
            {
                "lang": "cze",
                "value": "Dítě"
            }
        ]
    }
    term = sample_term.create_term(slug="3", extra_data=extra_data)
    db.session.add(term)
    db.session.commit()
    return term


