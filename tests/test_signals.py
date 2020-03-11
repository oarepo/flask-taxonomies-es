import time

from flask_taxonomies.models import after_taxonomy_term_created, after_taxonomy_term_deleted

from flask_taxonomies_es.proxies import current_flask_taxonomies_es
from flask_taxonomies_es.signals import update_taxonomy_term, delete_taxonomy_term


def test_after_taxonomy_term_created(app, test_db, sample_term, sample_term_dict):
    after_taxonomy_term_created.connect(update_taxonomy_term)
    after_taxonomy_term_created.send(term=sample_term)
    taxonomy_code = sample_term.taxonomy.slug
    slug = sample_term.slug
    time.sleep(1)
    term_dict = current_flask_taxonomies_es.get(taxonomy_code, slug)
    del term_dict['date_of_serialization']
    assert term_dict == sample_term_dict


def test_after_taxonomy_term_deleted(app, test_db, sample_term, sample_term_dict):
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


def test_after_taxonomy_term_moved():
    pass
