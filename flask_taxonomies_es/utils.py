from urllib.parse import urlparse

from flask_taxonomies_es.proxies import current_flask_taxonomies_es


def _get_taxonomy_slug_from_url(taxonomy_url):
    url_parser = urlparse(taxonomy_url)
    path_list = url_parser.path.split("/")
    path_list = [part for part in path_list if len(part) > 0]
    slug = path_list[-1]
    taxonomies_index = path_list.index("taxonomies")
    return path_list[taxonomies_index + 1], slug


def _resolve_json(code, slug):
    term = current_flask_taxonomies_es.get(code, slug)
    del term["date_of_serialization"]
    del term["taxonomy"]
    return term
