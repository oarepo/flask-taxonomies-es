import pytest

from flask_taxonomies_es.serializer import get_taxonomy_term, jsonify_taxonomy_term


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
