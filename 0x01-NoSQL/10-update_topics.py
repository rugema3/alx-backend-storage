#!/usr/bin/env python3
"""10-update_topics.py module. """
import pymongo


def update_topics(mongo_collection, name, topics):
    """
    Change all topics of a school document based on the school name.

    :param mongo_collection: pymongo collection object
    :param name: School name to update
    :param topics: List of topics approached in the school
    """
    # Update documents with the specified school name
    result = mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )

    return result.modified_count
