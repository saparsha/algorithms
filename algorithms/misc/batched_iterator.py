"""Batched Iterator

Lazily yield fixed-size batches from any iterable.
"""

from itertools import islice


def batched(iterable, size):
    if size <= 0:
        raise ValueError("size must be positive")
    it = iter(iterable)
    while batch := list(islice(it, size)):
        yield batch


if __name__ == "__main__":
    assert list(batched(range(5), 2)) == [[0, 1], [2, 3], [4]]
    assert list(batched([], 3)) == []
    print("batched-iterator: ok")
