"""Upper Bound

First index whose value is strictly greater than target.
"""

def upper_bound(xs, target):
    lo, hi = 0, len(xs)
    while lo < hi:
        mid = (lo + hi) // 2
        if xs[mid] <= target:
            lo = mid + 1
        else:
            hi = mid
    return lo


if __name__ == "__main__":
    assert upper_bound([1, 2, 4, 4, 5], 4) == 4
    assert upper_bound([1, 2, 3], 0) == 0
    print("upper-bound: ok")
