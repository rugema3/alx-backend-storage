#!/usr/bin/env python3
"""a Python function that returns all students sorted by average score."""


def top_students(mongo_collection):
    """
    Return all students sorted by average score.

    :param mongo_collection: pymongo collection object
    :return: List of students with the average score
    """
    pipeline = [
        {
            "$addFields": {
                "averageScore": {
                    "$avg": "$topics.score"
                }
            }
        },
        {
            "$sort": {
                "averageScore": -1
            }
        }
    ]

    return list(mongo_collection.aggregate(pipeline))
