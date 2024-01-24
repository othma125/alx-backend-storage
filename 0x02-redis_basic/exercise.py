#!/usr/bin/env python3
"""Cache module"""
import redis
from uuid import uuid4
from typing import Union, Callable


class Cache:
    def __init__(self):
        """Cache class"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Method that stores cache data"""
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None)
    -> Union[str, bytes, int, float]:
        """Method that gets cache data"""
        if fn:
            return fn(self._redis.get(key))
        return self._redis.get(key)

    def get_str(self, key: str) -> str:
        """Method that gets cache data as string"""
        return self.get(key, str)

    def get_int(self, key: str) -> int:
        """Method that gets cache data as int"""
        return self.get(key, int)
