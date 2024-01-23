#!/usr/bin/env python3
"""11-schools_by_topic.py module."""
import pymongo


def schools_by_topic(mongo_collection, topic):
    """
    Return the list of schools having a specific topic.

    :param mongo_collection: pymongo collection object
    :param topic: Topic to search
    :return: List of schools with the specified topic
    """
    # Query documents with the specified topic
    result = mongo_collection.find({"topics": topic})

    # Convert the cursor to a list for easier printing
    schools_list = list(result)

    return schools_list
