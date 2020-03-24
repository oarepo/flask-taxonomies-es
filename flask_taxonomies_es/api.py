import os
import time
import traceback
from datetime import datetime

from elasticsearch.helpers import streaming_bulk
from elasticsearch_dsl import Search, Q
from flask_taxonomies.models import TaxonomyTerm
from invenio_search import current_search_client

from flask_taxonomies_es.exceptions import InvalidTermIdentification
from flask_taxonomies_es.serializer import get_taxonomy_term
from flask_taxonomies_es.utils import _get_taxonomy_slug_from_url, _get_tree_ids, bcolors


class TaxonomyESAPI:
    """
    Constructor takes Flask app as parameter. However, it is not necessary create class instance.
    Class instance should be called with proxy method: current_flask_taxonomies_es.
    """

    def __init__(self, app):
        self.app = app
        # self.index = app.config["TAXONOMY_ELASTICSEARCH_INDEX"]
        # self._create_index()

    @property
    def index(self):
        _index = self.app.config["TAXONOMY_ELASTICSEARCH_INDEX"]
        if not current_search_client.indices.exists(_index):
            current_search_client.indices.create(
                index=_index,
                ignore=400,
                body={}
            )
        return _index

    def set(self, taxonomy_term: TaxonomyTerm, timestamp=None) -> None:
        """
        Save serialized taxonomy into Elasticsearch. It create new or update old taxonomy record.

        :param taxonomy_term: Taxonomy term class from flask-taxonomies
        :type taxonomy_term: TaxonomyTerm
        :param timestamp: Datetime class
        :type timestamp: Datetime class
        :return: None
        :rtype: None
        """
        if taxonomy_term.parent:
            body = get_taxonomy_term(
                code=taxonomy_term.taxonomy.slug,
                slug=taxonomy_term.slug,
                timestamp=timestamp
            )
            current_search_client.index(
                index=self.index,
                id=taxonomy_term.id,
                body=body
            )

    def remove(self, taxonomy_term: TaxonomyTerm = None, taxonomy_code: str = None,
               slug: str = None) -> None:
        """
        Remove taxonomy term from elasticsearch index. It takes either TaxonomyTerm class or
        taxonomy code with slug as strings.

        :param taxonomy_term: Taxonomy term class from flask-taxonomies
        :type taxonomy_term: TaxonomyTerm
        :param taxonomy_code: Code of taxonomy.
        :type taxonomy_code: str
        :param slug: Taxonomy slug as string
        :type slug: str
        :return: None
        :rtype: None
        """
        if taxonomy_term:
            id_ = taxonomy_term.id
        elif taxonomy_code and slug:
            id_ = self.get(taxonomy_code, slug)["id"]
        else:
            raise InvalidTermIdentification(
                "TaxonomyTerm or Taxonomy Code with slug must be specified")
        current_search_client.delete(
            index=self.index,
            id=id_
        )

    def get(self, taxonomy_code: str, slug: str):
        """
        Return serialized taxonomy term. Takes taxonomy code and slug as strings.

        :type taxonomy_code: str
        :param slug:
        :type slug: str
        :return: Serialized taxonomy term as dict
        :rtype: dict
        """
        if slug.endswith("/"):
            slug = slug[:-1]
        query = Q("term", taxonomy__keyword=taxonomy_code) & Q("term", slug__keyword=slug)
        # s = Search(using=current_search_client, index=self.index)
        # results = list(s.query(query))
        results = self.search(query)
        if len(results) == 1:
            return results[0]
        elif len(results) == 0:
            return None
        else:
            raise Exception(
                f'More than one taxonomy were found, slug \"{slug}\" and taxonomy \"'
                f'{taxonomy_code}\" should be unique.'
            )

    def get_ref(self, taxonomy_url: str):
        """
        Like the get method, it returns a serialized taxonomy. Instead of taxonomy and slug it
        takes the url as an argument.

        :param taxonomy_url: taxonomy term url, could be absolute or relative.
        :type taxonomy_url: str
        :return: Serialized taxonomy term as dict
        :rtype: dict
        """
        taxonomy, slug = _get_taxonomy_slug_from_url(taxonomy_url)
        return self.get(taxonomy, slug)

    def list(self, taxonomy_code: str) -> list:
        """
        Returns list of taxonomy terms. Individual records are serialized taxonomy terms.

        :param taxonomy_code: Code of taxonomy.
        :type taxonomy_code: str
        :return: List of serialized (dict) taxonomy terms
        :rtype: list
        """
        query = Q("match", taxonomy=taxonomy_code)
        return self.search(query)

    def search(self, query: Q, match=False):
        """
        The method returns elasticsearch search results, taking the Q query from
        elasticsearch-dsl as a parameter.

        :param query: `<https://elasticsearch-dsl.readthedocs.io/en/latest/search_dsl.html
        #queries>`_
        :type query: elasticsearch_dsl.Q
        :return: list of jsonify results
        :rtype: list
        """
        s = Search(using=current_search_client, index=self.index)
        search_query = s.query(query)
        if match:
            search_query.sort({
                "_score": {
                    "order": "desc"
                }
            })
            results = list(search_query)
        else:
            results = list(search_query.scan())
        return [result.to_dict() for result in results]

    def reindex(self, taxonomies: list = None) -> datetime:
        """
        Reindex taxonomy index. Update taxonomy term and remove obsolete taxonomy terms.

        :return: UTC timestamp
        :rtype: datetime
        """
        timestamp = datetime.utcnow()
        self._synchronize_es(timestamp=timestamp, taxonomies=taxonomies)
        time.sleep(1)
        self._remove_old_es_term(timestamp, taxonomies=taxonomies)
        return timestamp

    def _synchronize_es(self, timestamp=None, taxonomies: list = None) -> None:
        success, failed = 0, 0
        errors = []
        try:
            with self.app.app_context():
                iterator = iter(self._taxonomy_terms_generator(timestamp, taxonomies=taxonomies))
                for ok, item in streaming_bulk(
                        current_search_client,
                        iterator,
                        raise_on_exception=False):
                    if not ok:
                        errors.append(item)
                        failed += 1
                    else:
                        success += 1
        finally:
            print("REINDEX RESULTS:")
            print(f"Failed: {failed}")
            print(f"Succeed: {success}")
            if len(errors) > 0:
                print("Errors:", errors)
            print("\n\n")

    def _taxonomy_terms_generator(self, timestamp, taxonomies: list = None):
        index_ = self.index
        path = self.app.config["TAXONOMY_ELASTICSEARCH_LOG_DIR"]
        if taxonomies is None:
            query = TaxonomyTerm.query.all()
        else:
            tree_ids = _get_tree_ids(taxonomies)
            query = TaxonomyTerm.query.filter(TaxonomyTerm.tree_id.in_(tree_ids))
        if not os.path.exists(path):
            os.mkdir(path)
        for node in query:
            try:
                if node.parent:
                    body = get_taxonomy_term(
                        code=node.taxonomy.slug,
                        slug=node.slug,
                        timestamp=timestamp
                    )
                    yield {
                        '_op_type': 'index',
                        '_index': index_,
                        '_id': node.id,
                        '_source': body
                    }
            except:
                exc_traceback = traceback.format_exc()
                print(exc_traceback)
                print("\n\n\n")
                if timestamp is None:
                    timestamp = datetime.utcnow()
                file_name = f'{timestamp.strftime("%Y%m%dT%H%M%S")}.err'
                file_path = os.path.join(path, file_name)
                with open(file_path, "a") as f:
                    f.write(
                        f"TAXONOMY CODE: {node.taxonomy.slug}; SLUG: {node.slug}\n\n"
                        f"{exc_traceback}\n\n\n\n")
                continue

    def _remove_old_es_term(self, timestamp, taxonomies: list = None) -> None:
        if taxonomies is None:
            taxonomies = TaxonomyTerm.query.filter_by(level=1).all()
            taxonomies = [taxonomy.slug for taxonomy in taxonomies]
        for taxonomy in taxonomies:
            terms_list = self.list(taxonomy)
            if len(terms_list) == 0:
                print(
                    f"{bcolors.WARNING}WARNING: Taxonomy \"{taxonomy}\" does not exist or does "
                    f"not contain any term{bcolors.ENDC}")
            for node in terms_list:
                date_of_serialization = datetime.strptime(
                    node["date_of_serialization"],
                    '%Y-%m-%d %H:%M:%S.%f'
                )
                if date_of_serialization < timestamp:
                    self.remove(taxonomy_code=node["taxonomy"], slug=node["slug"])
                    print(
                        f'Taxonomy term with slug: \"{node["slug"]}\" from \"{node["taxonomy"]}\" '
                        f'have been removed')
