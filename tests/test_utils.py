import time
from pprint import pprint

import pytest

from flask_taxonomies_es.proxies import current_flask_taxonomies_es
from flask_taxonomies_es.utils import _get_taxonomy_slug_from_url, _resolve_json, _get_tree_ids


@pytest.mark.parametrize("url, taxonomy, slug",
                         [
                             ("http://localhost/taxonomies/root/1/3/", "root", "3"),
                             ("/taxonomies/root/1/3/", "root", "3"),
                             ("taxonomies/root/1/3", "root", "3"),
                             ("/api/taxonomies/root/1/neco/navic/3", "root", "3"),
                             ("/api/taxonomies/taxonomie_x/1/neco/navic/3", "taxonomie_x", "3"),
                             ("cesta/pred/taxonomii/api/taxonomies/root/1/neco/navic/3", "root",
                              "3"),

                         ]
                         )
def test_get_taxonomy_slug_from_url(app, db, root_taxonomy, child_term, url, taxonomy, slug):
    taxonomy_res, slug_res = _get_taxonomy_slug_from_url(
        url)
    assert taxonomy_res == taxonomy
    assert slug_res == slug


def test_resolve_json(app, db, child_term, child_term_dict):
    current_flask_taxonomies_es.set(child_term)
    time.sleep(1)
    term = _resolve_json(child_term.taxonomy.slug, child_term.slug)
    child_term_dict = child_term_dict
    del child_term_dict["taxonomy"]
    assert term == child_term_dict


def test_get_tree_ids(app, db, root_taxonomy):
    tree_ids = _get_tree_ids(["root", "bla"])
    assert tree_ids == [1]
