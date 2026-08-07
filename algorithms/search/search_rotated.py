"""Search in Rotated Array

Binary search over a sorted array that has been rotated at an unknown pivot.
"""

def search_rotated(xs, target):
    lo, hi = 0, len(xs) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if xs[mid] == target:
            return mid
        if xs[lo] <= xs[mid]:
            if xs[lo] <= target < xs[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:
            if xs[mid] < target <= xs[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return None


if __name__ == "__main__":
    assert search_rotated([4, 5, 6, 7, 0, 1, 2], 0) == 4
    assert search_rotated([4, 5, 6, 7, 0, 1, 2], 3) is None
    print("search-rotated: ok")
