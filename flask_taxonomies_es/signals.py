from flask_taxonomies.models import TaxonomyTerm

from flask_taxonomies_es.proxies import current_flask_taxonomies_es


def update_taxonomy_term(sender, term=None, *args, **kwargs):
    if term:
        current_flask_taxonomies_es.set(term)


def delete_taxonomy_term(sender, term=None, *args, **kwargs):
    if term:
        current_flask_taxonomies_es.remove(taxonomy_term=term)


def move_term(sender, *args, **kwargs):
    current_flask_taxonomies_es.reindex()
