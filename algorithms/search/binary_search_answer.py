"""Binary Search on the Answer

Smallest value in a range satisfying a monotone predicate.
"""

def first_true(lo, hi, pred):
    while lo < hi:
        mid = (lo + hi) // 2
        if pred(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


if __name__ == "__main__":
    assert first_true(0, 100, lambda n: n * n >= 50) == 8
    assert first_true(0, 10, lambda n: n >= 0) == 0
    print("binary-search-answer: ok")
