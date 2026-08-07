"""Find a Peak Element

Locate any index greater than both neighbours, in logarithmic time.
"""

def find_peak(xs):
    lo, hi = 0, len(xs) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if xs[mid] < xs[mid + 1]:
            lo = mid + 1
        else:
            hi = mid
    return lo


if __name__ == "__main__":
    assert find_peak([1, 3, 2]) == 1
    assert find_peak([1, 2, 3]) == 2
    print("peak-element: ok")
