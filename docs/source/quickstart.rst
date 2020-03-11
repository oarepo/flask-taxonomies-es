*************
Quickstart
*************

The package is an extension of Flask-Taxonomies and is directly linked to Invenio 3.x. You must have Elasticsearch
server set up in Invenio. The whole logic is based on Blinker signals, so the package should be functional right after
installation.

Access to the API is established through a Proxy object. All methods are called via: current_taxonomies_es.

The API contains all CRUD methods. The most important methods for users are to obtain taxonomy from Elasticsearch.
Here we set up two methods get and get_ref.

The **get** method requires two mandatory arguments for the taxonomy code and slug,
which uniquely identify the taxonomy term.

.. code-block:: python

    from flask-taxonomies-es import current_flask_taxonomies_es

    taxonomy_dict = current_flask_taxonomies_es.get("taxonomy_code", "slug")

The get_ref method requires a url address for a taxonomic term. The address can be absolute or relative.
In the background, the urllib.parse library is used, which gets the path
and then creates an Elasticsearch query based on the path.

.. code-block:: python

    from flask-taxonomies-es import current_flask_taxonomies_es

    taxonomy_dict_relative = current_flask_taxonomies_es.get_ref("api/taxonomies/relative_address_slug")
    taxonomy_dict_absolut = current_flask_taxonomies_es.get_ref("https://wonderfulweb.com/api/taxonomies/relative_address_slug")

The API contains additional methods that are automatically called based on a signal from Flask-Taxonomies_.

See the `API documentation`_ for more information.


.. _Flask-Taxonomies: https://github.com/oarepo/flask-taxonomies
.. _API documentation: api.html