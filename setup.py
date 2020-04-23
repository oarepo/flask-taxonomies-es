# -*- coding: utf-8 -*-
"""Setup module for flask taxonomy."""
import os

from setuptools import setup

readme = open('README.rst').read()

DATABASE = "postgresql"
OAREPO_VERSION = os.environ.get('OAREPO_VERSION', '3.1.1')

install_requires = [
    'flask-taxonomies',
    'elasticsearch>=7.0.0,<8.0.0',
    'elasticsearch-dsl>=7.0.0,<8.0.0',
    'webargs<6.0.0',
    'email_validator'
]

tests_require = [
    'pytest>=4.6.3',
    'pytest-cov',
    'pytest-flask==0.15.1'
]

extras_require = {
    'docs': [
        'sphinx',
        'webargs<6.0.0',
        'oarepo[tests]~={version}'.format(
            version=OAREPO_VERSION)
    ],
    'postgresql': [
        'flask-taxonomies[postgresql]',
    ],
    'sqlite': [
        'flask-taxonomies[sqlite]',
    ],
    'tests': [
        *tests_require,
        'oarepo[tests]~={version}'.format(
            version=OAREPO_VERSION)],
    'tests-es7': [
        *tests_require,
        'oarepo[tests-es7]~={version}'.format(
            version=OAREPO_VERSION)],
}

setup_requires = [
    'pytest-runner>=2.7',
]

g = {}
with open(os.path.join('flask_taxonomies_es', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
version = g['__version__']

setup(
    name="flask_taxonomies_es",
    version=version,
    url="https://github.com/oarepo/flask-taxonomies-es",
    license="MIT",
    author="Daniel Kopecký",
    author_email="Daniel.Kopecky@techlib.cz",
    description="Elasticsearch extension for Flask-Taxonomies",
    zip_safe=False,
    packages=['flask_taxonomies_es'],
    entry_points={
        'invenio_base.apps': [
            'flask_taxonomies = flask_taxonomies_es.ext:FlaskTaxonomiesES',
        ],
        'invenio_base.api_apps': [
            'flask_taxonomies = flask_taxonomies_es.ext:FlaskTaxonomiesES',
        ],
        'flask.commands': [
            'taxonomies_es = flask_taxonomies_es.cli:taxonomies',
        ]
    },
    include_package_data=True,
    setup_requires=setup_requires,
    extras_require=extras_require,
    install_requires=install_requires,
    tests_require=tests_require,
    platforms='any',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Development Status :: 4 - Beta',
    ],
)
