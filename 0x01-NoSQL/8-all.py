#!/usr/bin/env python3
""" 8-all module. """

import pymongo


def list_all(mongo_collection):
    """
    List all documents in the specified MongoDB collection.

    :param mongo_collection: pymongo collection object
    :return: List of documents
    """
    if mongo_collection is None:
        return []
    return list(mongo_collection.find())
