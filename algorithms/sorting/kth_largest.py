"""Quickselect

Expected O(n) selection of the k-th smallest element.
"""

def quickselect(xs, k):
    xs = list(xs)
    lo, hi = 0, len(xs) - 1
    while True:
        pivot = xs[(lo + hi) // 2]
        i, j = lo, hi
        while i <= j:
            while xs[i] < pivot:
                i += 1
            while xs[j] > pivot:
                j -= 1
            if i <= j:
                xs[i], xs[j] = xs[j], xs[i]
                i += 1
                j -= 1
        if k <= j:
            hi = j
        elif k >= i:
            lo = i
        else:
            return xs[k]


if __name__ == "__main__":
    assert quickselect([7, 2, 9, 4], 0) == 2
    assert quickselect([7, 2, 9, 4], 3) == 9
    print("kth-largest: ok")
