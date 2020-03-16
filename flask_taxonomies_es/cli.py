import click
from flask import cli, current_app
from flask_taxonomies.cli import taxonomies
from flask_taxonomies.models import Taxonomy

from flask_taxonomies_es.proxies import current_flask_taxonomies_es


@taxonomies.group()
def es():
    pass


@es.command("set")
@click.argument("taxonomy")
@click.argument("slug")
@cli.with_appcontext
def set_(taxonomy: str, slug: str):
    taxonomy = Taxonomy.get(taxonomy)
    term = taxonomy.get_term(slug)
    current_flask_taxonomies_es.set(term)


@es.command("get")
@click.argument("taxonomy")
@click.argument("slug")
@cli.with_appcontext
def get_(taxonomy: str, slug: str):
    current_flask_taxonomies_es.get(taxonomy, slug)


@es.command("get_ref")
@click.argument("url")
@cli.with_appcontext
def get_ref_(url: str):
    current_flask_taxonomies_es.get_ref(url)


@es.command("remove")
@click.argument("taxonomy")
@click.argument("slug")
@cli.with_appcontext
def remove_(taxonomy: str, slug: str):
    current_flask_taxonomies_es.remove(taxonomy_code=taxonomy, slug=slug)


@es.command("list")
@click.argument("taxonomy")
@cli.with_appcontext
def list_(taxonomy: str):
    current_flask_taxonomies_es.list(taxonomy)


@es.command("reindex")
@cli.with_appcontext
def list_():
    api = current_app.wsgi_app.mounts['/api']
    with api.app_context():
        current_flask_taxonomies_es.reindex()
