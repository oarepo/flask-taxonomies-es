from urllib.parse import urlparse

from flask import current_app
from flask_taxonomies.models import Taxonomy, TaxonomyTerm
from werkzeug.utils import cached_property

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


class Constants:
    @cached_property
    def server_name(self):
        return current_app.config.get('SERVER_NAME')


constants = Constants()


def link_self(taxonomy_code, taxonomy_term=None, taxonomy_slug=None, parent_path: str = None):
    """
    Function returns reference to the taxonomy from taxonomy code and taxonomy term.
    :param taxonomy_code:
    :param taxonomy_term:
    :return:
    """

    SERVER_NAME = constants.server_name
    base = f"http://{SERVER_NAME}/api/taxonomies"
    if taxonomy_term and not taxonomy_slug:
        slug = taxonomy_term.slug
    elif not taxonomy_term and taxonomy_slug:
        slug = taxonomy_slug
    else:
        assert False, "Must insert taxonomy term or taxonomy slug, but you must not insert together"
    if parent_path is not None:
        path = [base, taxonomy_code + parent_path + "/"]
    else:
        path = [base, taxonomy_code + "/" + slug + "/"]
    return "/".join(path)


def get_taxonomy_links(taxonomy, taxonomy_term: TaxonomyTerm, parent_path: str = None):
    self = link_self(taxonomy_code=taxonomy, taxonomy_term=taxonomy_term)
    parent = link_self(taxonomy_code=taxonomy, taxonomy_term=taxonomy_term, parent_path=parent_path)
    return {
        "self": self,
        "tree": self + "?drilldown=True",
        "parent": parent,
        "parent_tree": parent + "?drilldown=True"
    }
