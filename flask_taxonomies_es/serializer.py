# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""JSON resolver for JSON schemas."""

from __future__ import absolute_import, print_function

from datetime import datetime
import traceback
from typing import List

from flask_taxonomies.models import (
    Taxonomy,
    TaxonomyTerm)
from flask_taxonomies.proxies import current_flask_taxonomies
from flask_taxonomies.views import format_ancestor


def get_taxonomy_term(code=None, slug=None, timestamp=None):
    try:
        taxonomy = Taxonomy.get(code)
        term = taxonomy.find_term(slug)
        parents = [format_ancestor(x) for x in term.ancestors]
    except:
        traceback.print_exc()
        raise ValueError("The taxonomy term does not exist.")
    resp = jsonify_taxonomy_term(term, taxonomy.code, term.tree_path,
                                 term.parent.tree_path or '', parents, timestamp=timestamp)
    return resp


def jsonify_taxonomy_term(t: TaxonomyTerm,
                          taxonomy_code,
                          path: str,
                          parent_path: str = None,
                          parents: List = None,
                          timestamp=None
                          ) -> dict:
    """Prepare TaxonomyTerm to be easily jsonified."""
    if not path.startswith('/'):
        raise Exception()
    result = {
        **(t.extra_data or {}),
        "date_of_serialization": str(timestamp) if timestamp else str(datetime.utcnow()),
        "id": t.id,
        "slug": t.slug,
        "taxonomy": t.taxonomy.slug,
        "path": path,
        "links": current_flask_taxonomies.term_links(taxonomy_code, path, parent_path),
        "level": t.level - 1
    }

    if parents:
        result['ancestors'] = [*parents]

    descendants_count = (t.right - t.left - 1) / 2
    if descendants_count:
        result["descendants_count"] = descendants_count

    return result
