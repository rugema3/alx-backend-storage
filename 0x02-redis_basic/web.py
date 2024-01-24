#!/usr/bin/env python3
"""Web module."""
import redis
import requests

r = redis.Redis()
count = 0


def get_page(url: str) -> str:
    """
    Obtain the HTML content of a particular URL and return it.

    Track how many times a particular URL was accessed in the key
    "count:{url}" and cache the result with an expiration time of 10 seconds.

    Args:
    - url (str): The URL of the web page.

    Returns:
    - str: The HTML content of the web page.
    """
    count_key = f"count:{url}"
    cache_key = f"cached:{url}"

    # Check if the result is cached
    cached_count = r.get(cache_key)
    if cached_count:
        r.incr(count_key)
        return cached_count.decode()

    # If not cached, fetch the page and cache the result
    resp = requests.get(url)
    r.incr(count_key)
    r.setex(cache_key, 10, str(count))
    return resp.text


if __name__ == "__main__":
    url = 'http://slowwly.robertomurray.co.uk'
    html_content = get_page(url)
    print(html_content)
