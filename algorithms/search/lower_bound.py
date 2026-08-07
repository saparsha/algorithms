"""Lower Bound

First index whose value is >= target, i.e. the insertion point.
"""

def lower_bound(xs, target):
    lo, hi = 0, len(xs)
    while lo < hi:
        mid = (lo + hi) // 2
        if xs[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo


if __name__ == "__main__":
    assert lower_bound([1, 2, 4, 4, 5], 4) == 2
    assert lower_bound([1, 2, 3], 9) == 3
    assert lower_bound([], 1) == 0
    print("lower-bound: ok")
