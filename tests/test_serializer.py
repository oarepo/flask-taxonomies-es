import pytest

from flask_taxonomies_es.serializer import get_taxonomy_term


def test_get_taxonomy_term(app):
    with pytest.raises(ValueError):
        get_taxonomy_term(code="root", slug="something")
