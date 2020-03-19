from pprint import pprint

import pytest

from flask_taxonomies_es.serializer import get_taxonomy_term, jsonify_taxonomy_term, _fix_links


@pytest.fixture
def json_dict():
    return {
        'url': 'http://www.vscht.cz/',
        'title': [{'lang': 'cze', 'value': 'Vysoká škola chemicko-technologická v Praze'}],
        'address': 'Technická 5, 166 28 Praha 6', 'lib_url': '',
        'date_of_serialization': '2020-03-18 15:22:11.119588', 'id': 2, 'slug': '1',
        'taxonomy': 'root',
        'path': '/1', 'links': {
            'self': 'http://localhost/taxonomies/root/1/',
            'tree': 'http://localhost/taxonomies/root/1/?drilldown=True',
            'parent': 'http://localhost/taxonomies/root/',
            'parent_tree': 'http://localhost/taxonomies/root/?drilldown=True'
        }, 'level': 1
    }


def test_get_taxonomy_term(app):
    with pytest.raises(ValueError):
        get_taxonomy_term(code="root", slug="something")


def test_get_taxonomy_term_2(app, db, sample_term, sample_term_dict):
    res = get_taxonomy_term(code=sample_term.taxonomy.slug, slug=sample_term.slug)
    del res["date_of_serialization"]
    assert res == sample_term_dict


def test_jsonify_taxonomy_term(app, db, root_taxonomy, sample_term):
    with pytest.raises(Exception):
        jsonify_taxonomy_term(
            sample_term,
            sample_term.taxonomy.slug,
            "withou_slash"
        )


def test_fix_links(json_dict):
    res = _fix_links(json_dict)
    del res["date_of_serialization"]
    assert res == {
        'address': 'Technická 5, 166 28 Praha 6',
        'id': 2,
        'level': 1,
        'lib_url': '',
        'links': {
            'parent': 'http://localhost/api/taxonomies/root/',
            'parent_tree': 'http://localhost/api/taxonomies/root/?drilldown=True',
            'self': 'http://localhost/api/taxonomies/root/1/',
            'tree': 'http://localhost/api/taxonomies/root/1/?drilldown=True'
        },
        'path': '/1',
        'slug': '1',
        'taxonomy': 'root',
        'title': [{
            'lang': 'cze',
            'value': 'Vysoká škola chemicko-technologická v Praze'
        }],
        'url': 'http://www.vscht.cz/'
    }


def test_fix_links_2(json_dict):
    json_dict["links"] = {
        'parent': 'http://localhost/api/taxonomies/root/',
        'parent_tree': 'http://localhost/api/taxonomies/root/?drilldown=True',
        'self': 'http://localhost/api/taxonomies/root/1/',
        'tree': 'http://localhost/api/taxonomies/root/1/?drilldown=True'
    }
    res = _fix_links(json_dict)
    del res["date_of_serialization"]
    assert res == {
        'address': 'Technická 5, 166 28 Praha 6',
        'id': 2,
        'level': 1,
        'lib_url': '',
        'links': {
            'parent': 'http://localhost/api/taxonomies/root/',
            'parent_tree': 'http://localhost/api/taxonomies/root/?drilldown=True',
            'self': 'http://localhost/api/taxonomies/root/1/',
            'tree': 'http://localhost/api/taxonomies/root/1/?drilldown=True'
        },
        'path': '/1',
        'slug': '1',
        'taxonomy': 'root',
        'title': [{
            'lang': 'cze',
            'value': 'Vysoká škola chemicko-technologická v Praze'
        }],
        'url': 'http://www.vscht.cz/'
    }
