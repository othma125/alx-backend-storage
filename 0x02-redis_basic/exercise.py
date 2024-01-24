#!/usr/bin/env python3
"""Cache module"""
import redis
from uuid import uuid4
from typing import Union, Callable, Any
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Tracks the number of calls made to a method in a Cache class.
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """Invokes the given method after incrementing its call counter.
        """
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """Tracks the call details of a method in a Cache class.
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """Returns the method's output after storing its inputs and output.
        """
        in_key = f'{method.__qualname__}:inputs'
        out_key = f'{method.__qualname__}:outputs'
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(in_key, str(args))
            output = method(self, *args, **kwargs)
            self._redis.rpush(out_key, str(output))
            return output
        return None

    return wrapper


def replay(fn: Callable) -> None:
    """Displays the call history of a Cache class' method.
    """
    if fn is None or not hasattr(fn, '__self__'):
        return
    r = getattr(fn.__self__, '_redis', None)
    if not isinstance(r, redis.Redis):
        return
    fn_name = fn.__qualname__
    count: int = r.get(fn_name) if r.exists(fn_name) else 0
    print(f'{fn_name} was called {count} times:')
    inputs = r.lrange(f'{fn_name}:inputs', 0, -1)
    outputs = r.lrange(f'{fn_name}:outputs', 0, -1)
    for i, o in zip(inputs, outputs):
        print(f'{fn_name}(*{i.decode("utf-8")}) -> {o}')


DataType = Union[str, bytes, int, float]


class Cache:
    def __init__(self):
        """Cache class"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: DataType) -> str:
        """Method that stores cache data"""
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> DataType:
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
