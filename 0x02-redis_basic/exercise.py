#!/usr/bin/env python3
"""Cache module"""
import redis
from uuid import uuid4
from typing import Union


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
