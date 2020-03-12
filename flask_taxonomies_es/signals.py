from flask_taxonomies_es.proxies import current_flask_taxonomies_es
from flask_taxonomies_es.utils import _resolve_json


def update_taxonomy_term(sender, term=None, *args, **kwargs):
    if term:
        current_flask_taxonomies_es.set(term)


def delete_taxonomy_term(sender, term=None, *args, **kwargs):
    if term:
        current_flask_taxonomies_es.remove(taxonomy_term=term)


def move_term(sender, *args, **kwargs):
    current_flask_taxonomies_es.reindex()


def json_resolve(sender, code=None, slug=None, *args, **kwargs):
    return _resolve_json(code, slug)


