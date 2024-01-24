#!/usr/bin/env python3
"""Exercise module."""
import redis
import uuid
from typing import Union, Callable, Optional, Any


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

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """
        Retrieve data from the cache using the provided key.

        Args:
        - key (str): The key associated with the stored data.
        - fn (Callable, optional): A callable function to convert the data
                                    back to the desired format.

        Returns:
        - Union[str, bytes, int, float, None]: The retrieved data or None if
                                                the key does not exist.
        """
        data = self._redis.get(key)
        if data is not None and fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Union[str, None]:
        """
        Retrieve data from the cache and convert it to a string.

        Args:
        - key (str): The key associated with the stored data.

        Returns:
        - Union[str, None]: The retrieved data as a string or None if the
                            key does not exist.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """
        Retrieve data from the cache and convert it to an integer.

        Args:
        - key (str): The key associated with the stored data.

        Returns:
        - Union[int, None]: The retrieved data as an integer or
                            None if the key does not exist.
        """
        return self.get(key, fn=int)
