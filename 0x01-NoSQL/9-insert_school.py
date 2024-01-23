#!/usr/bin/env python3
"""9-insert_school.py module. """
import pymongo


def insert_school(mongo_collection, **kwargs):
    """
    Insert a new document in the specified MongoDB collection
    based on keyword arguments.

    :param mongo_collection: pymongo collection object
    :param kwargs: Keyword arguments representing the fields and
                    values of the new document
    :return: The new _id of the inserted document
    """
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
