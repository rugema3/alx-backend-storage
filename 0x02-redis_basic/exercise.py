#!/usr/bin/env python3
"""Exercise module."""
import redis
import uuid
from typing import Union


class Cache:
    """
    A simple caching class using Redis.

    Attributes:
    - _redis: An instance of the Redis client.
    """

    def __init__(self):
        """
        Initialize a new Cache instance.

        This creates an instance of the Redis client and flushes the
        Redis database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in the cache and return a unique key.

        Args:
        - data (Union[str, bytes, int, float]): The data to be stored in
        the cache.

        Returns:
        - str: A unique key associated with the stored data.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
