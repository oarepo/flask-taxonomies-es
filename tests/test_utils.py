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


def test_resolve_json(app, db, child_term):
    current_flask_taxonomies_es.set(child_term)
    time.sleep(1)
    term = _resolve_json(child_term.taxonomy.slug, child_term.slug)
    assert term == {
        'ancestors': [
            {
                'address': 'Technická 5, 166 28 Praha 6',
                'level': 1,
                'lib_url': '',
                'slug': '1',
                'title': [
                    {
                        'lang': 'cze',
                        'value': 'Vysoká škola chemicko-technologická v '
                                 'Praze'
                    }
                ],
                'url': 'http://www.vscht.cz/'
            }
        ],
        'id': 3,
        'level': 2,
        'links': {
            'parent': 'http://localhost/taxonomies/root/1/',
            'parent_tree': 'http://localhost/taxonomies/root/1/?drilldown=True',
            'self': 'http://localhost/taxonomies/root/1/3/',
            'tree': 'http://localhost/taxonomies/root/1/3/?drilldown=True'
        },
        'path': '/1/3',
        'slug': '3',
        'title': [
            {
                'lang': 'cze',
                'value': 'Dítě'
            }
        ]
    }


def test_get_tree_ids(app, db, root_taxonomy):
    tree_ids = _get_tree_ids(["root", "bla"])
    assert tree_ids == [1]
