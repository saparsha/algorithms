"""Rotate Array

Rotate elements right by k using three in-place reversals.
"""

def rotate(xs, k):
    xs = list(xs)
    n = len(xs)
    if n == 0:
        return xs
    k %= n

    def rev(i, j):
        while i < j:
            xs[i], xs[j] = xs[j], xs[i]
            i += 1
            j -= 1

    rev(0, n - 1)
    rev(0, k - 1)
    rev(k, n - 1)
    return xs


if __name__ == "__main__":
    assert rotate([1, 2, 3, 4, 5], 2) == [4, 5, 1, 2, 3]
    assert rotate([1, 2], 0) == [1, 2]
    print("rotate-array: ok")
