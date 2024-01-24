#!/usr/bin/env python3
"""A module with tools for request caching and tracking.
"""
import redis
from requests import get
from functools import wraps
from typing import Callable


r = redis.Redis()


def data_cacher(method: Callable) -> Callable:
    """Caches the output of fetched data.
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        """Returns the cached data if available, otherwise fetches it.
        """
        r.incr(f"count:{url}")
        if r.exists(f"{method.__qualname__}"):
            return r.get(f"result:{url}")
        result = method(url)
        # r.set(f'count:{url}', 0)
        r.setex(f"{method.__qualname__}", 10, result)
        return result
    return wrapper


@data_cacher
def get_page(url: str) -> str:
    """Returns the content of a URL after caching the request's response,
    and tracking the request.
    """
    return get(url).text
