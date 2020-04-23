from urllib.parse import urlparse

from flask_taxonomies.models import Taxonomy

from flask_taxonomies_es.proxies import current_flask_taxonomies_es


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def _get_taxonomy_slug_from_url(taxonomy_url):
    url_parser = urlparse(taxonomy_url)
    path_list = url_parser.path.split("/")
    path_list = [part for part in path_list if len(part) > 0]
    slug = path_list[-1]
    taxonomies_index = path_list.index("taxonomies")
    return path_list[taxonomies_index + 1], slug


def _resolve_json(code, slug):
    term = current_flask_taxonomies_es.get(code, slug)
    if term:
        del term["date_of_serialization"]
        del term["taxonomy"]
    return term


def _get_tree_ids(taxonomies: list) -> list:
    tree_ids = []
    for taxonomy in taxonomies:
        tax = Taxonomy.get(taxonomy)
        if tax is not None:
            tree_ids.append(tax.tree_id)
    return tree_ids
