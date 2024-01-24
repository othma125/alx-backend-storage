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
    def invoker(url) -> str:
        """Returns the cached data if available, otherwise fetches it.
        """
        data = r.get(url)
        if data:
            return data.decode('utf-8')
        data = method(url)
        r.setex(url, 10, data)
        return data
    return invoker


@data_cacher
def get_page(url: str) -> str:
    """Returns the content of a URL after caching the request's response,
    and tracking the request.
    """
    return get(url).text
