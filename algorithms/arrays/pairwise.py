"""Pairwise Iteration

Yield consecutive overlapping pairs from an iterable.
"""

def pairwise(xs):
    it = iter(xs)
    prev = next(it, None)
    for cur in it:
        yield prev, cur
        prev = cur


if __name__ == "__main__":
    assert list(pairwise([1, 2, 3])) == [(1, 2), (2, 3)]
    assert list(pairwise([1])) == []
    print("pairwise: ok")
