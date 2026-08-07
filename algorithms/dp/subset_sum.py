"""Subset Sum

Decide whether some subset adds up exactly to a target.
"""

def subset_sum(xs, target):
    reachable = 1
    for x in xs:
        reachable |= reachable << x
    return bool(reachable >> target & 1)


if __name__ == "__main__":
    assert subset_sum([3, 34, 4, 12, 5, 2], 9)
    assert not subset_sum([1, 2], 7)
    print("subset-sum: ok")
