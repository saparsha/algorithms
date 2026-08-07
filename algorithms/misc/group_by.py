"""Group By Key

Bucket items into a dictionary keyed by a derived value.
"""

from collections import defaultdict


def group_by(items, key):
    groups = defaultdict(list)
    for item in items:
        groups[key(item)].append(item)
    return dict(groups)


if __name__ == "__main__":
    assert group_by(range(5), lambda n: n % 2) == {0: [0, 2, 4], 1: [1, 3]}
    print("group-by: ok")
