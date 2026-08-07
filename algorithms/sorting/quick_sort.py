"""Quicksort

In-place Lomuto-partition quicksort with a median-of-three pivot.
"""

def quick_sort(xs, lo=0, hi=None):
    if hi is None:
        hi = len(xs) - 1
    if lo >= hi:
        return xs
    mid = (lo + hi) // 2
    pivot = sorted([xs[lo], xs[mid], xs[hi]])[1]
    i = lo
    for j in range(lo, hi + 1):
        if xs[j] < pivot:
            xs[i], xs[j] = xs[j], xs[i]
            i += 1
    k = i
    for j in range(i, hi + 1):
        if xs[j] == pivot:
            xs[k], xs[j] = xs[j], xs[k]
            k += 1
    quick_sort(xs, lo, i - 1)
    quick_sort(xs, k, hi)
    return xs


if __name__ == "__main__":
    assert quick_sort([3, 6, 1, 6, 2]) == [1, 2, 3, 6, 6]
    assert quick_sort([1]) == [1]
    print("quick-sort: ok")
