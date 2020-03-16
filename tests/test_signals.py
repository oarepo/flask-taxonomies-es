import time
from flask_taxonomies.models import after_taxonomy_term_created, after_taxonomy_term_deleted, \
    before_taxonomy_jsonresolve, after_taxonomy_term_moved

from flask_taxonomies_es.proxies import current_flask_taxonomies_es
from flask_taxonomies_es.signals import update_taxonomy_term, delete_taxonomy_term, move_term


def test_after_taxonomy_term_created(app, db, sample_term, sample_term_dict):
    after_taxonomy_term_created.connect(update_taxonomy_term)
    after_taxonomy_term_created.send(term=sample_term)
    taxonomy_code = sample_term.taxonomy.slug
    slug = sample_term.slug
    time.sleep(1)
    term_dict = current_flask_taxonomies_es.get(taxonomy_code, slug)
    del term_dict['date_of_serialization']
    assert term_dict == sample_term_dict


def test_after_taxonomy_term_deleted(app, db, sample_term, sample_term_dict):
    taxonomy_code = sample_term.taxonomy.slug
    slug = sample_term.slug
    current_flask_taxonomies_es.set(sample_term)
    time.sleep(1)
    taxonomy_dict = current_flask_taxonomies_es.get(taxonomy_code, slug)
    del taxonomy_dict['date_of_serialization']
    assert taxonomy_dict == sample_term_dict
    after_taxonomy_term_deleted.connect(delete_taxonomy_term)
    after_taxonomy_term_deleted.send(term=sample_term)
    time.sleep(1)
    term_dict = current_flask_taxonomies_es.get(taxonomy_code, slug)
    time.sleep(1)
    assert term_dict is None


def test_before_taxonomy_jsonresolve(app, db, sample_term, sample_term_dict):
    taxonomy_code = sample_term.taxonomy.slug
    slug = sample_term.slug
    current_flask_taxonomies_es.set(sample_term)
    time.sleep(1)
    taxonomy_dict = current_flask_taxonomies_es.get(taxonomy_code, slug)
    del taxonomy_dict['date_of_serialization']
    assert taxonomy_dict == sample_term_dict
    resp = before_taxonomy_jsonresolve.send(None, code=taxonomy_code, slug=slug)
    assert resp[0][1] == {
        'address': 'Technická 5, 166 28 Praha 6',
        'id': 2,
        'level': 1,
        'lib_url': '',
        'links': {
            'parent': 'http://localhost/taxonomies/root/',
            'parent_tree': 'http://localhost/taxonomies/root/?drilldown=True',
            'self': 'http://localhost/taxonomies/root/1/',
            'tree': 'http://localhost/taxonomies/root/1/?drilldown=True'
        },
        'path': '/1',
        'slug': '1',
        'title': [
            {
                'lang': 'cze',
                'value': 'Vysoká škola chemicko-technologická v Praze'
            }
        ],
        'url': 'http://www.vscht.cz/'
    }


def test_after_taxonomy_term_moved(app, db, root_taxonomy, sample_term, sample_term_2, child_term):
    terms = current_flask_taxonomies_es.list("root")
    assert len(terms) == 0
    after_taxonomy_term_moved.connect(move_term)
    after_taxonomy_term_moved.send(child_term)
    time.sleep(1)
    terms = current_flask_taxonomies_es.list("root")
    assert len(terms) > 0
