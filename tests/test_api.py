import time

import pytest
from invenio_search import current_search_client

from flask_taxonomies_es.api import TaxonomyESAPI
from flask_taxonomies_es.proxies import current_flask_taxonomies_es


def test_init(app):
    assert current_search_client.indices.exists(app.config["TAXONOMY_ELASTICSEARCH_INDEX"])


def test_set_get_remove(app, test_db, root_taxonomy, sample_term):
    current_flask_taxonomies_es.set(sample_term)
    time.sleep(1)
    result = current_flask_taxonomies_es.get(root_taxonomy.slug, sample_term.slug)
    del result['date_of_serialization']
    assert result == {
        "url": "http://www.vscht.cz/",
        "title": [
            {
                "lang": "cze",
                "value": "Vysoká škola chemicko-technologická v Praze"
            }
        ],
        "address": "Technická 5, 166 28 Praha 6",
        "lib_url": "",
        "id": 2,
        "slug": "1",
        "taxonomy": "root",
        "path": "/1",
        "links": {
            "self": "http://localhost/taxonomies/root/1/",
            "tree": "http://localhost/taxonomies/root/1/?drilldown=True",
            "parent": "http://localhost/taxonomies/root/",
            "parent_tree": "http://localhost/taxonomies/root/?drilldown=True"
        },
        "level": 1
    }
    current_flask_taxonomies_es.remove(sample_term)
    time.sleep(1)
    result = current_flask_taxonomies_es.get(root_taxonomy.slug, sample_term.slug)
    assert result is None


def test_set_remove_2(app, test_db, root_taxonomy, sample_term):
    current_flask_taxonomies_es.set(sample_term)
    time.sleep(1)
    current_flask_taxonomies_es.remove(
        taxonomy_code=sample_term.taxonomy.slug,
        slug=sample_term.slug
    )
    time.sleep(1)
    result = current_flask_taxonomies_es.get(root_taxonomy.slug, sample_term.slug)
    assert result is None


def test_list(app, test_db, root_taxonomy, sample_term, sample_term_2):
    current_flask_taxonomies_es.set(sample_term)
    current_flask_taxonomies_es.set(sample_term_2)
    time.sleep(1)
    results = current_flask_taxonomies_es.list("root")
    new_results = []
    for result in results:
        del result["date_of_serialization"]
        new_results.append(result)
    assert new_results == [
        {
            'url': 'http://www.vscht.cz/',
            'title': [
                {'lang': 'cze', 'value': 'Vysoká škola chemicko-technologická v Praze'}
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
        },
        {
            'url': 'http://cuni.cz/',
            'title': [
                {
                    'lang': 'cze',
                    'value': 'Univerzita Karlova'
                }
            ],
            'address': 'Ovocný trh 5, 116 36 Praha 1',
            'lib_url': 'https://dspace.cuni.cz/',
            'id': 3,
            'slug': '2',
            'taxonomy': 'root', 'path': '/2',
            'links': {
                'self': 'http://localhost/taxonomies/root/2/',
                'tree': 'http://localhost/taxonomies/root/2/?drilldown=True',
                'parent': 'http://localhost/taxonomies/root/',
                'parent_tree': 'http://localhost/taxonomies/root/?drilldown=True'
            },
            'level': 1
        }
    ]


def test_get_ref(app, test_db, root_taxonomy, child_term):
    current_flask_taxonomies_es.set(child_term)
    time.sleep(1)
    res = current_flask_taxonomies_es.get(root_taxonomy.slug, child_term.slug)
    res2 = current_flask_taxonomies_es.get_ref(res["links"]["self"])
    del res['date_of_serialization']
    del res2['date_of_serialization']
    assert res == res2 == {
        'title': [
            {
                'lang': 'cze',
                'value': 'Dítě'
            }
        ],
        'id': 3,
        'slug': '3',
        'taxonomy': 'root',
        'path': '/1/3',
        'links': {
            'self': 'http://localhost/taxonomies/root/1/3/',
            'tree': 'http://localhost/taxonomies/root/1/3/?drilldown=True',
            'parent': 'http://localhost/taxonomies/root/1/',
            'parent_tree': 'http://localhost/taxonomies/root/1/?drilldown=True'
        },
        'level': 2,
        'ancestors': [
            {
                'url': 'http://www.vscht.cz/',
                'title': [
                    {
                        'lang': 'cze',
                        'value': 'Vysoká škola chemicko-technologická v Praze'
                    }
                ],
                'address': 'Technická 5, 166 28 Praha 6',
                'lib_url': '',
                'level': 1,
                'slug': '1'
            }
        ]
    }


def test_set_get_child_term(app, test_db, root_taxonomy, child_term):
    current_flask_taxonomies_es.set(child_term)
    time.sleep(1)
    result = current_flask_taxonomies_es.get(root_taxonomy.slug, child_term.slug)
    del result['date_of_serialization']
    assert result["path"] == '/1/3'


def test_synchronize_es(app, test_db, root_taxonomy, sample_term, sample_term_2, child_term):
    current_flask_taxonomies_es._synchronize_es()

# def test_remove_old_es_term()

# def test_reindex(app, test_db, root_taxonomy, sample_term, child_term):
#     current_flask_taxonomies_es.set(sample_term)
#     current_flask_taxonomies_es.reindex()
