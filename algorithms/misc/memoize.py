"""Memoization Decorator

Cache function results keyed on their arguments.
"""

import functools


def memoize(fn):
    cache = {}

    @functools.wraps(fn)
    def wrapper(*args):
        if args not in cache:
            cache[args] = fn(*args)
        return cache[args]

    wrapper.cache = cache
    return wrapper


if __name__ == "__main__":
    calls = []


    @memoize
    def slow_square(n):
        calls.append(n)
        return n * n


    assert slow_square(4) == 16 and slow_square(4) == 16
    assert calls == [4]
    print("memoize: ok")
