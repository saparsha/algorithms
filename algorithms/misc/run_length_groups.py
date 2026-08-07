"""Consecutive Runs

Split a sequence into runs of consecutive equal elements.
"""

from itertools import groupby


def runs(xs):
    return [(key, len(list(group))) for key, group in groupby(xs)]


if __name__ == "__main__":
    assert runs([1, 1, 2, 3, 3, 3]) == [(1, 2), (2, 1), (3, 3)]
    assert runs([]) == []
    print("run-length-groups: ok")
