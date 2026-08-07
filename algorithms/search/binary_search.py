"""Binary Search

Locate a target in a sorted sequence in O(log n) comparisons.
"""

def binary_search(xs, target):
    lo, hi = 0, len(xs) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if xs[mid] == target:
            return mid
        if xs[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return None


if __name__ == "__main__":
    assert binary_search([1, 3, 5, 7, 9], 7) == 3
    assert binary_search([1, 3, 5], 4) is None
    assert binary_search([], 1) is None
    print("binary-search: ok")
