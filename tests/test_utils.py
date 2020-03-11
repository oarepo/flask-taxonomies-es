import pytest

from flask_taxonomies_es.utils import _get_taxonomy_slug_from_url


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
def test_get_taxonomy_slug_from_url(app, test_db, root_taxonomy, child_term, url, taxonomy, slug):
    taxonomy_res, slug_res = _get_taxonomy_slug_from_url(
        url)
    assert taxonomy_res == taxonomy
    assert slug_res == slug
